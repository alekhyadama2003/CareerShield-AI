"""
CareerShield AI — database.py
Class: DatabaseManager
Handles SQLite schema creation, seeding, and all SQL queries.
Tech: Python OOP | SQL | DBMS
"""

import sqlite3
import os
from typing import List, Tuple, Optional


class DatabaseManager:
    """
    Manages all SQLite database operations for CareerShield AI.
    Encapsulates connection, schema creation, seeding, and queries.
    """

    DB_PATH = os.path.join(os.path.dirname(__file__), "data", "careerShield.db")

    def __init__(self):
        os.makedirs(os.path.dirname(self.DB_PATH), exist_ok=True)
        self._conn: Optional[sqlite3.Connection] = None

    # ── Connection Management ──────────────────────────────────────

    def connect(self) -> None:
        self._conn = sqlite3.connect(self.DB_PATH)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON")

    def disconnect(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *_):
        self.disconnect()

    @property
    def cursor(self) -> sqlite3.Cursor:
        if not self._conn:
            raise RuntimeError("DatabaseManager: call connect() first.")
        return self._conn.cursor()

    # ── Schema ────────────────────────────────────────────────────

    def create_schema(self) -> None:
        """Create all tables if they don't exist."""
        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS jobs (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                title            TEXT    NOT NULL,
                category         TEXT    NOT NULL,
                description      TEXT,
                experience_level TEXT    DEFAULT 'Entry'
            );

            CREATE TABLE IF NOT EXISTS job_skills (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id      INTEGER NOT NULL,
                skill       TEXT    NOT NULL,
                is_required INTEGER DEFAULT 1,
                FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS skill_demand (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                skill           TEXT    UNIQUE NOT NULL,
                demand_count    INTEGER DEFAULT 0,
                avg_salary_lpa  REAL    DEFAULT 0.0
            );

            CREATE INDEX IF NOT EXISTS idx_job_skills_job_id   ON job_skills(job_id);
            CREATE INDEX IF NOT EXISTS idx_job_skills_skill     ON job_skills(skill);
            CREATE INDEX IF NOT EXISTS idx_skill_demand_skill   ON skill_demand(skill);
        """)
        self._conn.commit()

    # ── Seeding ───────────────────────────────────────────────────

    def seed_if_empty(self) -> None:
        """Seed jobs and skill demand data only if tables are empty."""
        cur = self.cursor
        cur.execute("SELECT COUNT(*) FROM jobs")
        if cur.fetchone()[0] > 0:
            return
        self._seed_jobs()
        self._seed_skill_demand()
        self._conn.commit()

    def _seed_jobs(self) -> None:
        jobs = [
            ("Software Development Engineer", "Engineering", "Design scalable backend systems.", "Entry",
             ["python", "data structures", "algorithms", "sql", "git", "oop", "system design"],
             ["java", "c++", "kubernetes", "aws"]),

            ("Machine Learning Engineer", "AI/ML", "Build and deploy ML models.", "Mid",
             ["python", "machine learning", "deep learning", "numpy", "pandas", "sql", "git"],
             ["tensorflow", "pytorch", "mlops", "docker"]),

            ("Data Scientist", "Data", "Analyze datasets and build predictive models.", "Entry",
             ["python", "machine learning", "statistics", "pandas", "numpy", "sql", "data visualization"],
             ["r", "tableau", "spark", "deep learning"]),

            ("Data Analyst", "Data", "Transform data into business insights.", "Entry",
             ["sql", "excel", "data visualization", "python", "statistics"],
             ["tableau", "power bi", "pandas"]),

            ("Backend Developer", "Engineering", "Build RESTful APIs and server-side logic.", "Entry",
             ["python", "sql", "git", "oop", "dbms", "data structures"],
             ["docker", "flask", "django", "fastapi", "redis"]),

            ("AI/ML Research Intern", "AI/ML", "Prototype AI solutions.", "Intern",
             ["python", "machine learning", "numpy", "pandas", "algorithms"],
             ["deep learning", "tensorflow", "pytorch", "nlp"]),

            ("Database Administrator", "Data", "Design and maintain database systems.", "Entry",
             ["sql", "dbms", "data modeling", "indexing", "stored procedures"],
             ["mysql", "postgresql", "oracle", "mongodb"]),

            ("NLP Engineer", "AI/ML", "Build NLP models and pipelines.", "Mid",
             ["python", "nlp", "machine learning", "deep learning", "transformers"],
             ["pytorch", "huggingface", "spacy", "bert"]),

            ("Computer Vision Engineer", "AI/ML", "Develop image analysis systems.", "Mid",
             ["python", "deep learning", "computer vision", "opencv", "numpy"],
             ["pytorch", "tensorflow", "cuda", "yolo"]),

            ("QA / Test Engineer", "Engineering", "Design test plans, automate testing.", "Entry",
             ["python", "testing", "sql", "git", "debugging"],
             ["selenium", "pytest", "postman"]),

            ("Full Stack Developer", "Engineering", "Build end-to-end web applications.", "Mid",
             ["python", "javascript", "sql", "html", "css", "git"],
             ["react", "nodejs", "docker", "aws"]),

            ("Product Data Analyst", "Data", "Drive product decisions with data.", "Entry",
             ["sql", "python", "statistics", "data visualization", "excel"],
             ["tableau", "mixpanel", "looker"]),
        ]

        cur = self.cursor
        for title, category, desc, level, required, optional in jobs:
            cur.execute(
                "INSERT INTO jobs (title, category, description, experience_level) VALUES (?,?,?,?)",
                (title, category, desc, level)
            )
            job_id = cur.lastrowid
            for skill in required:
                cur.execute(
                    "INSERT INTO job_skills (job_id, skill, is_required) VALUES (?,?,1)",
                    (job_id, skill)
                )
            for skill in optional:
                cur.execute(
                    "INSERT INTO job_skills (job_id, skill, is_required) VALUES (?,?,0)",
                    (job_id, skill)
                )

    def _seed_skill_demand(self) -> None:
        data = [
            ("python", 142, 12.5), ("sql", 128, 9.8), ("machine learning", 98, 14.0),
            ("data structures", 90, 13.5), ("algorithms", 88, 13.2), ("git", 115, 10.0),
            ("deep learning", 75, 15.5), ("pandas", 80, 11.5), ("numpy", 78, 11.2),
            ("docker", 68, 13.0), ("aws", 72, 14.5), ("oop", 95, 10.5),
            ("system design", 60, 18.0), ("nlp", 45, 16.0), ("computer vision", 42, 16.5),
            ("kubernetes", 55, 15.0), ("tensorflow", 50, 14.8), ("pytorch", 52, 15.2),
            ("statistics", 65, 12.0), ("data visualization", 70, 10.8), ("dbms", 75, 9.5),
            ("linux", 60, 12.0), ("testing", 55, 9.0), ("debugging", 58, 9.2),
            ("excel", 62, 7.5), ("javascript", 88, 11.0), ("transformers", 40, 17.0),
            ("opencv", 35, 14.0), ("stored procedures", 45, 9.0), ("data modeling", 48, 10.0),
        ]
        self.cursor.executemany(
            "INSERT OR IGNORE INTO skill_demand (skill, demand_count, avg_salary_lpa) VALUES (?,?,?)",
            data
        )

    # ── Query Methods ─────────────────────────────────────────────

    def fetch_all_jobs(self) -> List[sqlite3.Row]:
        """Return all jobs: (id, title, category, description, experience_level)."""
        return self.cursor.execute(
            "SELECT id, title, category, description, experience_level FROM jobs ORDER BY id"
        ).fetchall()

    def fetch_job_skills(self, job_id: int) -> List[sqlite3.Row]:
        """Return all skills for a job: (skill, is_required)."""
        return self.cursor.execute(
            "SELECT skill, is_required FROM job_skills WHERE job_id = ?", (job_id,)
        ).fetchall()

    def fetch_skill_demand(self, limit: int = 20) -> List[sqlite3.Row]:
        """Return top-demand skills: (skill, demand_count, avg_salary_lpa)."""
        return self.cursor.execute(
            "SELECT skill, demand_count, avg_salary_lpa FROM skill_demand "
            "ORDER BY demand_count DESC LIMIT ?", (limit,)
        ).fetchall()

    def fetch_demand_for_skill(self, skill: str) -> int:
        """Return demand count for a specific skill."""
        row = self.cursor.execute(
            "SELECT demand_count FROM skill_demand WHERE skill = ?", (skill,)
        ).fetchone()
        return row["demand_count"] if row else 0

    # ── Bootstrap ─────────────────────────────────────────────────

    def bootstrap(self) -> None:
        """Connect, create schema, and seed data in one call."""
        self.connect()
        self.create_schema()
        self.seed_if_empty()
