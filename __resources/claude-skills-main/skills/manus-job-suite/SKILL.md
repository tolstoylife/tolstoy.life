---
name: manus-job-suite
description: Multi-board job search (Adzuna/USAJobs/100+ boards), AI resume matching, career advising, interview coaching (STAR method), salary estimation (BLS data), and Excel export. 15 job tool plugins with fallback chains.
allowed-tools: Read, Bash, Grep, Glob
---

# Manus Job Search Suite

Full job search and career platform in `~/manus-chatbot/agents/`.

## 4 Specialized Agents

| Agent | File | Capabilities |
|-------|------|-------------|
| JobSearchAgent | `job_search_agent.py` | Multi-board search, location intelligence, HF-powered matching |
| EnhancedJobSearchAgent | `enhanced_job_search_agent.py` | 20-tool integration, multiple resumes, Excel export |
| CareerAdvisorAgent | `career_advisor_agent.py` | Career path planning, skill gap analysis, salary progression |
| InterviewCoachAgent | `interview_coach_agent.py` | Mock interviews, STAR method, company-specific prep |
| ResumeWriterAgent | `resume_writer_agent.py` | AI resume creation, ATS optimization, skill extraction |

## 15 Job Tool Plugins (`agents/job_tools/`)

| Tool | API | Cost |
|------|-----|------|
| `adzuna_tool` | Adzuna (100+ boards) | Free tier |
| `usajobs_tool` | USAJobs federal jobs | FREE |
| `bls_tool` | Bureau of Labor Statistics | FREE |
| `onet_tool` | O*NET occupations/skills | FREE |
| `pypdf_tool` | PDF resume extraction | FREE |
| `spacy_tool` | NLP resume/JD parsing | FREE |
| `skills_ontology_tool` | Skills taxonomy | FREE |
| `salary_estimator` | Multi-source salary data | FREE |
| `resume_matcher_tool` | Semantic resume-job match | FREE |
| `qualification_analyzer` | Qualification gap analysis | FREE |
| `company_site_finder` | Career page URL discovery | FREE |
| `excel_exporter` | Formatted Excel export | FREE |

## API Access

```bash
# Job search
curl -X POST http://localhost:8000/api/v1/chat/message \
  -d '{"message": "Find remote Python developer jobs in Florida", "agent": "job_search"}'

# Career advice
curl -X POST http://localhost:8000/api/v1/chat/message \
  -d '{"message": "What skills should I learn to transition from QA to DevOps?"}'
```
