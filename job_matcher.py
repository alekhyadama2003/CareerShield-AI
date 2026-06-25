"""
CareerShield AI — job_matcher.py
Class: JobMatcher
Matches resume skills against job database using weighted scoring.
Uses JobHeap (DSA) for O(n log k) top-N extraction.
Tech: Python OOP | DSA (Min-Heap) | SQL
"""

from typing import List, Set, Tuple
from database import DatabaseManager
from dsa import JobHeap
from models import JobMatch


class JobMatcher:
    """
    Matches a candidate's skill set against all jobs in the DB.
    Produces weighted match scores and ATS scores.

    Scoring weights:
      Required skills : 70%
      Optional skills : 30%
    """

    REQUIRED_WEIGHT = 70.0
    OPTIONAL_WEIGHT = 30.0

    def __init__(self, db: DatabaseManager):
        self._db = db

    # ── Public API ────────────────────────────────────────────────

    def match(self, resume_skills: Set[str], top_n: int = 5) -> List[JobMatch]:
        """
        Match resume against all jobs. Return top-N ranked results.
        Uses JobHeap (min-heap) for O(n log k) efficiency.
        """
        resume_lower = {s.lower() for s in resume_skills}
        heap = JobHeap(capacity=top_n)

        for job_row in self._db.fetch_all_jobs():
            job_id = job_row["id"]
            skills_rows = self._db.fetch_job_skills(job_id)

            required = [r["skill"] for r in skills_rows if r["is_required"] == 1]
            optional = [r["skill"] for r in skills_rows if r["is_required"] == 0]

            match_score, matched, miss_req, miss_opt = self._compute_match_score(
                resume_lower, required, optional
            )
            ats_score = self._compute_ats_score(
                resume_lower, required, optional, match_score
            )

            job_match = JobMatch(
                job_id=job_id,
                title=job_row["title"],
                category=job_row["category"],
                experience_level=job_row["experience_level"],
                match_score=match_score,
                ats_score=ats_score,
                matched_skills=matched,
                missing_required=miss_req,
                missing_optional=miss_opt,
                total_required=len(required),
                total_optional=len(optional),
            )
            heap.push(match_score, ats_score, job_id, job_match)

        return heap.top_n()

    # ── Scoring Logic ─────────────────────────────────────────────

    def _compute_match_score(
        self,
        resume_lower: Set[str],
        required: List[str],
        optional: List[str],
    ) -> Tuple[float, List[str], List[str], List[str]]:
        """
        Weighted match score:
          required_score = (matched_req / total_req) * 70
          optional_score = (matched_opt / total_opt) * 30
        """
        matched_req = [s for s in required if s in resume_lower]
        missing_req = [s for s in required if s not in resume_lower]
        matched_opt = [s for s in optional if s in resume_lower]
        missing_opt = [s for s in optional if s not in resume_lower]

        req_score = (len(matched_req) / len(required) * self.REQUIRED_WEIGHT) if required else 0.0
        opt_score = (len(matched_opt) / len(optional) * self.OPTIONAL_WEIGHT) if optional else 0.0

        score = round(req_score + opt_score, 1)
        return score, matched_req + matched_opt, missing_req, missing_opt

    def _compute_ats_score(
        self,
        resume_lower: Set[str],
        required: List[str],
        optional: List[str],
        match_score: float,
    ) -> float:
        """
        ATS simulation:
          keyword_density  = hits / total_keywords * 40
          required_coverage = matched_req / total_req * 40
          completeness      = match_score / 100 * 20
        """
        all_keywords = required + optional
        if not all_keywords:
            return 0.0

        hits = sum(1 for s in all_keywords if s in resume_lower)
        keyword_density = (hits / len(all_keywords)) * 40.0

        req_coverage = (
            (sum(1 for s in required if s in resume_lower) / len(required) * 40.0)
            if required else 0.0
        )
        completeness = (match_score / 100.0) * 20.0

        return round(min(keyword_density + req_coverage + completeness, 100.0), 1)
