# 🧭 Pathweaver AI
### Turn Your Learning Into Your Next Opportunity

Pathweaver AI is an AI-powered career intelligence platform that transforms a student's learning history, projects, courses, and skills into an evidence-based career profile.

Instead of simply listing skills on a resume, Pathweaver helps learners understand what they know, identify potential gaps for their target career, and discover the next practical step toward their goals.

**Built for:** Hacktoberfest Hack Day — Open Source AI

---

## 💡 The Problem

Students learn through online courses, certifications, personal projects, tutorials, and experimentation. However, they often struggle to connect these experiences to the skills employers expect.

Common challenges include:

- Not knowing which skills they have actually demonstrated.
- Struggling to identify gaps between their current abilities and a target role.
- Feeling overwhelmed by lengthy learning roadmaps.
- Finding it difficult to decide what project or skill to work on next.

## 🚀 The Solution

Pathweaver AI converts unstructured learning experiences into actionable career intelligence.

Users provide their learning history and select a target career. The AI analyzes their input, identifies skills supported by evidence, highlights potential skill gaps, and recommends a practical next action.

### How It Works

1. **Share your journey:** Enter your projects, courses, certifications, learning experiences, and skills.
2. **Discover your skills:** Extract relevant skills and connect them to supporting evidence.
3. **Choose your destination:** Select a target role, such as Data Engineer or MLOps Engineer.
4. **Understand your gaps:** Compare demonstrated skills with the requirements of the target role.
5. **Take your next step:** Receive a focused recommendation to help close an important gap.

---

## ✨ Core Features

### 🧠 1. Skill Intelligence
Transform unstructured learning history into a structured skill profile.

- Extract relevant technical skills.
- Identify supporting evidence from user-provided information.
- Distinguish practical experience from course or tutorial exposure.
- Indicate confidence in extracted skills.

### 🎯 2. Career Gap Analysis
Understand how your demonstrated skills compare with your target role.

- Identify relevant existing skills.
- Highlight missing or insufficiently demonstrated skills.
- Explain why particular skills matter for the role.
- Help prioritize areas for improvement.

### 🚀 3. Next Best Action
Turn career insights into practical steps.

- Recommend a focused learning task or project.
- Connect the recommendation to an identified skill gap.
- Encourage learning through implementation rather than passive consumption.

### 🔮 Planned Features
- Persistent user profiles and progress tracking.
- Skill progression over time.
- Structured job-role requirement datasets.
- Personalized project recommendations.
- Exportable career-readiness reports.
- Integration with public job descriptions.

*Planned features are part of the roadmap and may not be implemented in the current MVP.*

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Interactive web interface |
| OpenRouter | Hosted AI model inference |
| OpenAI Python SDK | OpenAI-compatible API client |
| python-dotenv | Local environment configuration |

### Architecture

```text
          User
           |
           v
   Streamlit Interface
           |
           v
    Learning History
           |
           v
     AI Analysis
           |
           v
   OpenRouter API
           |
           v
    Structured Output
           |
           v
   +------------------+
   | Skill Intelligence|
   | Career Gap Analysis|
   | Next Best Action |
   +------------------+
           |
           v
    Actionable Insights
```

The application uses a hosted inference API, allowing AI analysis without requiring users to run a large language model locally.

---

## ⚙️ Getting Started

### Prerequisites

- Python 3.11 or a compatible Python version supported by the dependencies.
- Git.
- An internet connection.
- An OpenRouter API key.

### 1. Clone the Repository

```bash
git clone https://github.com/Manojv117/pathweaver-ai.git
cd pathweaver-ai
```

### 2. Create a Virtual Environment

On macOS or Linux:

```bash
python
