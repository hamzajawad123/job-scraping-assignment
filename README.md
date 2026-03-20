# Public Job Market Trends Tracker (Selenium + Scrapy)

## 1. Project Overview
This project is a sophisticated data collection system designed for organizations that provide career guidance, bootcamps, and workforce planning. It simulates a production-grade environment by combining two powerful technologies:

- **Selenium**: Handles dynamic, JavaScript-heavy content and user-like interactions such as filtering and scrolling on job boards.
- **Scrapy**: Provides a scalable, high-speed framework for extracting structured data from individual job detail pages.

The goal is to analyze hiring trends, identify in-demand skills, and monitor entry-level opportunities across diverse public job sources.

---

## 2. Project Repository Structure
The project follows the exact hierarchy required for the assignment:

| Path | Purpose |
| ---- | ------- |
| `selenium/` | Browser automation scripts and helper utilities for link collection |
| `scrapy_project/` | Scrapy spiders, items, pipelines, and settings for deep parsing |
| `data/raw/` | Stores `jobs.csv` containing the initial URLs collected via Selenium |
| `data/final/` | Stores the final structured dataset in `jobs.json` or `jobs.csv` |
| `analysis/` | Python scripts and notebooks for summary metrics and trend charts |
| `docs/` | Short analytical report, assumptions, and setup documentation |
| `README.md` | Comprehensive project overview, setup, and usage guide |
| `.gitignore` | Excludes virtual environments, cache, and sensitive artifacts |

---

## 3. Setup and Installation

### Prerequisites
- Python 3.10+
- Google Chrome Browser (latest version)
- Git Bash (for Windows users)

### Installation Steps

1. **Clone the Repository**

git clone <your-repository-url>
cd JOB_SCRAPING_ASSIGNMENT


2. **Initialize Virtual Environment**

python -m venv venv


3. **Activate Virtual Environment**
- Windows Command Prompt:

venv\Scripts\activate

- Windows Git Bash / Linux / Mac:

source venv/Scripts/activate


4. **Install Dependencies**

pip install --upgrade pip
pip install selenium scrapy pandas webdriver-manager


---

## 4. Execution Workflow

### Phase 1: Link Extraction (Selenium)
Run the Selenium script to visit approved job boards (e.g., Vectara, Careem, NJP) and collect job detail links:


python selenium/link_extractor.py


**Output:** `data/raw/jobs.csv`

### Phase 2: Data Parsing (Scrapy)
Run the Scrapy spider to visit each job URL and extract structured data:


cd scrapy_project
scrapy crawl job_spider -o ../data/final/jobs.json


**Output:** `data/final/jobs.json`

---

## 5. Required Data Fields
Each record in the final dataset includes:

- **Job Title**: Exact posting title
- **Company Name**: Source company name
- **Location**: City, country, or remote/hybrid tags
- **Department**: Team (Engineering, Product, etc.)
- **Employment Type**: Full-time, contract, internship
- **Posted Date**: Publicly available posting date
- **Job URL**: Canonical detail page URL
- **Job Description**: Cleaned summary of the role
- **Required Skills**: Keyword-extracted skills (e.g., Python, SQL, Excel)

---

## 6. Git Branching Strategy
Professional team-based workflow:

- **main**: Stable, final submission version
- **develop**: Integration branch where all features are merged first
- **feature/\***: Task-specific branches (e.g., `feature/selenium-search`)
- **bugfix/\***: Fixes for parser or export issues
- **Release Tag**: Final submission tagged as `v1.0`

---

## 7. Compliance and Ethics
- **Public Access**: Only publicly available listings were scraped
- **No Login Bypass**: No authentication or private content accessed
- **Politeness**: `DOWNLOAD_DELAY = 1.5` seconds used to prevent server strain
- **Bot Protection**: No CAPTCHA solving or aggressive bypass
- **Data Integrity**: Personal candidate data never collected

---

## 8. Summary of Insights
Based on collected data:

- **Top Skills**: Python, SQL, Project Management
- **Top Regions**: Remote, Islamabad, Dubai
- **Entry-Level Count**: `[X]` positions identified
- **Common Departments**: Engineering, Product, Operations
- **Common Employment Types**: Full-time, Internship

---

## 9. Deliverables
The final submission includes:

- Selenium link collection scripts
- Scrapy spider and parser
- Raw job URLs dataset
- Final structured dataset
- Analysis scripts / notebooks
- Documentation (README.md, setup, assumptions)

---

## 10. Notes and Assumptions
- Some fields may be missing if not present on job boards
- Skills are extracted using keyword matching from job description
- Job availability reflects only the scraping period
- Selenium handles dynamic content with scrolling or waiting logic

---

## 11. Example Commands

**Run Selenium Collector**

python selenium/link_extractor.py


**Run Scrapy Spider**

cd scrapy_project
scrapy crawl job_spider -o ../data/final/jobs.json


**Export to CSV Instead of JSON**

cd scrapy_project
scrapy crawl job_spider -o ../data/final/jobs.csv


---

## 12. Conclusion
This project demonstrates how Selenium and Scrapy can be integrated to build a pra
