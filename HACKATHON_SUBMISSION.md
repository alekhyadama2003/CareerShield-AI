# CareerShield AI — Hackathon Submission

## One-Line Summary
CareerShield AI is a Python-native career intelligence system that analyzes resumes, matches candidates to job roles using weighted scoring, identifies skill gaps, and generates personalized learning roadmaps — built entirely with OOP, SQL/SQLite, and DSA, with no external APIs.

## Short Description (5 lines)
CareerShield AI is an AI-powered career guidance system built for students and early-career professionals. It extracts skills from resumes using a Trie-based NLP parser, matches them against a SQLite job database using a weighted scoring engine (required skills 70%, optional 30%), and ranks results using a MinHeap for O(n log k) efficiency. A SkillFrequencyMap (HashMap) aggregates skill gaps across top matches and feeds a phased learning roadmap with curated resources. The system runs fully offline — no APIs, no cloud — using only Python OOP, SQL, and DSA.

## Problem It Solves
Most students have no structured way to measure job readiness. CareerShield AI gives a resume-to-role compatibility score, ATS simulation, and a concrete, prioritized skill-learning plan — all from a single CLI command.

## Tech Stack
- Python (Class-based OOP — 8 classes)
- SQLite / DBMS (3-table relational schema with FK constraints and indexes)
- DSA: Trie (skill matching), MinHeap (job ranking), HashMap (gap frequency)
- No APIs. No internet. No frontend required.

## Key Technical Decisions
| Decision | Rationale |
|---|---|
| Trie for skill lookup | O(m) matching; extensible to prefix/fuzzy search |
| MinHeap for top-N jobs | O(n log k) vs O(n log n) sort — efficient for large job DBs |
| SQLite with FK + indexes | Proper DBMS design; index on job_skills(job_id) and skill columns |
| Weighted scoring (70/30) | Required skills dominate; optional skills differentiate candidates |
| Phased roadmap | Gap skills sorted by composite score: job frequency × market demand |

## What Makes It Different
- Pure Python — no ML libraries, no APIs, runs on any machine
- Proper DSA rationale documented in code (not just used for show)
- DBMS-grade schema: foreign keys, ON DELETE CASCADE, multi-column indexes
- ATS simulation mirrors real recruiter tool scoring logic
- Market salary + demand data enriches the roadmap prioritization
