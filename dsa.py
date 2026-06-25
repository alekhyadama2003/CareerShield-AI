"""
CareerShield AI — dsa.py
DSA Components used internally by CareerShield AI.

Structures:
  TrieNode / SkillTrie  — O(m) skill lookup and prefix matching (m = skill length)
  JobHeap               — Min-heap for maintaining top-N job matches by score
  SkillFrequencyMap     — HashMap-based frequency counter for gap analysis

Tech: Python OOP | Data Structures & Algorithms
"""

import heapq
from typing import List, Tuple, Optional, Set


# ══════════════════════════════════════════════════════════════
# 1. TRIE — Skill Vocabulary Lookup
# ══════════════════════════════════════════════════════════════

class TrieNode:
    """Single node in a Trie."""

    __slots__ = ("children", "is_end", "skill")

    def __init__(self):
        self.children: dict = {}   # char → TrieNode
        self.is_end: bool = False  # marks a complete skill
        self.skill: str = ""       # stores canonical skill string at terminal node


class SkillTrie:
    """
    Trie data structure for O(m) skill insertion and lookup.
    Used by SkillExtractor to match skills from resume text efficiently.

    Why Trie over set?
      - Supports prefix queries (autocomplete / partial matching)
      - O(m) lookup where m = word length, same as hash set average
        but deterministic and cache-friendly for long multi-word skills
      - Easily extended for fuzzy / typo matching
    """

    def __init__(self):
        self._root = TrieNode()
        self._size = 0

    def insert(self, skill: str) -> None:
        """Insert a skill (lowercased) into the Trie."""
        node = self._root
        skill = skill.lower().strip()
        for ch in skill:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        if not node.is_end:
            node.is_end = True
            node.skill = skill
            self._size += 1

    def search(self, skill: str) -> bool:
        """Return True if the exact skill exists in the Trie."""
        node = self._find_node(skill.lower().strip())
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> bool:
        """Return True if any skill starts with prefix."""
        return self._find_node(prefix.lower().strip()) is not None

    def all_skills(self) -> List[str]:
        """Return all skills stored in the Trie (DFS traversal)."""
        results = []
        self._dfs(self._root, [], results)
        return results

    def _find_node(self, text: str) -> Optional[TrieNode]:
        node = self._root
        for ch in text:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def _dfs(self, node: TrieNode, path: list, results: list) -> None:
        if node.is_end:
            results.append(node.skill)
        for ch, child in node.children.items():
            path.append(ch)
            self._dfs(child, path, results)
            path.pop()

    def __len__(self) -> int:
        return self._size

    def __contains__(self, skill: str) -> bool:
        return self.search(skill)


# ══════════════════════════════════════════════════════════════
# 2. MIN-HEAP — Top-N Job Match Ranker
# ══════════════════════════════════════════════════════════════

class JobHeapEntry:
    """
    Heap entry wrapping a JobMatch result.
    Implements __lt__ so heapq (min-heap) can compare entries.
    We negate score so the heap keeps the TOP-N highest scores.
    """

    __slots__ = ("score", "ats_score", "job_id", "payload")

    def __init__(self, score: float, ats_score: float, job_id: int, payload):
        self.score = score
        self.ats_score = ats_score
        self.job_id = job_id
        self.payload = payload  # The full JobMatch object

    def __lt__(self, other: "JobHeapEntry") -> bool:
        # Min-heap: smallest score on top → we can pop when size > N
        if self.score != other.score:
            return self.score < other.score
        return self.ats_score < other.ats_score


class JobHeap:
    """
    Fixed-size min-heap that maintains the top-N job matches.

    Algorithm:
      - Push each match. If heap size > N, pop the minimum (worst match).
      - Result: heap holds the N best matches in O(n log k) time,
        better than sorting all n jobs O(n log n) when k << n.
    """

    def __init__(self, capacity: int):
        self._capacity = capacity
        self._heap: List[JobHeapEntry] = []

    def push(self, score: float, ats_score: float, job_id: int, payload) -> None:
        entry = JobHeapEntry(score, ats_score, job_id, payload)
        heapq.heappush(self._heap, entry)
        if len(self._heap) > self._capacity:
            heapq.heappop(self._heap)  # remove the weakest match

    def top_n(self) -> list:
        """Return top-N matches sorted descending by score."""
        return [e.payload for e in sorted(self._heap, reverse=True)]

    def __len__(self) -> int:
        return len(self._heap)


# ══════════════════════════════════════════════════════════════
# 3. SKILL FREQUENCY MAP — Gap Priority Counter
# ══════════════════════════════════════════════════════════════

class SkillFrequencyMap:
    """
    HashMap-based counter for skill gap analysis.
    Tracks how many job matches each missing skill appears in.
    Used to prioritize the learning roadmap.

    Time complexity: O(1) insert/lookup (Python dict = hash map)
    """

    def __init__(self):
        self._map: dict = {}  # skill → count

    def add(self, skill: str) -> None:
        skill = skill.lower().strip()
        self._map[skill] = self._map.get(skill, 0) + 1

    def get(self, skill: str) -> int:
        return self._map.get(skill.lower().strip(), 0)

    def top_k(self, k: int) -> List[Tuple[str, int]]:
        """Return top-k skills by frequency using partial sort (heapq.nlargest)."""
        return heapq.nlargest(k, self._map.items(), key=lambda x: x[1])

    def all_sorted(self) -> List[Tuple[str, int]]:
        return sorted(self._map.items(), key=lambda x: x[1], reverse=True)

    def __len__(self) -> int:
        return len(self._map)
