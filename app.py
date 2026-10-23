import json
import os
import re
from typing import Any

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# 1. CONFIGURATION
# ============================================================

load_dotenv()

st.set_page_config(
    page_title="Pathweaver AI",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# 2. CUSTOM UI STYLING
# ============================================================

st.markdown(
    """
    <style>
        :root {
            --pw-red: #e60023;
            --pw-red-pressed: #cc001f;
            --pw-ink: #000000;
            --pw-body: #33332e;
            --pw-muted: #62625b;
            --pw-ash: #91918c;
            --pw-canvas: #ffffff;
            --pw-soft: #fbfbf9;
            --pw-card: #f6f6f3;
            --pw-line: #dadad3;
            --pw-line-soft: #e5e5e0;
            --pw-success: #103c25;
            --pw-success-bg: #c7f0da;
        }
        html, body, [class*="css"] {
            font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }
        .stApp {
            background: var(--pw-soft);
            color: var(--pw-body);
        }
        [data-testid="stHeader"] {
            background: rgba(251, 251, 249, 0.92);
        }
        .block-container {
            max-width: 1120px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }
        .main-title {
            color: var(--pw-ink);
            font-size: clamp(2.15rem, 4vw, 3.1rem);
            font-weight: 780;
            letter-spacing: -1.5px;
            line-height: 1.12;
            margin-bottom: 0.4rem;
        }
        .subtitle {
            font-size: 1.05rem;
            color: var(--pw-muted);
            margin-bottom: 0.45rem;
            max-width: 720px;
            line-height: 1.55;
        }
        .section-heading {
            color: var(--pw-ink);
            font-size: 1.35rem;
            font-weight: 750;
            letter-spacing: -0.45px;
            margin-top: 0.15rem;
            margin-bottom: 0.5rem;
        }
        .skill-card {
            border: 1px solid var(--pw-line);
            border-radius: 16px;
            padding: 18px;
            margin-bottom: 12px;
            background: var(--pw-canvas);
        }
        .skill-name {
            color: var(--pw-ink);
            font-size: 1.05rem;
            font-weight: 700;
        }
        .muted-text {
            color: var(--pw-muted);
            font-size: 0.9rem;
        }
        div[data-testid="stMetric"] {
            background: var(--pw-canvas);
            border: 1px solid var(--pw-line);
            padding: 17px 18px;
            border-radius: 16px;
        }
        div[data-testid="stMetricLabel"] {
            color: var(--pw-muted);
            font-size: 0.9rem;
        }
        div[data-testid="stMetricValue"] {
            color: var(--pw-ink);
            font-weight: 800;
            letter-spacing: -0.6px;
        }
        div[data-testid="stForm"],
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-color: var(--pw-line) !important;
            border-radius: 20px !important;
        }
        div[data-testid="stForm"] {
            padding: 1.4rem 1.5rem 1.25rem;
            background: var(--pw-canvas);
        }
        div[data-testid="stButton"] button,
        div[data-testid="stFormSubmitButton"] button {
            border-radius: 16px;
            min-height: 2.8rem;
            font-weight: 700;
            transition: background-color 120ms ease, border-color 120ms ease;
        }
        div[data-testid="stButton"] button[kind="primary"],
        div[data-testid="stFormSubmitButton"] button[kind="primary"] {
            border: 1px solid var(--pw-red);
            color: #ffffff;
            background: var(--pw-red);
        }
        div[data-testid="stButton"] button[kind="primary"]:hover,
        div[data-testid="stFormSubmitButton"] button[kind="primary"]:hover {
            border-color: var(--pw-red-pressed);
            background: var(--pw-red-pressed);
            color: #ffffff;
        }
        div[data-testid="stButton"] button[kind="secondary"] {
            border: 1px solid var(--pw-line);
            color: var(--pw-ink);
            background: var(--pw-card);
        }
        /* Form labels and controls: strong contrast and consistent sizing */
        div[data-testid="stTextArea"] label,
        div[data-testid="stTextInput"] label,
        div[data-testid="stSelectbox"] label {
            color: #292923 !important;
            font-weight: 650 !important;
            font-size: 0.94rem !important;
            margin-bottom: 0.35rem !important;
        }
        div[data-testid="stTextArea"] textarea,
        div[data-testid="stTextInput"] input,
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            background: #ffffff !important;
            color: #292923 !important;
            border: 1px solid #d7d7cf !important;
            border-radius: 12px !important;
            min-height: 2.85rem;
        }
        div[data-testid="stTextArea"] textarea {
            min-height: 145px;
            line-height: 1.55;
        }
        div[data-testid="stTextArea"] textarea::placeholder,
        div[data-testid="stTextInput"] input::placeholder {
            color: #77776f !important;
            opacity: 1 !important;
        }
        div[data-testid="stTextArea"] textarea:focus,
        div[data-testid="stTextInput"] input:focus,
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within {
            border-color: var(--pw-red) !important;
            box-shadow: 0 0 0 2px rgba(230, 0, 35, 0.12) !important;
        }
        div[data-testid="stForm"] [data-testid="stMarkdownContainer"] p {
            margin-bottom: 0.6rem;
        }
        div[data-testid="stForm"] {
            gap: 0.8rem;
        }
        div[data-testid="stProgress"] > div {
            border-radius: 999px;
        }
        div[data-testid="stProgress"] div[role="progressbar"] > div {
            background: var(--pw-red);
        }
        div[data-testid="stExpander"] {
            border: 1px solid var(--pw-line);
            border-radius: 16px;
            background: var(--pw-canvas);
        }
        div[data-testid="stAlert"] {
            border-radius: 16px;
        }
        hr {
            border-color: var(--pw-line-soft);
        }
        .footer-text {
            color: var(--pw-muted);
            font-size: 0.85rem;
            text-align: center;
            margin-top: 2.5rem;
            padding-top: 1.25rem;
            border-top: 1px solid var(--pw-line);
        }
        @media (max-width: 768px) {
            .block-container {
                padding-top: 1rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }
            .main-title {
                letter-spacing: -1.1px;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 3. HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🧭 Pathweaver AI</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="subtitle">
        Turn your learning journey into an evidence-based career path.
    </div>
    """,
    unsafe_allow_html=True,
)

st.write(
    "Discover your current skills, identify gaps for your target role, "
    "and get one practical next step."
)


# ============================================================
# 4. OPENROUTER / OPENAI CLIENT
# ============================================================

def get_client() -> OpenAI:
    """Create an OpenAI-compatible client using environment variables."""

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    base_url = os.getenv(
        "OPENAI_BASE_URL",
        "https://openrouter.ai/api/v1",
    ).strip()

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is missing. Add your API key to your .env file."
        )

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
        timeout=90.0,
        max_retries=2,
    )

    return client


