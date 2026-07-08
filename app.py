"""
app.py
------
Streamlit UI for the AI Boardroom – Startup Evaluation Team.

Run with:
    streamlit run app.py
"""

import streamlit as st

from agents import SPECIALIST_AGENTS, INVESTOR_AGENT, run_boardroom
from ollama_client import DEFAULT_MODEL, OllamaError, check_ollama_available


# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Boardroom – Startup Evaluation Team",
    page_icon="",
    layout="wide",
)

st.title(" AI Boardroom – Startup Evaluation Team")
st.caption(
    "Enter your startup idea and let 8 AI experts evaluate it, "
    "ending with a final investor verdict. Runs 100% locally on Ollama."
)


# ---------------------------------------------------------------------------
# Sidebar: model + Ollama health
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header(" Settings")

    model = st.text_input(
        "Ollama model",
        value=DEFAULT_MODEL,
        help="Examples: qwen2.5:7b, gemma2:2b, llama3.1:8b. "
             "Make sure you ran `ollama pull <model>` first.",
    )

    if st.button(" Check Ollama connection"):
        ok, msg = check_ollama_available(model=model)
        (st.success if ok else st.error)(msg)

    st.markdown("---")
    st.markdown("### The 8 Agents")
    for a in SPECIALIST_AGENTS:
        st.write(f"{a.icon} {a.name}")
    st.write(f"{INVESTOR_AGENT.icon} {INVESTOR_AGENT.name}")


# ---------------------------------------------------------------------------
# Main input form
# ---------------------------------------------------------------------------
st.subheader(" Startup Brief")

with st.form("startup_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Startup name", placeholder="e.g. Leen Alsaleh Coffee")
        target_users = st.text_input(
            "Target users",
            placeholder="e.g. Customers in Saudi Arabia",
        )
        budget = st.text_input(
            "Budget",
            placeholder="e.g. $20,000 for the first 6 months",
        )
    with col2:
        idea = st.text_area(
            "One-line idea",
            placeholder="e.g. specialty coffee subscription service with Arabic-first branding.",
            height=90,
        )
        problem = st.text_area(
            "Problem you are solving",
            height=90,
            placeholder="e.g. Lack of accessible, culturally relevant coffee options in Saudi Arabia.",
        )
        solution = st.text_area(
            "Your solution",
            height=90,
            placeholder="e.g. A subscription service for specialty coffee with Arabic-first branding.",
        )

    submitted = st.form_submit_button(" Run the Boardroom")


# ---------------------------------------------------------------------------
# Run the boardroom on submit
# ---------------------------------------------------------------------------
def _all_filled(*values: str) -> bool:
    return all(v and v.strip() for v in values)


if submitted:
    if not _all_filled(name, idea, target_users, problem, solution, budget):
        st.warning("Please fill in every field before running the boardroom.")
        st.stop()

    # Pre-flight health check so we fail fast with a clear message.
    ok, health_msg = check_ollama_available(model=model)
    if not ok:
        st.error(health_msg)
        st.stop()

    info = {
        "name": name,
        "idea": idea,
        "target_users": target_users,
        "problem": problem,
        "solution": solution,
        "budget": budget,
    }

    # Live progress indicator.
    progress_area = st.empty()

    def on_progress(agent_label: str) -> None:
        progress_area.info(f"Thinking… {agent_label}")

    try:
        with st.spinner("The boardroom is deliberating. This may take a few minutes…"):
            result = run_boardroom(info, model=model, on_progress=on_progress)
    except OllamaError as e:
        progress_area.empty()
        st.error(f"Ollama error:\n\n{e}")
        st.stop()
    except Exception as e:  # any other crash
        progress_area.empty()
        st.exception(e)
        st.stop()

    progress_area.empty()
    st.success(" Boardroom evaluation complete.")

    # -----------------------------------------------------------------------
    # Show the specialist reports in tabs
    # -----------------------------------------------------------------------
    st.subheader(" Specialist Reports")

    tab_labels = [f"{a.icon} {a.name}" for a in SPECIALIST_AGENTS]
    tabs = st.tabs(tab_labels)
    for tab, agent in zip(tabs, SPECIALIST_AGENTS):
        with tab:
            st.markdown(result["specialists"][agent.name])

    # -----------------------------------------------------------------------
    # Investor final verdict (the star of the show)
    # -----------------------------------------------------------------------
    st.subheader(f"{INVESTOR_AGENT.icon} Final Verdict — {INVESTOR_AGENT.name}")
    with st.container(border=True):
        st.markdown(result["investor"])

    # -----------------------------------------------------------------------
    # Download button so the user can keep the report
    # -----------------------------------------------------------------------
    full_report_parts = [f"# AI Boardroom Report — {name}\n"]
    for agent in SPECIALIST_AGENTS:
        full_report_parts.append(f"\n## {agent.icon} {agent.name}\n")
        full_report_parts.append(result["specialists"][agent.name])
    full_report_parts.append(f"\n## {INVESTOR_AGENT.icon} {INVESTOR_AGENT.name}\n")
    full_report_parts.append(result["investor"])
    full_report = "\n".join(full_report_parts)

    st.download_button(
        "⬇ Download full report (Markdown)",
        data=full_report,
        file_name=f"{name.replace(' ', '_')}_boardroom_report.md",
        mime="text/markdown",
    )
