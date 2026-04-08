# Resume Analyzer API — Project Context Document
> Paste this at the start of any new chat so Claude is instantly up to speed.

---

## 🧠 Who I Am
- Name: Koras Koirala (GitHub: @koras7)
- Course: CS 3321 — Introduction to Software Engineering, Idaho State University, Spring 2026
- Instructor: Ryan Davis
- I am using Claude as my primary AI assistant throughout this project

---

## 👥 My Team
| Name | GitHub | Role |
|---|---|---|
| Bektur Akkabakov | @akkabakovb | Team Lead, repo owner, /analyze endpoint |
| Koras Koirala | @koras7 | /roles endpoint, endpoint improvements |
| Deepan | - | /roles endpoint |
| Himanshu Jha | @himanshujha05 | /analyze endpoint |

---

## 📦 The Project
**Name:** Resume Analyzer API
**Repo:** https://github.com/akkabakovb/Resume_Scanner_SoftwareEngineering
**Type:** Backend only REST API — no frontend
**Framework:** FastAPI + Python 3.14
**Package Manager:** uv
**AI Provider:** OpenAI (gpt-4o-mini)

---

## 🎯 What The Project Does
An AI-powered resume analysis API with two core features:

1. **Resume Analysis** — User submits a resume (PDF or plain text), API returns:
   - Overall quality score (0-100)
   - Strengths (list)
   - Weaknesses (list)
   - Key skills (list)
   - Improved professional summary
   - Career recommendation

2. **Job Role Matching** — User submits a resume (PDF or plain text), API returns top 3 matching job roles each with:
   - Job title
   - Reason why it fits
   - Match score (0-100)
   - Key skills that match

---

## 📡 Current API Endpoints
| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | API status check |
| GET | `/` | Root |
| POST | `/analyze` | PDF resume → full structured analysis |
| POST | `/analyze/text` | Plain text resume → full structured analysis |
| POST | `/roles` | PDF resume → top 3 matching job roles |
| POST | `/roles/text` | Plain text resume → top 3 matching job roles |

---

## 🏗 Project Architecture
```
Client (Postman / curl / test script)
    ↓
FastAPI Application (Python + uv)
    ↓
┌─────────────────────────────────┐
│  POST /analyze  POST /roles     │
│  POST /analyze/text             │
│  POST /roles/text               │
└─────────────────────────────────┘
    ↓
Resume Parser Service
(pdfplumber for PDF, plain text direct)
    ↓
OpenAI Service (gpt-4o-mini)
    ↓
OpenAI API (3rd party)

Supporting:
- Doppler → Secrets management
- Docker → Containerization
- AWS → Cloud deployment
- GitHub Actions → CI/CD
```

---

## 📁 Project Structure
```
Resume_Scanner_SoftwareEngineering/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py          # Pydantic models
│   └── routers/
│       ├── __init__.py
│       ├── analyze.py          # /analyze endpoints
│       └── roles.py            # /roles endpoints
├── main.py                     # FastAPI entry point
├── pyproject.toml              # dependencies
├── uv.lock                     # locked deps
├── .env                        # secrets (never committed)
├── .gitignore
├── .python-version
└── README.md
```

---

## 🛠 Tech Stack
- Language: Python 3.14
- Framework: FastAPI
- Package Manager: uv
- AI: OpenAI gpt-4o-mini
- PDF Parsing: PyMuPDF (fitz) + pdfplumber
- Validation: Pydantic
- Secrets: Doppler + GitHub Secrets
- Testing: PyTest + pytest-cov
- Container: Docker + Docker Hub
- Cloud: AWS
- CI/CD: GitHub Actions

---

## 🌿 Branching Strategy
- `master` — production ready, never commit directly
- Always create feature branches: `git checkout -b feature/your-feature`
- Always open a Pull Request before merging
- Branches so far:
  - `feature/roles-endpoint` — built /roles
  - `feature/analyze-endpoint` — built /analyze
  - `feature/improve-endpoints` — improved both endpoints
  - `feature/readme` — added README

---

## ✅ What's Done
- [x] Project setup with uv and FastAPI
- [x] API architecture designed
- [x] POST /analyze — PDF resume analysis (structured JSON)
- [x] POST /analyze/text — plain text analysis
- [x] POST /roles — PDF job role matching with match_score and key_skills
- [x] POST /roles/text — plain text job matching
- [x] GET /health — health check
- [x] Pydantic schemas for all requests and responses
- [x] OpenAI integration with gpt-4o-mini
- [x] PDF parsing with PyMuPDF and pdfplumber
- [x] PDF file type validation
- [x] Proper error handling (400 and 500 errors)
- [x] GitHub Project board with tickets
- [x] Professional README with Mermaid architecture diagram
- [x] Clean branching and PR workflow

---

## 📋 What's Coming Next (In Order)
1. **Unit Tests** — PyTest for all endpoints, mock OpenAI calls
2. **80% Code Coverage** — pytest-cov
3. **Linting** — Ruff or Flake8
4. **Secrets Management** — Doppler + GitHub Secrets
5. **Docker** — Dockerfile, docker build, docker run, push to Docker Hub
6. **AWS Deployment** — Deploy Docker container to AWS
7. **GitHub Actions CI/CD** — 3 jobs: Test → Build → Deploy
8. **Extra Credit** — 4th GitHub Actions job (something special)
9. **Final Presentation** — April 27, 10 minutes, live demo

---

## 🏆 Final Presentation Rubric (100 points)
| Item | Points |
|---|---|
| Live demo with 3rd party API working | +15 |
| Running on AWS | +15 |
| Running in Docker | +20 |
| Secrets in Doppler | +10 |
| Unit tests + 80% coverage | +15 |
| GitHub Actions (3 jobs) | +15 |
| PowerPoint presentation | +10 |
| **Extra credit** (4th GitHub Action) | +10 |
| **Auto -15 if secrets exposed** | -15 |

---

## ⚠️ Important Rules
- NEVER commit `.env` to GitHub — auto -15 points on presentation
- NEVER hardcode API keys in code
- Always activate venv: `source .venv/bin/activate`
- Always pull before working: `git pull origin master`
- Run app: `uv run uvicorn main:app --reload`
- API docs: `http://localhost:8000/docs`
- If `uv.lock` conflicts: delete it and run `uv sync`

---

## 💬 How I Work With Claude
- I share updates from my team Discord and Claude helps me understand and plan
- Claude helps me design architecture and plan before coding
- I use Claude Code in CLI to actually write the code
- Claude reviews code before I accept it
- We update the architecture and plans as the team makes decisions
- Claude keeps track of what's done and what's coming next