# ============================================================
# 5. AI ANALYSIS
# ============================================================

def analyze_journey(journey: str, role: str) -> dict[str, Any]:
    """
    Analyze the user's learning journey and return a structured
    career profile, evidenced skills, role gaps, and a next action.
    """

    client = get_client()

    model = os.getenv(
        "OPENAI_MODEL",
        "gpt-4o-mini",
    ).strip()

    system_prompt = """
You are Pathweaver AI, an evidence-based career development assistant.

Your job is to analyze a person's learning journey and compare it with
their target career role.

IMPORTANT RULES:
1. Use only information supported by the user's learning journey.
2. Never invent projects, qualifications, work experience, or skills.
3. Clearly distinguish demonstrated evidence from self-reported skills.
4. Do not claim that someone is proficient merely because they mention
   a technology.
5. If evidence is insufficient, acknowledge the uncertainty.
6. Recommend practical and achievable next steps appropriate to the
   user's current level.
7. Prioritize the most important skill gaps for the target role.
8. Do not treat every missing skill as a critical gap.
9. Recommend exactly one next action that can be completed in a
   manageable amount of time.
10. Do not assume the user has completed a project unless they say so.
11. Return valid JSON only. Do not use Markdown fences.

Return a JSON object with this exact structure:

{
  "profile_summary": "A concise summary of the user's demonstrated learning.",
  "skills": [
    {
      "name": "Python",
      "level": "Developing",
      "confidence": 0.8,
      "evidence": "The specific evidence supplied by the user",
      "evidence_type": "Project"
    }
  ],
  "role_fit_summary": "An honest explanation of the user's current fit.",
  "gaps": [
    {
      "skill": "Docker",
      "priority": "High",
      "reason": "Why this skill matters for the target role.",
      "prerequisite": "What to learn or understand first."
    }
  ],
  "next_action": {
    "title": "Build a small data pipeline",
    "why": "Why this is the best next step.",
    "steps": [
      "Step one",
      "Step two",
      "Step three"
    ],
    "success_evidence": "A concrete result that demonstrates completion.",
    "estimated_hours": 4
  }
}

FIELD REQUIREMENTS:

profile_summary:
- A concise and realistic summary.
- Must not invent experience.

skills:
- Maximum 8 skills.
- Only include skills supported by the supplied information.
- level must be one of: Beginner, Developing, Proficient.
- confidence must be a number between 0 and 1.
- evidence must identify the actual statement, project, course, or
  experience supporting the skill.
- evidence_type must be one of: Project, Course, Experience,
  Self-reported.
- Use Project only when the user describes actually building something.
- Use Course only when the user describes relevant coursework.
- Use Experience only when the user describes relevant experience.
- Use Self-reported when the user states a skill without stronger evidence.

role_fit_summary:
- Explain the current alignment with the target role.
- Be encouraging but honest.
- Do not invent a numerical employability score.

gaps:
- Maximum 5 gaps.
- priority must be High, Medium, or Low.
- Explain why each gap matters for the specified role.
- Recommend realistic prerequisites.
- Do not label a skill as missing if the user has already demonstrated it.

next_action:
- Recommend exactly one actionable task.
- steps must be a list of 3 to 6 clear steps.
- success_evidence must be measurable or verifiable.
- estimated_hours must be a positive number.
- If the user provides too little evidence, recommend a small diagnostic
  task instead of inventing a career profile.

Base all recommendations on the user's actual information and target role.
"""

    user_prompt = f"""
TARGET ROLE:
{role}

USER'S LEARNING JOURNEY:
{journey}

Analyze this journey for the specified target role.

Identify only skills supported by the information provided. Be transparent
about uncertainty and recommend the most useful next action.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError(
            "The AI provider returned an empty response. Please try again."
        )

    # Remove Markdown code fences if the provider adds them.
    content = content.strip()
    content = re.sub(r"^```(?:json)?\s*", "", content)
    content = re.sub(r"\s*```$", "", content)

    try:
        result = json.loads(content)
    except json.JSONDecodeError:
        # Attempt to recover a JSON object from surrounding text.
        start = content.find("{")
        end = content.rfind("}")

        if start == -1 or end == -1 or end <= start:
            raise ValueError(
                "The AI response was not valid JSON. Please try again."
            )

        try:
            result = json.loads(content[start:end + 1])
        except json.JSONDecodeError as exc:
            raise ValueError(
                "The AI returned malformed JSON. Please try again."
            ) from exc

    # Validate the essential response structure.
    required_keys = [
        "profile_summary",
        "skills",
        "role_fit_summary",
        "gaps",
        "next_action",
    ]

    missing_keys = [
        key for key in required_keys if key not in result
    ]

    if missing_keys:
        raise ValueError(
            f"The AI response is missing required fields: "
            f"{', '.join(missing_keys)}"
        )

    if not isinstance(result["skills"], list):
        raise ValueError("The skills field must be a list.")

    if not isinstance(result["gaps"], list):
        raise ValueError("The gaps field must be a list.")

    if not isinstance(result["next_action"], dict):
        raise ValueError("The next_action field must be an object.")

    action_keys = [
        "title",
        "why",
        "steps",
        "success_evidence",
        "estimated_hours",
    ]

    missing_action_keys = [
        key
        for key in action_keys
        if key not in result["next_action"]
    ]

    if missing_action_keys:
        raise ValueError(
            "The next action is missing fields: "
            + ", ".join(missing_action_keys)
        )

    return result


# ============================================================
# 6. CAREER PROFILE FORM
# ============================================================

with st.container(border=True):
    st.markdown(
        '<div class="section-heading">🎯 Build your career map</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "Tell us what you have learned, the projects you have built, "
        "and the role you want to pursue."
    )

    with st.form("career_profile_form"):

        history = st.text_area(
            "Your learning journey",
            height=150,
            placeholder=(
                "Example:\n"
                "I know Python basics and SQL joins. I built a small API "
                "that collected weather data and stored it in PostgreSQL. "
                "I used pandas to clean CSV files and recently started "
                "learning Docker.\n\n"
                "Mention your actual skills, projects, courses, and "
                "what you are currently learning."
            ),
        )

        role_choice = st.selectbox(
            "Choose your target role",
            [
                "Data Engineer",
                "MLOps Engineer",
                "Other",
            ],
        )

        custom_role = ""

        if role_choice == "Other":
            custom_role = st.text_input(
                "Enter your target role",
                placeholder="e.g. Machine Learning Engineer",
            )

        submitted = st.form_submit_button(
            "✨ Synthesize my path",
            type="primary",
            width="stretch",
        )


# ============================================================
# 7. PROCESS FORM SUBMISSION
# ============================================================

if submitted:

    if len(history.strip()) < 30:
        st.warning(
            "Please provide at least 30 characters describing your "
            "learning journey, skills, or projects."
        )

    else:
        target_role = (
            custom_role.strip()
            if role_choice == "Other"
            else role_choice
        )

        if not target_role:
            st.warning(
                "Please enter the target role you want to pursue."
            )

        else:
            try:
                with st.spinner(
                    "🧠 Analyzing your learning journey and career gaps..."
                ):
                    new_result = analyze_journey(
                        history.strip(),
                        target_role,
                    )

                # Store the result for subsequent Streamlit reruns.
                st.session_state["pw_result"] = new_result
                st.session_state["pw_role"] = target_role

                # Reset progress whenever a new career map is generated.
                st.session_state["pw_action_completed"] = False

                st.session_state["pw_history"] = history.strip()

                st.success(
                    "Your career map is ready!"
                )

            except Exception as exc:
                st.error(
                    "We couldn't generate your career map."
                )

                st.caption(
                    "Check your API configuration, model availability, "
                    "internet connection, and provider usage limits. "
                    "Your API key is not displayed."
                )

                with st.expander("Technical details"):
                    st.code(str(exc))


# ============================================================
# 8. DISPLAY CAREER MAP
# ============================================================

result = st.session_state.get("pw_result")
saved_role = st.session_state.get("pw_role")

if result:

    st.divider()

    # --------------------------------------------------------
    # PROFILE OVERVIEW
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-heading">🗺️ Your career map</div>',
        unsafe_allow_html=True,
    )

    st.caption(f"Target role: {saved_role}")

    st.info(
        result.get(
            "profile_summary",
            "No profile summary was returned.",
        )
    )

    skills = result.get("skills", [])
    gaps = result.get("gaps", [])

    high_priority_gaps = sum(
        1
        for gap in gaps
        if isinstance(gap, dict)
        and gap.get("priority") == "High"
    )

    metric_col1, metric_col2, metric_col3 = st.columns(3)

    with metric_col1:
        st.metric(
            "Skills identified",
            len(skills),
        )

    with metric_col2:
        st.metric(
            "Career gaps",
            len(gaps),
        )

    with metric_col3:
        st.metric(
            "High-priority gaps",
            high_priority_gaps,
        )

    # --------------------------------------------------------
    # SKILLS AND EVIDENCE
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-heading">🧠 Your skills and evidence</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "Each skill should be supported by information from your "
        "learning journey. Confidence indicates how strongly the "
        "provided information supports the identification."
    )

    if not skills:
        st.info(
            "No sufficiently supported skills were identified. "
            "Add more details about your actual learning or projects."
        )

    else:
        for index, skill in enumerate(skills, start=1):

            if not isinstance(skill, dict):
                continue

            skill_name = skill.get("name", "Unnamed skill")
            level = skill.get("level", "Unknown")
            evidence = skill.get(
                "evidence",
                "No evidence supplied.",
            )
            evidence_type = skill.get(
                "evidence_type",
                "Self-reported",
            )

            try:
                confidence = float(
                    skill.get("confidence", 0)
                )
            except (TypeError, ValueError):
                confidence = 0.0

            # Keep the confidence value within the valid range.
            confidence = max(0.0, min(1.0, confidence))

            with st.container(border=True):

                skill_col, level_col = st.columns(
                    [3, 1]
                )

                with skill_col:
                    st.markdown(
                        f"**{index}. {skill_name}**"
                    )

                with level_col:
                    st.caption(
                        f"Level: {level}"
                    )

                st.progress(
                    confidence,
                    text=(
                        f"Evidence confidence: "
                        f"{confidence:.0%}"
                    ),
                )

                st.markdown(
                    f"**Evidence type:** {evidence_type}"
                )

                st.write(
                    f"**Supporting evidence:** {evidence}"
                )

    # --------------------------------------------------------
    # TARGET ROLE FIT
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-heading">🎯 Your target-role alignment</div>',
        unsafe_allow_html=True,
    )

    st.write(
        result.get(
            "role_fit_summary",
            "No role-fit summary was returned.",
        )
    )

    # --------------------------------------------------------
    # CAREER GAPS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-heading">🚧 Skills to develop</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "Focus on the most relevant gaps first. You do not need "
        "to learn everything at once."
    )

    if not gaps:
        st.success(
            "No specific skill gaps were identified from the "
            "available evidence. Consider building a more advanced "
            "project to test your current skills."
        )

    else:
        priority_order = {
            "High": 0,
            "Medium": 1,
            "Low": 2,
        }

        sorted_gaps = sorted(
            gaps,
            key=lambda gap: priority_order.get(
                gap.get("priority", "Low"),
                3,
            ) if isinstance(gap, dict) else 3,
        )

        for gap in sorted_gaps:

            if not isinstance(gap, dict):
                continue

            priority = gap.get(
                "priority",
                "Not specified",
            )

            title = (
                f"{gap.get('skill', 'Unnamed skill')} "
                f"— {priority} priority"
            )

            with st.expander(title):

                st.write(
                    f"**Why it matters:** "
                    f"{gap.get('reason', 'Not specified.')}"
                )

                st.write(
                    f"**Prerequisite or starting point:** "
                    f"{gap.get('prerequisite', 'Not specified.')}"
                )

    # --------------------------------------------------------
    # VISUAL CAREER ROADMAP
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-heading">🗺️ Your visual roadmap</div>',
        unsafe_allow_html=True,
    )
    st.caption(
        "Follow the path from skills supported by your evidence, "
        "through the most relevant gaps, to one practical action and its proof of completion."
    )

    def _dot_text(value: Any, limit: int = 150) -> str:
        """Escape text for Graphviz labels and keep the graph readable."""
        text_value = " ".join(str(value or "").split())
        if len(text_value) > limit:
            text_value = text_value[: limit - 1].rstrip() + "…"
        return text_value.replace("\\", "\\\\").replace('"', '\\"')

    supported_skill_names = [
        str(skill.get("name", "")).strip()
        for skill in skills
        if isinstance(skill, dict) and str(skill.get("name", "")).strip()
    ]
    current_skills_label = ", ".join(supported_skill_names[:4]) or "Add more learning evidence"
    if len(supported_skill_names) > 4:
        current_skills_label += f" +{len(supported_skill_names) - 4} more"

    roadmap_priority = {"High": 0, "Medium": 1, "Low": 2}
    roadmap_gaps = sorted(
        [gap for gap in gaps if isinstance(gap, dict)],
        key=lambda gap: roadmap_priority.get(str(gap.get("priority", "Low")), 3),
    )
    gap_names = [
        f"{gap.get('skill', 'Skill gap')} ({gap.get('priority', 'Priority not set')})"
        for gap in roadmap_gaps[:3]
    ]
    gaps_label = ", ".join(gap_names) or "No specific gaps identified"

    roadmap_action = result.get("next_action", {})
    if not isinstance(roadmap_action, dict):
        roadmap_action = {}

    action_title = _dot_text(roadmap_action.get("title", "Choose your next action"), 90)
    success_label = _dot_text(
        roadmap_action.get("success_evidence", "Define a verifiable result"),
        130,
    )

    roadmap_dot = f'''
    digraph PathweaverRoadmap {{
        graph [
            rankdir=TB,
            bgcolor="transparent",
            pad="0.25",
            nodesep="0.42",
            ranksep="0.48",
            splines=ortho
        ];
        node [
            shape=box,
            style="rounded,filled",
            fontname="Arial",
            fontsize=11,
            margin="0.20,0.14",
            penwidth=1.2,
            color="#64748B",
            fontcolor="#262622"
        ];
        edge [
            color="#e60023",
            penwidth=1.8,
            arrowsize=0.8
        ];

        current [
            label="CURRENT SKILLS\\n{_dot_text(current_skills_label, 130)}",
            fillcolor="#f6f6f3",
            color="#dadad3"
        ];
        gaps_node [
            label="PRIORITY GAPS\\n{_dot_text(gaps_label, 130)}",
            fillcolor="#fff0f1",
            color="#e60023"
        ];
        next_node [
            label="YOUR NEXT ACTION\\n{action_title}",
            fillcolor="#e60023",
            color="#cc001f",
            fontcolor="#ffffff",
            penwidth=2
        ];
        success_node [
            label="SUCCESS EVIDENCE\\n{success_label}",
            fillcolor="#c7f0da",
            color="#b6ddc8"
        ];

        current -> gaps_node -> next_node -> success_node;
    }}
    '''

    with st.container(border=True):
        st.graphviz_chart(roadmap_dot, width="stretch")

    roadmap_col1, roadmap_col2 = st.columns([1, 1])
    with roadmap_col1:
        st.caption("🟢 Current skills are based on the evidence listed above.")
    with roadmap_col2:
        st.caption("🟠 Gaps are prioritized by the AI; verify them against your own goals.")

    # --------------------------------------------------------
    # INTERACTIVE SKILL-GAP EXPLORER
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-heading">🔎 Explore a skill gap</div>',
        unsafe_allow_html=True,
    )
    st.write(
        "Choose a gap to inspect its reason, prerequisite, suggested practice tasks, "
        "and starting resources."
    )

    if roadmap_gaps:
        gap_options = [
            f"{gap.get('skill', 'Skill gap')} · {gap.get('priority', 'Priority not set')} priority"
            for gap in roadmap_gaps
        ]
        selected_gap_label = st.selectbox(
            "Select a skill gap",
            options=gap_options,
            key="pw_selected_gap",
        )
        selected_gap_index = gap_options.index(selected_gap_label)
        selected_gap = roadmap_gaps[selected_gap_index]
        selected_gap_name = str(selected_gap.get("skill", "this skill")).strip()
        selected_gap_key = selected_gap_name.lower()

        # These are starting points, not a claim that the user has completed them.
        resource_catalog = [
            (
                ("sql", "postgres", "database"),
                "SQL and databases",
                "https://www.postgresql.org/docs/",
                "PostgreSQL documentation",
                [
                    "Write a query using filtering, grouping, and joins.",
                    "Load a small dataset and verify its row count.",
                    "Document one query and explain what it returns.",
                ],
            ),
            (
                ("python", "pandas"),
                "Python and data manipulation",
                "https://docs.python.org/3/tutorial/",
                "The Python tutorial",
                [
                    "Write a small script that reads structured data.",
                    "Validate missing values and unexpected data types.",
                    "Save the cleaned output and test the result.",
                ],
            ),
            (
                ("docker", "container"),
                "Docker and containers",
                "https://docs.docker.com/get-started/",
                "Docker getting started",
                [
                    "Create a minimal Dockerfile for a small application.",
                    "Build and run the container locally.",
                    "Record the command and verify the application output.",
                ],
            ),
            (
                ("orchestration", "airflow", "workflow", "scheduling"),
                "Workflow orchestration",
                "https://airflow.apache.org/docs/",
                "Apache Airflow documentation",
                [
                    "Split a pipeline into extract, transform, and load steps.",
                    "Define dependencies between the steps.",
                    "Run the workflow and inspect logs for a successful run.",
                ],
            ),
            (
                ("spark", "pyspark", "distributed"),
                "Distributed data processing",
                "https://spark.apache.org/docs/latest/",
                "Apache Spark documentation",
                [
                    "Load a dataset with Spark.",
                    "Apply at least one filter and aggregation.",
                    "Compare the output with a small known example.",
                ],
            ),
            (
                ("cloud", "aws", "azure", "gcp", "oci", "storage"),
                "Cloud fundamentals",
                "https://cloud.google.com/docs",
                "Google Cloud documentation",
                [
                    "Choose a small public dataset to store in a cloud bucket.",
                    "Document the access permissions and storage format.",
                    "Verify that the object can be read back successfully.",
                ],
            ),
            (
                ("testing", "quality", "validation", "reliability"),
                "Testing and data quality",
                "https://docs.pytest.org/en/stable/",
                "pytest documentation",
                [
                    "Define one valid input and one invalid input.",
                    "Write checks for schema, nulls, and duplicate records.",
                    "Run the checks and record the expected outcome.",
                ],
            ),
        ]

        matching_resource = next(
            (
                item for item in resource_catalog
                if any(keyword in selected_gap_key for keyword in item[0])
            ),
            None,
        )

        if matching_resource:
            _, resource_category, resource_url, resource_title, suggested_tasks = matching_resource
        else:
            resource_category = selected_gap_name
            resource_url = "https://roadmap.sh/"
            resource_title = "Roadmap.sh — explore learning paths"
            suggested_tasks = [
                f"Write down what you already know about {selected_gap_name}.",
                f"Complete one small practical exercise involving {selected_gap_name}.",
                "Save a verifiable artifact, such as code, notes, a query, or a short demo.",
            ]

        detail_col, task_col = st.columns([1, 1])
        with detail_col:
            with st.container(border=True):
                st.markdown(f"#### 🎯 {selected_gap_name}")
                st.markdown(f"**Priority:** {selected_gap.get('priority', 'Not specified')}")
                st.write(f"**Why it matters:** {selected_gap.get('reason', 'No reason was supplied.')}")
                st.write(
                    f"**Prerequisite / starting point:** "
                    f"{selected_gap.get('prerequisite', 'No prerequisite was supplied.')}"
                )
                st.markdown(f"**Starting resource:** [{resource_title}]({resource_url})")
                st.caption(
                    f"Resource category: {resource_category}. This is a suggested starting point; "
                    "choose resources appropriate to your level."
                )

        with task_col:
            with st.container(border=True):
                st.markdown("#### 🧩 Suggested practice tasks")
                for task_number, task in enumerate(suggested_tasks, start=1):
                    st.markdown(f"**{task_number}.** {task}")
                st.caption(
                    "These tasks are starter suggestions generated by Pathweaver's local resource guide, "
                    "not additional claims made by the AI about your experience."
                )
    else:
        st.success("No specific skill gaps were identified, so there is nothing to explore here.")

    # --------------------------------------------------------
    # NEXT-BEST ACTION
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-heading">🚀 Your next-best action</div>',
        unsafe_allow_html=True,
    )

    action = result.get("next_action", {})

    with st.container(border=True):

        st.subheader(
            action.get(
                "title",
                "Your next action",
            )
        )

        st.write(
            action.get(
                "why",
                "Complete this action to develop your skills.",
            )
        )

        estimated_hours = action.get(
            "estimated_hours",
            "Not specified",
        )

        st.caption(
            f"⏱️ Estimated time: {estimated_hours} hour(s)"
        )

        st.markdown("#### Steps to complete")

        steps = action.get("steps", [])

        if isinstance(steps, list) and steps:

            for step_number, step in enumerate(
                steps,
                start=1,
            ):
                st.markdown(
                    f"**{step_number}.** {step}"
                )

        else:
            st.write(
                "No detailed steps were returned. Review the action "
                "and break it into smaller tasks."
            )

        st.markdown("#### What success looks like")

        st.success(
            action.get(
                "success_evidence",
                "Produce a verifiable result demonstrating completion.",
            )
        )

    # --------------------------------------------------------
    # PROGRESS TRACKING
    # --------------------------------------------------------

    st.divider()

    st.markdown(
        '<div class="section-heading">📈 Your progress</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "Track your progress by completing the recommended action."
    )

    completed = st.checkbox(
        "✅ I've completed this action",
        key="pw_action_completed",
    )

    progress = 100 if completed else 0

    st.progress(
        progress,
        text=f"Action completion: {progress}%",
    )

    if completed:

        st.success(
            "🎉 Great work! You've marked this action as complete. "
            "Review the success criteria above to confirm your result."
        )

        st.info(
            "Ready for your next challenge? Generate a new career map "
            "to receive another recommended action."
        )

    else:

        st.info(
            "Your action is still in progress. Work through the steps "
            "above, check the success criteria, and mark it complete "
            "when you finish."
        )

    # --------------------------------------------------------
    # DEBUG INFORMATION
    # --------------------------------------------------------

    with st.expander("🔍 View raw JSON (debugging)"):

        st.json(result)

    # --------------------------------------------------------
    # PRIVACY NOTICE
    # --------------------------------------------------------

    st.caption(
        "Privacy: Your submitted learning journey is sent to the "
        "configured AI provider for analysis. Avoid including passwords, "
        "API keys, private records, or other sensitive information."
    )


# ============================================================
# 9. EMPTY STATE
# ============================================================

else:

    st.divider()

    st.markdown(
        '<div class="section-heading">✨ What Pathweaver AI does</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🧠 Discover")
        st.write(
            "Identify skills from your actual learning, courses, "
            "and projects."
        )

    with col2:
        st.markdown("### 🎯 Align")
        st.write(
            "Compare your current evidence with your target role "
            "and discover important gaps."
        )

    with col3:
        st.markdown("### 🚀 Progress")
        st.write(
            "Get one practical next action and track its completion."
        )

    st.info(
        "Enter your learning journey above and select "
        "'Synthesize my path' to get started."
    )


# ============================================================
# 10. FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer-text">
        Built with Streamlit and AI · Pathweaver AI
    </div>
    """,
    unsafe_allow_html=True,
)