"""
CareerShield AI — career_advisor.py
Class: CareerAdvisor
Handles career recommendations, skill gap analysis, and learning roadmap.
Uses SkillFrequencyMap (DSA) for gap prioritization.
Tech: Python OOP | DSA (HashMap / heapq)
"""

from typing import List, Set, Dict, Tuple
from dsa import SkillFrequencyMap
from database import DatabaseManager
from models import JobMatch


# ── Career Path Definitions ────────────────────────────────────

CAREER_PATHS: Dict[str, Set[str]] = {
    "AI/ML Engineer":            {"machine learning", "deep learning", "python", "tensorflow", "pytorch"},
    "Data Scientist":            {"python", "statistics", "machine learning", "pandas", "sql"},
    "Backend Developer":         {"python", "sql", "dbms", "oop", "data structures"},
    "NLP Engineer":              {"nlp", "python", "machine learning", "deep learning"},
    "Computer Vision Engineer":  {"computer vision", "opencv", "deep learning", "python"},
    "Data Analyst":              {"sql", "excel", "data visualization", "statistics", "python"},
    "Database Administrator":    {"sql", "dbms", "data modeling", "indexing", "stored procedures"},
    "SDE (General)":             {"python", "data structures", "algorithms", "sql", "oop"},
    "Full Stack Developer":      {"python", "javascript", "sql", "git"},
    "DevOps Engineer":           {"docker", "kubernetes", "linux", "ci/cd", "aws"},
}

# ── Learning Resources ─────────────────────────────────────────

LEARNING_RESOURCES: Dict[str, List[str]] = {
    "machine learning":    ["Andrew Ng ML Course (Coursera)", "Hands-On ML — Aurélien Géron (Book)"],
    "deep learning":       ["Deep Learning Specialization — deeplearning.ai", "Fast.ai Practical DL"],
    "python":              ["Python.org Official Tutorial", "Automate the Boring Stuff (Book)"],
    "sql":                 ["SQLZoo Interactive Tutorial", "LeetCode SQL 50"],
    "data structures":     ["Striver's DSA Sheet (takeuforward.org)", "NeetCode 150"],
    "algorithms":          ["NeetCode 150", "CLRS — Introduction to Algorithms (Book)"],
    "system design":       ["System Design Primer (GitHub)", "Designing Data-Intensive Apps (Book)"],
    "docker":              ["Docker Official Get Started Guide", "TechWorld with Nana — Docker YT"],
    "kubernetes":          ["Kubernetes Interactive Tutorial (Official)", "KodeKloud CKA Course"],
    "aws":                 ["AWS Skill Builder (Free)", "Stephane Maarek AWS SAA Course"],
    "nlp":                 ["HuggingFace NLP Course (Free)", "Speech & Language Processing — Jurafsky"],
    "computer vision":     ["CS231n — Stanford (YouTube)", "OpenCV Python Tutorials (Official)"],
    "statistics":          ["StatQuest with Josh Starmer (YouTube)", "Statistics for Data Science — DataCamp"],
    "git":                 ["Pro Git Book (Free)", "Learn Git Branching (Interactive)"],
    "tensorflow":          ["TensorFlow Official Tutorials", "Deep Learning with Python — Chollet"],
    "pytorch":             ["PyTorch 60-Minute Blitz (Official)", "Zero to Mastery PyTorch"],
    "oop":                 ["Python OOP — Corey Schafer (YouTube)", "Head First Design Patterns (Book)"],
    "dbms":                ["CMU Database Systems (YouTube)", "Database System Concepts — Silberschatz"],
    "linux":               ["The Linux Command Line (Free Book)", "Linux Journey (Interactive)"],
    "ci/cd":               ["GitHub Actions Official Docs", "Jenkins Pipeline Tutorial"],
    "data visualization":  ["Matplotlib Official Tutorial", "Seaborn Gallery + Docs"],
    "data modeling":       ["Database Design Course — freeCodeCamp (YouTube)"],
    "stored procedures":   ["SQL Server Stored Procedures Tutorial — W3Schools", "Mode SQL Tutorial"],
    "indexing":            ["Use The Index, Luke! (Free Book)", "MySQL Indexing — Official Docs"],
    "transformers":        ["HuggingFace Transformers Course (Free)", "Attention Is All You Need (Paper)"],
    "opencv":              ["OpenCV-Python Tutorials (Official)", "CS231n Lecture Notes"],
    "testing":             ["pytest Official Docs", "Test-Driven Development with Python — Book"],
}

# Phases: (label, skill_count)
ROADMAP_PHASES = [
    ("Phase 1 — Immediate (0-1 Month)",   2),
    ("Phase 2 — Short-Term (1-3 Months)", 3),
    ("Phase 3 — Mid-Term (3-6 Months)",   3),
]


