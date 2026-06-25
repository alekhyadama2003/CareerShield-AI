"""
CareerShield AI — main.py
Class: CareerShieldApp (Orchestrator)
Wires all components together and exposes CLI.

Usage:
    python main.py                  # demo mode
    python main.py resume.pdf       # PDF resume
    python main.py resume.txt       # TXT resume
    python main.py --top 7          # show top 7 matches

Tech: Python OOP | SQL/SQLite | DSA (Trie, MinHeap, HashMap) | DBMS
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(__file__))

from database import DatabaseManager
from skill_extractor import SkillExtractor
from job_matcher import JobMatcher
from career_advisor import CareerAdvisor
from resume_reader import ResumeReader
from reporter import Reporter
from models import CareerReport


# ── Demo Resume ────────────────────────────────────────────────

DEMO_RESUME = """
Alekhya Reddy
B.Tech Computer Science & Engineering | LPU | 2022-2026
Email: alekhya@email.com  |  GitHub: github.com/alekhya  |  LinkedIn: linkedin.com/in/alekhya

SKILLS
Python, SQL, Machine Learning, Data Structures, Algorithms, OOP, DBMS,
NumPy, Pandas, Scikit-learn, NLP, Git, Agile, SDLC, Debugging, Testing

EXPERIENCE
Jr. Engineer Intern — High Flows IT Solutions Pvt. Ltd. | Jan 2026 – Present
- Developed IT Service Desk & Ticketing System (ITSD) using SQL Server and Python
- Optimized 15+ SQL queries reducing average query latency by 32%
- Participated in 6 Agile sprints, completing 94% of assigned story points
- Built stored procedures, triggers, and views for automated data workflows

PROJECTS
AI Claim Verifier — HackerRank Orchestrate Hackathon (June 2026)
- Built multi-modal damage-claim verification pipeline using Claude API (VLM)
- Implemented deterministic image quality checks via NumPy
- Added concurrency via ThreadPoolExecutor; reduced processing time by 45%
- Schema validation, disk caching, and evaluation metrics integrated

Animal Species Prediction — Capstone (Team Leader)
- Led team of 4 in ML classification pipeline for animal species prediction
- Implemented data preprocessing, feature engineering, model evaluation (Python/SQL)

ACHIEVEMENTS
- HackerRank Orchestrate Hackathon Participant (June 2026)

EDUCATION
B.Tech, CSE — Lovely Professional University | 2022-2026
"""


# ══════════════════════════════════════════════════════════════
# ORCHESTRATOR CLASS
# ══════════════════════════════════════════════════════════════

class CareerShieldApp:
    """
    Top-level orchestrator for CareerShield AI.
    Composes all subsystem classes and runs the full analysis pipeline.

    Components:
      DatabaseManager  — SQLite schema, seed, queries
      SkillExtractor   — Resume text → skill set (uses SkillTrie)
      JobMatcher       — Skills → ranked job matches (uses JobHeap)
      CareerAdvisor    — Gaps, roadmap, career recs (uses SkillFrequencyMap)
      ResumeReader     — PDF/TXT → plain text
      Reporter         — Renders CareerReport to terminal
    """

    def __init__(self):
        self._db = DatabaseManager()
        self._extractor = SkillExtractor()
        self._reader = ResumeReader()
        self._reporter = Reporter()

    def initialize(self) -> None:
        """Bootstrap database: connect, create schema, seed data."""
        print("Initializing CareerShield AI...")
        self._db.bootstrap()
        print("Database ready.\n")

    def run(self, resume_text: str, top_n: int = 5) -> CareerReport:
        """
        Full pipeline:
          1. Extract skills from resume text
          2. Match against job database
          3. Analyze gaps and build roadmap
          4. Generate career recommendations
          5. Build dashboard
          6. Review resume quality
        """
        # Step 1 — Skill Extraction (Trie-based)
        print("Extracting skills from resume...")
        resume_skills = self._extractor.extract(resume_text)
        skill_summary = self._extractor.categorize(resume_skills)
        print(f"  {len(resume_skills)} skills detected.\n")

        # Step 2 — Job Matching (MinHeap-based top-N)
        print("Matching against job database...")
        matcher = JobMatcher(self._db)
        top_matches = matcher.match(resume_skills, top_n=top_n)
        print(f"  Top {len(top_matches)} matches found.\n")

        # Step 3 — Career Analysis
        print("Running career analysis...")
        advisor = CareerAdvisor(self._db)
        missing_skills, skill_gap_priority = advisor.analyze_gaps(top_matches)
        roadmap = advisor.generate_roadmap(missing_skills, skill_gap_priority)
        career_recs = advisor.recommend_careers(resume_skills)
        dashboard = advisor.build_dashboard(resume_skills, top_matches)
        resume_suggestions = advisor.review_resume(resume_text, resume_skills)
        print("  Analysis complete.\n")

        return CareerReport(
            resume_skills=resume_skills,
            skill_summary=skill_summary,
            top_matches=top_matches,
            career_recommendations=career_recs,
            learning_roadmap=roadmap,
            skill_gap_priority=skill_gap_priority[:10],
            resume_suggestions=resume_suggestions,
            dashboard=dashboard,
        )

    def render(self, report: CareerReport) -> None:
        self._reporter.render(report)

    def shutdown(self) -> None:
        self._db.disconnect()


# ── CLI ───────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="CareerShield AI — Resume Analysis & Career Guidance"
    )
    parser.add_argument(
        "resume", nargs="?",
        help="Path to resume (.pdf or .txt). Omit to run demo."
    )
    parser.add_argument(
        "--top", type=int, default=5,
        help="Number of top job matches to display (default: 5)"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    app = CareerShieldApp()

    try:
        app.initialize()

        if args.resume:
            print(f"Loading resume: {args.resume}")
            resume_text = app._reader.load(args.resume)
            print(f"  Loaded — {len(resume_text.split())} words\n")
        else:
            print("No resume file provided. Running in DEMO mode.\n")
            resume_text = DEMO_RESUME

        report = app.run(resume_text, top_n=args.top)
        app.render(report)

    finally:
        app.shutdown()


if __name__ == "__main__":
    main()
parser.add_argument(
    "--demo",
    action="store_true",
    help="Run with built-in demo resume"
)