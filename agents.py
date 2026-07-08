"""
agents.py
---------
Defines the 8 boardroom agents.

Each agent is just:
    - a name
    - an emoji/icon (nice for the UI)
    - a function that builds its prompt
    - a `run()` method that sends the prompt to Ollama and returns text

The Investor agent is special: it needs the other 7 reports as input.
"""

from typing import Callable

from ollama_client import generate, DEFAULT_MODEL
import prompts


class Agent:
    """A single expert on the AI boardroom."""

    def __init__(self, name: str, icon: str, prompt_builder: Callable):
        self.name = name
        self.icon = icon
        self.prompt_builder = prompt_builder

    def run(self, info: dict, model: str = DEFAULT_MODEL, **extra) -> str:
        """
        Build the prompt and ask Ollama for a response.

        `extra` is used by the Investor agent to pass in `agent_reports`.
        """
        prompt = self.prompt_builder(info, **extra) if extra else self.prompt_builder(info)
        return generate(prompt, model=model)


# ---------------------------------------------------------------------------
# The 7 specialist agents (run in order, in parallel-friendly style).
# ---------------------------------------------------------------------------
SPECIALIST_AGENTS: list[Agent] = [
    Agent("CEO & Strategy",       "", prompts.ceo_prompt),
    Agent("Market Research",      "", prompts.market_prompt),
    Agent("Business Model",       "", prompts.business_model_prompt),
    Agent("Customer Experience",  "", prompts.cx_prompt),
    Agent("Software Architect",   "", prompts.architect_prompt),
    Agent("Operations & Execution","", prompts.operations_prompt),
    Agent("Risk & Security",      "", prompts.risk_prompt),
]


# The 8th agent — always runs last, sees everyone else's report.
INVESTOR_AGENT = Agent(
    name="Investor / Final Decision",
    icon="",
    prompt_builder=prompts.investor_prompt,
)


def run_boardroom(info: dict, model: str = DEFAULT_MODEL, on_progress=None) -> dict:
    """
    Run the full boardroom evaluation.

    Parameters
    ----------
    info : dict
        Startup info collected from the Streamlit form.
    model : str
        Ollama model tag to use.
    on_progress : callable(name: str) -> None, optional
        Called before each agent runs so the UI can show progress.

    Returns
    -------
    dict
        {
          "specialists": { agent_name: report_text, ... },  # 7 items
          "investor": "final verdict text",
        }
    """
    specialist_reports: dict[str, str] = {}

    for agent in SPECIALIST_AGENTS:
        if on_progress:
            on_progress(f"{agent.icon} {agent.name}")
        specialist_reports[agent.name] = agent.run(info, model=model)

    if on_progress:
        on_progress(f"{INVESTOR_AGENT.icon} {INVESTOR_AGENT.name}")

    investor_verdict = INVESTOR_AGENT.run(
        info,
        model=model,
        agent_reports=specialist_reports,
    )

    return {
        "specialists": specialist_reports,
        "investor": investor_verdict,
    }
