# 🤝 LagosPropIQ Collaboration Guide

Welcome to **LagosPropIQ** — a collaborative data intelligence project focused on **analyzing and understanding the Lagos real estate market** using data-driven insights.

This guide provides clear instructions for interns and contributors to collaborate efficiently, maintain clean code, and ensure data consistency across the repository.

## 🗂️ Repository Overview

**Repository Name:** `LagosPropIQ`  
**Purpose:** To collect, clean, and analyze real estate data across Lagos from multiple online sources.  
**Primary Contributors:** Data Science & Data Analysis Interns  

## 🚀 Step 1: Cloning the Repository

Every contributor must first clone the repo before making changes.

```bash
# Clone the repository to your local system
git clone https://github.com/intellisenseCodez/LagosPropIQ.git

# Move into the project directory
cd LagosPropIQ
```

## 🌿 Step 2: Creating Your Working Branch

Each collaborators must work on a separate branch to avoid conflicts.
Use this naming convention:
feature/<name>-<task> (e.g., feature/john-doe-property-scraper)

```bash
# Create a new branch from the main branch
git checkout -b feature/john-doe-property-scraper
```

✅ **Always create your branch from** `main`.

❌ **Do not work directly on the** `main` **branch**.

## 💾 Step 3: Pulling Updates Before Working

Before starting new work, sync your local repo with the latest version of `main`:

```bash
git checkout main
git pull origin main
```

Then switch back to your branch:

```bash
git checkout <your-branch-name>
```

## 🧠 Step 4: Committing Your Work

- Use clear and meaningful commit messages.
- Good commit messages make it easy to track project progress.

**Format Examples:**

```bash
git add .
git commit -m "feat: add scraper for PropertyPro listings"
git commit -m "fix: clean duplicate entries in NigeriaPropertyCentre dataset"
git commit -m "docs: update collaboration guide"
```
## 🔄 Step 5: Pushing Your Branch to GitHub

Once your work is ready to share or review:

```bash
git push origin <your-branch-name>
```

## 🧩 Step 6: Creating a Pull Request (PR)

1. Go to GitHub → Open the repository.
2. Click **“Compare & Pull Request.”** to `develop` branch
3. Fill in details:
   - **Title****: Short and descriptive (e.g., “Added PropertyPro Scraper Script”)
   - **Description**: Briefly explain what your script does.
   - **Reviewer**: Assign the project lead or mentor.
4. Wait for review and approval before merging to main.

✅ **Do not merge your own PRs** unless given permission.


## 🧹 Step 7: Keeping Your Branch Up-to-Date

If your PR is pending and main has changed, rebase or merge the latest updates:

```bash
git checkout develop
git pull origin develop
git checkout <your-branch-name>
git merge main
```

Resolve any conflicts if prompted, then push again.

## 🗃️ Folder Structure

```bash
LagosPropIQ/
│
├── src/ 
│   ├── data/                     # All raw and processed data
│        ├── raw/                  # Uncleaned data from scraping
│        └── cleaned/              # Processed or validated datasets
│
|   ├── scripts/                  # Python or notebook scripts
│   ├── scraping/             # Web scraping scripts
│   ├── cleaning/             # Data cleaning & preprocessing scripts
│   └── analysis/             # Exploratory and summary analysis scripts
│
|   ├── notebooks/                # Jupyter notebooks for EDA or prototyping
│
├── docs/                     # Documentation, reports, and guidelines
│
├── requirements.txt          # List of required dependencies
└── README.md                 # Project overview and contribution guide
```

## 🧱 Best Practices

- Follow the branch naming convention strictly.
- Commit frequently with clear messages (e.g., “FEAT: Added scraper for PropertyPro.ng listings”).
- Always pull the latest changes before starting new work.
- Store large datasets in .gitignore if necessary.
- Document your code clearly with comments and docstrings.
- Collaborate and communicate updates via GitHub Issues or Pull Request comments.

## ⚙️ Tech Stack

- Python (BeautifulSoup, Selenium, Scrapy, Pandas)
- PostgreSQL / PostGIS for data storage
- Jupyter Notebook for exploration and reporting
- Git + GitHub for version control

## 💬 Communication

- All discussions should be on the GitHub Issues page.
- For urgent clarifications, contact the Project Lead.
- Use clear titles and tags for all issues and pull requests.







