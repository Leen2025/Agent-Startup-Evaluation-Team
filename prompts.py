"""
prompts.py
----------
All the prompt templates for the 8 boardroom agents live here.

Each function takes the startup information (and, for the final agent,
the other agents' reports) and returns a ready-to-send prompt string.

Keeping prompts in one file makes them easy to tweak without touching
the app logic.
"""


# A shared header that reminds the model to stay focused and structured.
COMMON_STYLE = (
    "You are a senior expert on an AI startup evaluation board.\n"
    "Write in clear, concise business English.\n"
    "Use short sections with bold headings and bullet points.\n"
    "Do NOT invent numbers you cannot justify. If unsure, say so.\n"
)


def _startup_block(info: dict) -> str:
    """Format the startup info into a reusable block that every prompt includes."""
    return (
        f"STARTUP NAME: {info['name']}\n"
        f"IDEA: {info['idea']}\n"
        f"TARGET USERS: {info['target_users']}\n"
        f"PROBLEM: {info['problem']}\n"
        f"SOLUTION: {info['solution']}\n"
        f"BUDGET: {info['budget']}\n"
    )


# ---------------------------------------------------------------------------
# 1. CEO & Strategy Agent
# ---------------------------------------------------------------------------
def ceo_prompt(info: dict) -> str:
    return (
        f"{COMMON_STYLE}\n"
        "ROLE: You are the CEO & Strategy expert.\n\n"
        "STARTUP BRIEF:\n"
        f"{_startup_block(info)}\n"
        "Please produce a strategic overview with these sections:\n"
        "1. Vision & Mission\n"
        "2. Strategic Positioning (what makes it stand out)\n"
        "3. Long-term Goals (1, 3, 5 years)\n"
        "4. Success Criteria (how we know it's winning)\n"
        "Keep it under 300 words.\n"
    )


# ---------------------------------------------------------------------------
# 2. Market Research Agent
# ---------------------------------------------------------------------------
def market_prompt(info: dict) -> str:
    return (
        f"{COMMON_STYLE}\n"
        "ROLE: You are the Market Research expert.\n\n"
        "STARTUP BRIEF:\n"
        f"{_startup_block(info)}\n"
        "Produce a market analysis with these sections:\n"
        "1. Market Size (rough qualitative estimate + reasoning)\n"
        "2. Target Segments (who exactly)\n"
        "3. Competitors (3-5 examples and how they differ)\n"
        "4. Trends & Timing (why now)\n"
        "5. Market Risks\n"
        "Keep it under 350 words.\n"
    )


# ---------------------------------------------------------------------------
# 3. Business Model Agent
# ---------------------------------------------------------------------------
def business_model_prompt(info: dict) -> str:
    return (
        f"{COMMON_STYLE}\n"
        "ROLE: You are the Business Model expert.\n\n"
        "STARTUP BRIEF:\n"
        f"{_startup_block(info)}\n"
        "Produce a business model plan with these sections:\n"
        "1. Revenue Streams (how it makes money)\n"
        "2. Pricing Model (subscription, one-time, freemium, etc.)\n"
        "3. Cost Structure (main cost drivers)\n"
        "4. Unit Economics (rough view of margin per customer)\n"
        "5. Path to Profitability\n"
        "Keep it under 350 words.\n"
    )


# ---------------------------------------------------------------------------
# 4. Customer Experience Agent
# ---------------------------------------------------------------------------
def cx_prompt(info: dict) -> str:
    return (
        f"{COMMON_STYLE}\n"
        "ROLE: You are the Customer Experience (CX/UX) expert.\n\n"
        "STARTUP BRIEF:\n"
        f"{_startup_block(info)}\n"
        "Produce a customer experience plan with these sections:\n"
        "1. User Journey (from discovery to loyal user)\n"
        "2. Key Touchpoints and how they should feel\n"
        "3. Onboarding Experience\n"
        "4. Retention & Delight Ideas\n"
        "5. Top 3 UX Risks\n"
        "Keep it under 300 words.\n"
    )


