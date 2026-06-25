"""
CareerShield AI — reporter.py
Class: Reporter
Renders the CareerReport as a formatted terminal output.
Tech: Python OOP
"""

from models import CareerReport


class Reporter:
    """Renders CareerReport to terminal in a clean structured format."""

    WIDTH = 68

    # ── Public ────────────────────────────────────────────────────

    def render(self, report: CareerReport) -> None:
        self._header()
        self._dashboard(report)
        self._skill_summary(report)
        self._job_matches(report)
        self._career_recommendations(report)
        self._skill_gap(report)
        self._resume_review(report)
        self._learning_roadmap(report)
        self._market_intelligence(report)
        self._footer()

    # ── Internal Helpers ──────────────────────────────────────────

    def _div(self, char: str = "─") -> None:
        print(char * self.WIDTH)

    def _section(self, title: str) -> None:
        print()
        self._div("═")
        print(f"  {title}")
        self._div("═")

    def _bar(self, score: float, width: int = 20) -> str:
        filled = int(score / 100 * width)
        return f"[{'█' * filled}{'░' * (width - filled)}] {score}%"

    # ── Sections ─────────────────────────────────────────────────

    def _header(self) -> None:
        print()
        print("╔" + "═" * (self.WIDTH - 2) + "╗")
        title = "CareerShield AI — Career Intelligence Report"
        pad = (self.WIDTH - 2 - len(title)) // 2
        print("║" + " " * pad + title + " " * (self.WIDTH - 2 - pad - len(title)) + "║")
        print("╚" + "═" * (self.WIDTH - 2) + "╝")

    def _dashboard(self, report: CareerReport) -> None:
        self._section("SKILL INTELLIGENCE DASHBOARD")
        d = report.dashboard
        print(f"  Skills Detected     : {d['resume_skill_count']}")
        print(f"  Avg Match Score     : {d['avg_match_score']}%")
        print(f"  Avg ATS Score       : {d['avg_ats_score']}%")
        print(f"  Best Matching Role  : {d['top_job_title']}  ({d['top_job_score']}%)")
        print()
        print("  Your Marketable Skills (by market demand):")
        for skill, demand, salary in d["marketable_skills"]:
            bar = "▓" * (demand // 10)
            print(f"    {skill:<28} {bar:<14} {demand:>4} openings | ₹{salary:.1f} LPA")

    def _skill_summary(self, report: CareerReport) -> None:
        self._section("SKILLS EXTRACTED FROM RESUME")
        for category, skills in report.skill_summary.items():
            print(f"  [{category}]")
            # Wrap skills in lines of max ~60 chars
            line = "    "
            for i, skill in enumerate(skills):
                chunk = skill + (", " if i < len(skills) - 1 else "")
                if len(line) + len(chunk) > 64:
                    print(line.rstrip(", "))
                    line = "    " + chunk
                else:
                    line += chunk
            print(line.rstrip(", "))

    def _job_matches(self, report: CareerReport) -> None:
        self._section("TOP JOB ROLE MATCHES")
        for i, m in enumerate(report.top_matches, 1):
            print(f"\n  #{i}  {m.title}  [{m.experience_level}]")
            print(f"       Category  : {m.category}")
            print(f"       Match     : {self._bar(m.match_score)}")
            print(f"       ATS       : {self._bar(m.ats_score)}")
            if m.matched_skills:
                print(f"       Matched   : {', '.join(m.matched_skills[:6])}")
            if m.missing_required:
                print(f"       Missing ★ : {', '.join(m.missing_required[:5])}")
            if m.missing_optional:
                print(f"       Nice-to-H : {', '.join(m.missing_optional[:4])}")

    def _career_recommendations(self, report: CareerReport) -> None:
        self._section("CAREER PATH RECOMMENDATIONS")
        for rec in report.career_recommendations:
            print(f"  ➤  {rec}")

    def _skill_gap(self, report: CareerReport) -> None:
        self._section("SKILL GAP ANALYSIS  (Priority → Learning Impact)")
        print(f"  {'#':<3} {'Skill':<30} {'Missing From':>13}  {'Priority':>8}")
        self._div()
        for rank, (skill, count) in enumerate(report.skill_gap_priority[:8], 1):
            urgency = "HIGH" if count >= 3 else "MEDIUM" if count >= 2 else "LOW"
            print(f"  {rank:<3} {skill:<30} {count:>8} jobs    {urgency:>8}")

    def _resume_review(self, report: CareerReport) -> None:
        self._section("RESUME QUALITY REVIEW")
        for s in report.resume_suggestions:
            print(f"  [!]  {s}")

    def _learning_roadmap(self, report: CareerReport) -> None:
        self._section("PERSONALIZED LEARNING ROADMAP")
        for phase, items in report.learning_roadmap.items():
            print(f"\n  ◆ {phase}")
            for item in items:
                skill, resources = item.split("|||", 1)
                print(f"      • {skill}")
                for res in resources.split("; "):
                    print(f"          → {res}")

    def _market_intelligence(self, report: CareerReport) -> None:
        self._section("MARKET INTELLIGENCE — TOP SKILLS IN DEMAND")
        print(f"  {'Skill':<28}  {'Openings':>8}  {'Avg Salary':>10}  {'Status'}")
        self._div()
        for skill, demand, salary in report.dashboard["top_market_skills"]:
            status = "✔ You have this" if skill in report.resume_skills else ""
            print(f"  {skill:<28}  {demand:>8}  ₹{salary:>7.1f} LPA  {status}")

    def _footer(self) -> None:
        print()
        print("╔" + "═" * (self.WIDTH - 2) + "╗")
        msg = "CareerShield AI — Built with Python | SQL | DSA | OOP"
        pad = (self.WIDTH - 2 - len(msg)) // 2
        print("║" + " " * pad + msg + " " * (self.WIDTH - 2 - pad - len(msg)) + "║")
        print("╚" + "═" * (self.WIDTH - 2) + "╝")
        print()
