"""
CareerShield AI — skill_extractor.py
Class: SkillExtractor
Extracts and categorizes skills from raw resume text.
Uses SkillTrie (DSA) for O(m) lookup.
Tech: Python OOP | DSA (Trie)
"""

import re
from typing import Set, Dict, List

from dsa import SkillTrie


# ── Master Vocabulary ──────────────────────────────────────────

SKILL_VOCABULARY: List[str] = [
    # Languages
    "python", "java", "c++", "c", "javascript", "typescript", "r", "scala",
    "kotlin", "swift", "go", "rust", "php", "bash",
    # AI / ML
    "machine learning", "deep learning", "neural networks", "nlp",
    "natural language processing", "computer vision", "reinforcement learning",
    "transformers", "bert", "llm", "generative ai", "mlops",
    "feature engineering", "model deployment", "xgboost", "random forest",
    "linear regression", "logistic regression", "svm", "clustering",
    # Frameworks
    "tensorflow", "pytorch", "keras", "scikit-learn",
    "pandas", "numpy", "matplotlib", "seaborn", "plotly",
    "flask", "django", "fastapi", "huggingface", "spacy", "nltk",
    "opencv", "yolo",
    # Data & DB
    "sql", "mysql", "postgresql", "sqlite", "mongodb", "redis",
    "elasticsearch", "nosql", "data analysis", "data visualization",
    "data modeling", "data pipeline", "etl", "spark", "hadoop",
    "tableau", "power bi", "excel", "statistics", "probability",
    "indexing", "stored procedures", "triggers", "views", "normalization",
    "transactions", "acid",
    # CS Fundamentals
    "data structures", "algorithms", "oop", "object oriented programming",
    "system design", "distributed systems", "operating systems",
    "dbms", "networking", "design patterns", "solid principles",
    "rest api", "graphql", "microservices", "debugging", "testing",
    "unit testing", "concurrency", "multithreading", "async",
    # DevOps / Cloud
    "docker", "kubernetes", "git", "github", "ci/cd",
    "aws", "azure", "gcp", "linux", "terraform",
    # Tools / Process
    "jira", "agile", "scrum", "sdlc", "jupyter",
    # Data science extras
    "data modeling", "feature engineering",
]

# Aliases → canonical skill
ALIASES: Dict[str, str] = {
    "ml": "machine learning",
    "dl": "deep learning",
    "cv": "computer vision",
    "dsa": "data structures",
    "ds": "data structures",
    "nlp": "nlp",
    "oop": "oop",
    "dbms": "dbms",
    "js": "javascript",
    "ts": "typescript",
    "sklearn": "scikit-learn",
    "llm": "llm",
    "llms": "llm",
    "genai": "generative ai",
    "rest": "rest api",
    "restful": "rest api",
    "k8s": "kubernetes",
    "ci/cd": "ci/cd",
    "object oriented": "oop",
    "object-oriented": "oop",
    "data structure": "data structures",
    "algorithm": "algorithms",
    "natural language processing": "nlp",
    "computer network": "networking",
}

# Skill categories for grouping
SKILL_CATEGORIES: Dict[str, Set[str]] = {
    "Languages": {
        "python", "java", "c++", "javascript", "typescript", "r",
        "scala", "go", "kotlin", "swift", "bash"
    },
    "AI / ML": {
        "machine learning", "deep learning", "nlp", "computer vision",
        "transformers", "bert", "tensorflow", "pytorch", "keras",
        "scikit-learn", "xgboost", "llm", "generative ai",
        "reinforcement learning", "mlops", "opencv", "yolo",
        "huggingface", "spacy", "feature engineering",
    },
    "Data & Databases": {
        "sql", "pandas", "numpy", "mysql", "postgresql", "mongodb",
        "sqlite", "data visualization", "data analysis", "etl",
        "spark", "tableau", "power bi", "statistics", "excel",
        "data modeling", "stored procedures", "indexing", "dbms",
        "triggers", "views", "normalization",
    },
    "CS Fundamentals": {
        "data structures", "algorithms", "oop", "system design",
        "rest api", "debugging", "testing", "unit testing",
        "design patterns", "networking", "operating systems",
        "concurrency", "distributed systems",
    },
    "DevOps / Cloud": {
        "docker", "kubernetes", "git", "aws", "azure",
        "gcp", "linux", "ci/cd", "terraform"
    },
    "Tools & Process": {
        "jira", "agile", "scrum", "sdlc", "jupyter",
        "github", "flask", "django", "fastapi",
    },
}


class SkillExtractor:
    """
    Extracts technical skills from resume text using:
    1. A SkillTrie for O(m) exact-match lookups (DSA)
    2. Alias mapping for abbreviations (ml → machine learning)
    3. Multi-word skill matching (longest match first)
    """

    def __init__(self):
        self._trie = SkillTrie()
        self._aliases = ALIASES
        self._build_trie()

    def _build_trie(self) -> None:
        for skill in SKILL_VOCABULARY:
            self._trie.insert(skill)

    @staticmethod
    def _normalize(text: str) -> str:
        text = text.lower()
        text = re.sub(r"[_|\\]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def extract(self, resume_text: str) -> Set[str]:
        """
        Extract all skills from raw resume text.
        Returns a set of canonical skill names.
        """
        if not resume_text or not resume_text.strip():
            return set()

        text = self._normalize(resume_text)
        found: Set[str] = set()

        # 1. Alias matching
        for alias, canonical in self._aliases.items():
            pattern = r"\b" + re.escape(alias) + r"\b"
            if re.search(pattern, text):
                found.add(canonical)

        # 2. Vocabulary matching via Trie (multi-word skills first → greedy longest match)
        vocab_sorted = sorted(SKILL_VOCABULARY, key=lambda s: len(s.split()), reverse=True)
        for skill in vocab_sorted:
            if self._trie.search(skill):       # O(m) Trie lookup
                pattern = r"\b" + re.escape(skill) + r"\b"
                if re.search(pattern, text):
                    found.add(skill)

        return found

    def categorize(self, skills: Set[str]) -> Dict[str, List[str]]:
        """Group skills by category."""
        result: Dict[str, List[str]] = {}
        uncategorized = set(skills)

        for category, cat_skills in SKILL_CATEGORIES.items():
            matched = skills & cat_skills
            if matched:
                result[category] = sorted(matched)
                uncategorized -= matched

        if uncategorized:
            result["Other"] = sorted(uncategorized)

        return result
