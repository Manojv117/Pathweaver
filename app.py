import json
import os
from typing import Any

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
st.set_page_config(page_title="Pathweaver AI", page_icon="🧭", layout="wide")
st.title("🧭 Pathweaver AI")
st.caption("Turn your learning journey into an evidence-based next step.")

with st.container(border=True):
    st.subheader("Build your career map")
    st.write("Describe what you've learned and built. Pathweaver will extract skills, compare them with your target role, and recommend one practical next action.")
    with st.form("career_profile_form"):
        history = st.text_area(
            "Your learning journey", height=220,
            placeholder="Example: I know Python basics and SQL joins. I built a small API that collected weather data and stored it in PostgreSQL. I used pandas to clean CSV files and recently started learning Docker..."
        )
        target_role = st.text_input("Target role", value="Data Engineer")
        submitted = st.form_submit_button("Synthesize my path", type="primary", use_container_width=True)

def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    base_url = os.getenv("OPENAI_BASE_URL", "").strip()

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is missing.")

    kwargs = {"api_key": api_key}
    if base_url:
        kwargs["base_url"] = base_url

    return OpenAI(**kwargs)

def analyze_journey(journey: str, role: str) -> dict:
    client = get_client()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
    system_prompt = """
You are Pathweaver AI, a careful career-skills analyst. Use only evidence in the user's journey.
Do not claim a skill unless supported by the text. Distinguish demonstrated from inferred skills.
Return ONLY valid JSON with this shape:
{
 "profile_summary":"2-3 sentence summary",
 "skills":[{"name":"skill","level":"Beginner|Developing|Proficient","confidence":0.0,"evidence":"specific phrase/project","evidence_type":"Project|Course|Experience|Self-reported"}],
 "role_fit_summary":"balanced comparison to target role",
 "gaps":[{"skill":"missing or weak skill","priority":"High|Medium|Low","reason":"why it matters","prerequisite":"what to learn or demonstrate first"}],
 "next_action":{"title":"one achievable task","why":"why this next","steps":["step 1","step 2","step 3"],"success_evidence":"what to produce","estimated_hours":4}
}
Confidence is 0-1. Include at most 8 skills and 5 gaps. Recommend one small action, not a huge project.
Never invent qualifications, certificates, employment, or completed projects. If evidence is insufficient, say so and recommend a diagnostic task.
"""
    user_prompt = f"Target role: {role}\n\nStudent learning journey:\n---\n{journey}\n---\nAnalyze this journey and return the JSON object only."
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        temperature=0.2,
    )
    content = (response.choices[0].message.content or "").strip()
    if content.startswith("```"):
        content = content.split("\n", 1)[-1]
        if content.endswith("```"):
            content = content[:-3].strip()
        if content.lower().startswith("json"):
            content = content[4:].strip()
    try:
        result = json.loads(content)
    except json.JSONDecodeError as exc:
        raise RuntimeError("The model response was not valid JSON. Try again or use a model that follows structured instructions.") from exc
    required = ["profile_summary", "skills", "role_fit_summary", "gaps", "next_action"]
    if any(k not in result for k in required) or not isinstance(result["skills"], list) or not isinstance(result["gaps"], list) or not isinstance(result["next_action"], dict):
        raise RuntimeError("The model returned an unexpected JSON structure. Try again.")
    return result

if submitted:
    if len(history.strip()) < 30:
        st.warning("Add a few sentences about your learning journey so the analysis has evidence to work with.")
    elif not target_role.strip():
        st.warning("Enter a target role.")
    else:
        with st.spinner("Mapping your skills and finding your next step..."):
            try:
                st.session_state["pw_result"] = analyze_journey(history.strip(), target_role.strip())
                st.session_state["pw_role"] = target_role.strip()
            except Exception as exc:
                st.error(f"Analysis failed: {exc}")
                st.info("Check your API key, model name, endpoint URL, and provider quota. Your provider must support OpenAI-compatible chat completions.")

result = st.session_state.get("pw_result")
if result:
    st.divider()
    st.header("Your Pathweaver map")
    st.subheader("Your current identity")
    st.write(result["profile_summary"])
    st.caption(f"Target role: {st.session_state.get('pw_role', target_role)}")
    skills, gaps = result.get("skills", []), result.get("gaps", [])
    c1, c2, c3 = st.columns(3)
    c1.metric("Skills identified", len(skills))
    c2.metric("High-priority gaps", sum(1 for g in gaps if str(g.get("priority", "")).lower() == "high"))
    c3.metric("Next action", "1")
    left, right = st.columns([1.1, 1])
    with left:
        st.subheader("Skills supported by evidence")
        if not skills:
            st.info("No skills were confidently extracted. Add more project and learning details.")
        for skill in skills:
            with st.container(border=True):
                st.markdown(f"**{skill.get('name', 'Skill')}** · {skill.get('level', 'Unspecified')}")
                try:
                    confidence = max(0.0, min(1.0, float(skill.get("confidence", 0))))
                except (TypeError, ValueError):
                    confidence = 0.0
                st.progress(confidence, text=f"Evidence confidence: {confidence:.0%}")
                st.caption(f"Evidence: {skill.get('evidence', 'Not provided')}")
                st.caption(f"Evidence type: {skill.get('evidence_type', 'Unspecified')}")
    with right:
        st.subheader("Career gap analysis")
        st.write(result.get("role_fit_summary", ""))
        for gap in gaps:
            priority = gap.get("priority", "Medium")
            with st.expander(f"{gap.get('skill', 'Skill gap')} · {priority} priority", expanded=str(priority).lower() == "high"):
                st.write(gap.get("reason", ""))
                st.caption(f"Prerequisite: {gap.get('prerequisite', 'Not specified')}")
        if not gaps:
            st.success("No specific gaps identified. Validate the profile against an actual job description.")
    st.subheader("Your next-best action")
    action = result.get("next_action", {})
    with st.container(border=True):
        st.markdown(f"### {action.get('title', 'Recommended task')}")
        st.write(action.get("why", ""))
        if action.get("estimated_hours") is not None:
            st.caption(f"Estimated effort: {action['estimated_hours']} hours")
        st.markdown("**Steps**")
        for step in action.get("steps", []):
            st.markdown(f"- {step}")
        st.markdown("**Evidence to produce**")
        st.write(action.get("success_evidence", ""))
        st.info("AI-generated guidance can be wrong. Validate it against real job descriptions and your own experience.")
    with st.expander("View raw JSON (debugging)"):
        st.json(result)

st.divider()
st.caption("Pathweaver AI MVP · Submitted text is sent to the configured model provider. Avoid entering sensitive personal information.")