# ---------------------------------------------------------------------------
# 5. Software Architect Agent
# ---------------------------------------------------------------------------
def architect_prompt(info: dict) -> str:
    return (
        f"{COMMON_STYLE}\n"
        "ROLE: You are the Software Architect.\n\n"
        "STARTUP BRIEF:\n"
        f"{_startup_block(info)}\n"
        "Produce a technical architecture proposal with these sections:\n"
        "1. Recommended Tech Stack (frontend, backend, database, hosting)\n"
        "2. High-level System Design (main components and how they talk)\n"
        "3. Scalability Plan\n"
        "4. Integrations / Third-party Services\n"
        "5. Technical Risks\n"
        "Keep it under 350 words.\n"
    )


# ---------------------------------------------------------------------------
# 6. Operations & Execution Agent
# ---------------------------------------------------------------------------
def operations_prompt(info: dict) -> str:
    return (
        f"{COMMON_STYLE}\n"
        "ROLE: You are the Operations & Execution expert.\n\n"
        "STARTUP BRIEF:\n"
        f"{_startup_block(info)}\n"
        "Produce an execution plan with these sections:\n"
        "1. Team Roles Needed for MVP\n"
        "2. 90-Day Execution Roadmap (weeks/milestones)\n"
        "3. Budget Allocation (rough % split of the given budget)\n"
        "4. Key Operational Risks\n"
        "5. Metrics to Track Weekly\n"
        "Keep it under 350 words.\n"
    )


# ---------------------------------------------------------------------------
# 7. Risk & Security Agent
# ---------------------------------------------------------------------------
def risk_prompt(info: dict) -> str:
    return (
        f"{COMMON_STYLE}\n"
        "ROLE: You are the Risk & Security expert.\n\n"
        "STARTUP BRIEF:\n"
        f"{_startup_block(info)}\n"
        "Produce a risk & security review with these sections:\n"
        "1. Business Risks (market, competition, timing)\n"
        "2. Legal & Compliance Risks (privacy, data, regional laws)\n"
        "3. Security Risks (data protection, auth, abuse)\n"
        "4. Operational Risks\n"
        "5. Mitigation Plan (top 5 concrete actions)\n"
        "Keep it under 350 words.\n"
    )


# ---------------------------------------------------------------------------
# 8. Investor / Final Decision Agent
# ---------------------------------------------------------------------------
def investor_prompt(info: dict, agent_reports: dict) -> str:
    """
    The investor reads the other 7 reports and gives a final verdict.
    `agent_reports` is a dict: { "CEO & Strategy": "...", "Market Research": "...", ... }
    """
    joined_reports = "\n\n".join(
        f"### {name} Report ###\n{text}"
        for name, text in agent_reports.items()
    )

    return (
        f"{COMMON_STYLE}\n"
        "ROLE: You are a seasoned Investor making the FINAL decision.\n"
        "You have just read the reports from 7 other experts.\n\n"
        "STARTUP BRIEF:\n"
        f"{_startup_block(info)}\n\n"
        "EXPERT REPORTS:\n"
        f"{joined_reports}\n\n"
        "Now write your FINAL VERDICT using EXACTLY this structure, "
        "with these exact bold headings on their own lines:\n\n"
        "**Final Score:** <a number from 0 to 100> / 100\n\n"
        "**Investment Decision:** <one of: Strong Invest / Invest / "
        "Invest with Conditions / Pass>\n\n"
        "**MVP Recommendation:**\n"
        "- 3 to 5 bullet points describing the smallest useful MVP\n\n"
        "**Key Strengths:**\n"
        "- 3 to 5 bullets\n\n"
        "**Key Risks:**\n"
        "- 3 to 5 bullets\n\n"
        "**Next Steps:**\n"
        "- 3 to 5 concrete actions for the next 30 days\n\n"
        "Be honest. If the idea is weak, say so and explain why.\n"
    )
