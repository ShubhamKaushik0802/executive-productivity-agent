# GitHub Upload Guide

**Candidate: Shubham Kaushik**

Create a repository called:

`executive-productivity-agent`

Upload the **contents of this project folder** so the repository root contains `app.py`, `README.md`, `requirements.txt`, `src/`, `data/`, `docs/`, etc.

Then run:

```bash
git init
git add .
git commit -m "Build executive productivity agent"
git branch -M main
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```

Do not commit `.env` or API keys. `.gitignore` already covers them.

The final repository should let a reviewer run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

The `demo.html` file is a fallback for a no-install browser walkthrough.
