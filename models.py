"""
CareerShield AI — models.py
Data classes / models used across the system.
Tech: Python OOP (dataclasses)
"""

from dataclasses import dataclass, field
from typing import List, Set, Dict, Tuple


@dataclass
class JobMatch:
    """Holds the result of matching a resume against one job."""
    job_id: int
    title: str
    category: str
    experience_level: str
    match_score: float          # 0–100, weighted required/optional
    ats_score: float            # 0–100, ATS simulation score
    matched_skills: List[str]
    missing_required: List[str]
    missing_optional: List[str]
    total_required: int
    total_optional: int


@dataclass
class CareerReport:
    """Full output of the CareerShield AI analysis pipeline."""
    resume_skills: Set[str]
    skill_summary: Dict[str, List[str]]           # category → [skills]
    top_matches: List[JobMatch]
    career_recommendations: List[str]
    learning_roadmap: Dict[str, List[str]]        # phase → [skill + resource]
    skill_gap_priority: List[Tuple[str, int]]     # (skill, job_count)
    resume_suggestions: List[str]
    dashboard: Dict
