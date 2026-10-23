# Pathweaver AI MVP

A Streamlit prototype that turns student learning history into an evidence-based skill profile, target-role gap analysis, and one practical next action.

## 1. Set up Python

Python 3.11 or 3.12 is recommended. Use a project virtual environment instead of Anaconda's `base` to avoid dependency conflicts.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 2. Configure a hosted model

```bash
cp .env.example .env
```

Edit `.env` with your hosted API key and model name. For another OpenAI-compatible provider, set `OPENAI_BASE_URL` to its documented API base URL. The provider must support chat completions; model names, quotas, and compatibility vary.

Never commit `.env` or share your API key.

## 3. Run

```bash
python -m streamlit run app.py
```

Open the local URL Streamlit prints, usually http://localhost:8501.

## MVP workflow

1. Paste courses, projects, tools, and experience.
2. Choose a target role.
3. Receive skills with evidence/confidence, prioritized gaps, and one achievable next action.

## Limitations and next steps

- Role expectations are general, not based on a live job listing yet.
- Model-generated skill levels and priorities are estimates; verify them.
- Submitted text is sent to your model provider. Avoid sensitive personal information.
- Next: add resume upload, a pasted job description, a skill graph, progress tracking, and tests.
# Pathweaver
