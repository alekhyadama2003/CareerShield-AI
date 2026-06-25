# 🛡️ CareerShield AI

> **AI-powered career intelligence system — Resume analysis, job matching, skill gap identification, and personalized learning roadmaps.**

Built with **Python (OOP)** · **SQL / SQLite (DBMS)** · **DSA (Trie, MinHeap, HashMap)**

---

## 🧠 Problem Statement

Students and early-career professionals struggle to:
- Understand how well their resume matches real job roles
- Identify missing skills clearly and prioritize what to learn next
- Get structured, actionable career guidance without expensive tools

CareerShield AI solves this with a fully offline, Python-native career intelligence pipeline.

---

## ⚙️ Key Features

| Module | What It Does |
|---|---|
| **Resume Skill Extractor** | Extracts skills from PDF/TXT resumes using rule-based NLP + Trie matching |
| **Job Matching Engine** | Weighted scoring (required 70% / optional 30%) ranked via MinHeap |
| **ATS Score Analyzer** | Simulates Applicant Tracking System logic against job keywords |
| **Career Recommendation Engine** | Maps your skills to career paths with alignment percentages |
| **Skill Gap Analyzer** | Identifies missing required skills across top job matches |
| **Learning Roadmap Generator** | Converts skill gaps into phased, resource-linked study plans |
| **Skill Intelligence Dashboard** | Shows marketable skills, demand counts, and salary benchmarks |
| **Resume Quality Review** | Flags structural issues and suggests ATS improvements |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│          main.py (CLI)              │
│       CareerShieldApp               │  ← Orchestrator (OOP)
└──────────────┬──────────────────────┘
               │
    ┌──────────┼──────────────────┐
    ▼          ▼                  ▼
ResumeReader  SkillExtractor   DatabaseManager
 (.pdf/.txt)  (Trie — DSA)    (SQLite / DBMS)
                  │                  │
                  ▼                  ▼
            JobMatcher ◄─────── job_skills
           (MinHeap — DSA)     (SQL JOIN)
                  │
                  ▼
           CareerAdvisor
         (SkillFrequencyMap)
          - gap analysis
          - career recs
          - learning roadmap
                  │
                  ▼
             Reporter
         (terminal output)
```

---

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.9+ |
| Paradigm | Object-Oriented Programming (OOP) — 8 classes |
| Database | SQLite via `sqlite3` (standard library) |
| DSA | Trie (skill lookup), MinHeap (job ranking), HashMap (gap frequency) |
| PDF Parsing | `pdfplumber` / `PyPDF2` (optional) |
| No APIs | Fully offline, no external services |

---

## 📁 Project Structure

```
careerShield/
├── main.py              # CLI entry point + CareerShieldApp orchestrator
├── database.py          # DatabaseManager — SQLite schema, seed, queries
├── skill_extractor.py   # SkillExtractor — Trie-based NLP skill extraction
├── dsa.py               # SkillTrie, JobHeap, SkillFrequencyMap (DSA)
├── job_matcher.py       # JobMatcher — weighted scoring + ATS simulation
├── career_advisor.py    # CareerAdvisor — gaps, roadmap, recommendations
├── resume_reader.py     # ResumeReader — PDF/TXT loading
├── reporter.py          # Reporter — terminal report renderer
├── models.py            # JobMatch, CareerReport dataclasses
├── requirements.txt
└── data/
    └── careerShield.db  # SQLite database (auto-created on first run)
```

---

## 🚀 Setup & Run

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/careerShield-ai.git
cd careerShield-ai
```

### 2. Install dependencies (PDF support only)
```bash
pip install pdfplumber PyPDF2
```
> Core functionality requires **zero third-party packages** (uses Python stdlib only).

### 3. Run demo mode
```bash
python main.py
```

### 4. Run with your resume
```bash
python main.py resume.pdf
python main.py resume.txt
python main.py resume.pdf --top 7    # show top 7 job matches
```

---

## 🗄️ Database Schema

```sql
-- Jobs table
CREATE TABLE jobs (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    title            TEXT NOT NULL,
    category         TEXT NOT NULL,
    description      TEXT,
    experience_level TEXT DEFAULT 'Entry'
);

-- Job skills with required/optional flag
CREATE TABLE job_skills (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id      INTEGER NOT NULL,
    skill       TEXT NOT NULL,
    is_required INTEGER DEFAULT 1,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
);

-- Market demand intelligence
CREATE TABLE skill_demand (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    skill           TEXT UNIQUE NOT NULL,
    demand_count    INTEGER DEFAULT 0,
    avg_salary_lpa  REAL DEFAULT 0.0
);
```

---

## 🧩 DSA Components

### SkillTrie — `dsa.py`
- **Purpose:** O(m) skill lookup and prefix matching (m = skill character length)
- **Why not a set?** Supports future prefix/fuzzy matching; deterministic for multi-word skills
- **Operations:** `insert()`, `search()`, `starts_with()`, `all_skills()` (DFS)

### JobHeap — `dsa.py`
- **Purpose:** Maintain top-N job matches in O(n log k) — better than sorting all jobs O(n log n) when k ≪ n
- **Implementation:** Python `heapq` min-heap; ejects weakest match when size exceeds capacity

### SkillFrequencyMap — `dsa.py`
- **Purpose:** Count how many top job matches each missing skill appears in
- **Implementation:** HashMap (`dict`) + `heapq.nlargest` for top-k extraction

---

## 📊 Sample Output

```
╔══════════════════════════════════════════════════════════════════╗
║           CareerShield AI — Career Intelligence Report           ║
╚══════════════════════════════════════════════════════════════════╝

  Skills Detected     : 22
  Avg Match Score     : 67.5%
  Avg ATS Score       : 74.6%
  Best Matching Role  : AI/ML Research Intern  (77.5%)

  #1  AI/ML Research Intern  [Intern]
       Match     : [███████████████░░░░░] 77.5%
       ATS       : [████████████████░░░░] 82.2%
       Matched   : python, machine learning, numpy, pandas, algorithms, nlp
       Nice-to-H : deep learning, tensorflow, pytorch
```

---

## 👤 Author

**Alekhya Reddy**
B.Tech CSE — Lovely Professional University | 2022–2026
Jr. Engineer Intern — High Flows IT Solutions Pvt. Ltd.

---

## 📄 License

MIT License