class CareerAdvisor:
    """
    Produces:
    1. Career path recommendations (overlap scoring)
    2. Skill gap analysis (SkillFrequencyMap — DSA)
    3. Prioritized learning roadmap
    """

    def __init__(self, db: DatabaseManager):
        self._db = db

    # ── 1. Career Recommendations ─────────────────────────────────

    def recommend_careers(self, resume_skills: Set[str]) -> List[str]:
        """
        Rank career paths by skill overlap ratio.
        Returns list of formatted recommendation strings.
        """
        resume_lower = {s.lower() for s in resume_skills}
        scored = []

        for career, required in CAREER_PATHS.items():
            overlap = len(resume_lower & required)
            ratio = overlap / len(required) if required else 0.0
            if ratio >= 0.2:
                fit = (
                    "Strong Fit" if ratio >= 0.6
                    else "Good Fit" if ratio >= 0.4
                    else "Developing"
                )
                scored.append((career, ratio, fit))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [
            f"{career}  [{fit} — {round(ratio * 100)}% alignment]"
            for career, ratio, fit in scored[:5]
        ]

    # ── 2. Skill Gap Analysis ─────────────────────────────────────

    def analyze_gaps(
        self,
        top_matches: List[JobMatch],
    ) -> Tuple[List[str], List[Tuple[str, int]]]:
        """
        Aggregate missing required skills across top job matches.
        Uses SkillFrequencyMap (DSA HashMap) to count occurrences.
        Boosts priority using DB market demand data.
        Returns (ordered unique skills, [(skill, job_count)] sorted by priority).
        """
        freq_map = SkillFrequencyMap()
        for match in top_matches:
            for skill in match.missing_required:
                freq_map.add(skill)

        # Fetch demand weights from DB
        demand_rows = self._db.fetch_skill_demand(limit=50)
        demand_map = {row["skill"]: row["demand_count"] for row in demand_rows}

        # Re-sort by composite: (job_count * 10) + market_demand
        all_gaps = freq_map.all_sorted()
        prioritized = sorted(
            all_gaps,
            key=lambda x: (x[1] * 10) + demand_map.get(x[0], 0),
            reverse=True,
        )

        return [skill for skill, _ in prioritized], prioritized

    # ── 3. Learning Roadmap ───────────────────────────────────────

    def generate_roadmap(
        self,
        missing_skills: List[str],
        skill_gap_priority: List[Tuple[str, int]],
    ) -> Dict[str, List[str]]:
        """
        Convert prioritized missing skills into a phased learning roadmap.
        """
        priority_order = [s for s, _ in skill_gap_priority]
        sorted_missing = sorted(
            missing_skills,
            key=lambda s: priority_order.index(s) if s in priority_order else 999,
        )

        roadmap: Dict[str, List[str]] = {}
        idx = 0
        for phase_label, count in ROADMAP_PHASES:
            batch = sorted_missing[idx: idx + count]
            if not batch:
                break
            entries = []
            for skill in batch:
                resources = LEARNING_RESOURCES.get(
                    skill, ["Search official documentation", "Practice on LeetCode/Kaggle"]
                )
                entries.append(f"{skill.title()}|||{'; '.join(resources[:2])}")
            roadmap[phase_label] = entries
            idx += count

        return roadmap

    # ── 4. Resume Quality Review ──────────────────────────────────

    def review_resume(self, resume_text: str, resume_skills: Set[str]) -> List[str]:
        """Return actionable resume improvement suggestions."""
        suggestions = []
        text_lower = resume_text.lower()
        word_count = len(resume_text.split())

        if word_count < 200:
            suggestions.append(
                "Resume is very short (<200 words). Aim for 400-700 words for entry-level roles."
            )
        elif word_count > 900:
            suggestions.append(
                "Resume may be too long (>900 words). Keep to 1 page for <3 years of experience."
            )

        if not any(kw in text_lower for kw in ["github", "linkedin", "portfolio"]):
            suggestions.append(
                "Add GitHub and LinkedIn profile links — essential for tech recruiter screening."
            )

        quantifiers = ["%", "improved", "reduced", "increased", "optimized", "built", "led", "deployed"]
        if not any(kw in text_lower for kw in quantifiers):
            suggestions.append(
                "Quantify achievements: 'Reduced query latency by 32%', 'Built X serving 1K+ users'."
            )

        if len(resume_skills) < 8:
            suggestions.append(
                "Skill section is sparse. Explicitly list all languages, tools, and frameworks."
            )

        if "data structures" not in resume_skills and "algorithms" not in resume_skills:
            suggestions.append(
                "Add 'Data Structures & Algorithms' if practiced — critical keyword for SDE roles."
            )

        if not any(kw in text_lower for kw in ["project", "built", "developed", "implemented"]):
            suggestions.append(
                "Add a Projects section with concrete deliverables and tech stack."
            )

        if not suggestions:
            suggestions.append(
                "Resume structure looks solid. Focus on further quantifying impact."
            )

        return suggestions

    # ── 5. Dashboard Data ─────────────────────────────────────────

    def build_dashboard(
        self,
        resume_skills: Set[str],
        top_matches: List[JobMatch],
    ) -> Dict:
        """Aggregate data for the skill intelligence dashboard."""
        demand_rows = self._db.fetch_skill_demand(limit=10)
        all_demand = self._db.fetch_skill_demand(limit=50)

        marketable = [
            (row["skill"], row["demand_count"], row["avg_salary_lpa"])
            for row in all_demand
            if row["skill"] in resume_skills
        ]

        avg_match = round(sum(m.match_score for m in top_matches) / len(top_matches), 1) if top_matches else 0
        avg_ats = round(sum(m.ats_score for m in top_matches) / len(top_matches), 1) if top_matches else 0

        return {
            "resume_skill_count": len(resume_skills),
            "avg_match_score":    avg_match,
            "avg_ats_score":      avg_ats,
            "top_job_title":      top_matches[0].title if top_matches else "N/A",
            "top_job_score":      top_matches[0].match_score if top_matches else 0,
            "top_market_skills":  [(r["skill"], r["demand_count"], r["avg_salary_lpa"]) for r in demand_rows],
            "marketable_skills":  marketable[:8],
        }
