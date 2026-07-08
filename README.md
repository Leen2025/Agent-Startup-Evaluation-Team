# 🏦 AI Boardroom – Startup Evaluation Team

A local Streamlit app where **8 AI expert agents** evaluate your startup idea
and give you a final investor verdict — score, decision, MVP plan, strengths,
risks, and next steps.

Runs 100% locally via [Ollama](https://ollama.com). No paid APIs, no internet
search, nothing sent to the cloud.

---

## 👥 The 8 Agents

| # | Agent | What they cover |
|---|---|---|
| 1 | 🎯 CEO & Strategy | Vision, positioning, long-term goals |
| 2 | 📊 Market Research | Market size, segments, competitors, trends |
| 3 | 💰 Business Model | Revenue streams, pricing, costs, path to profit |
| 4 | 😊 Customer Experience | User journey, onboarding, retention |
| 5 | 🛠️ Software Architect | Tech stack, system design, scalability |
| 6 | 🚀 Operations & Execution | Team, 90-day roadmap, budget split, metrics |
| 7 | 🛡️ Risk & Security | Business, legal, security, mitigation |
| 8 | 🏦 Investor / Final Decision | Reads all 7 reports, gives the verdict |

The **Investor Agent** produces:

- ✅ Final Score `/100`
- ✅ Investment Decision
- ✅ MVP Recommendation
- ✅ Key Strengths
- ✅ Key Risks
- ✅ Next Steps

---

## 📂 Project Structure

```
ai_boardroom/
├── app.py              # Streamlit UI
├── agents.py           # The 8 agents + orchestration
├── ollama_client.py    # Thin wrapper around the local Ollama API
├── prompts.py          # All prompt templates in one place
├── requirements.txt    # Python dependencies
└── README.md
```

---

## 🚀 Setup (5 steps)

### 1. Create the folder (if you don't already have it)

```bash
mkdir ai_boardroom
cd ai_boardroom
```

Then place `app.py`, `agents.py`, `ollama_client.py`, `prompts.py`,
`requirements.txt`, and this `README.md` inside.

### 2. Create a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the requirements

```bash
pip install -r requirements.txt
```

### 4. Install Ollama and pull a model

1. Download and install Ollama from **https://ollama.com/download**
2. Start it (the Ollama app runs quietly in the background).
3. Pull a model — pick ONE:

   ```bash
   # Smart, recommended default (needs ~6 GB RAM):
   ollama pull qwen2.5:7b

   # Small and fast, good for low-RAM machines (~3 GB):
   ollama pull gemma2:2b
   ```

### 5. Run the Streamlit app

```bash
streamlit run app.py
```

Streamlit will open `http://localhost:8501` in your browser.

---

## 🔧 Changing the model

The default model is set in **one place**:

```python
# ollama_client.py
DEFAULT_MODEL = "qwen2.5:7b"
```

You can also change it live from the **sidebar** in the app — just type the
model tag (for example `gemma2:2b`) and click **🚀 Run the Boardroom**.

Any model tag that works with `ollama pull <tag>` will work here.

---

## 🧪 How to use

1. Open the app in your browser.
2. Fill in:
   - **Startup name**
   - **One-line idea**
   - **Target users**
   - **Problem**
   - **Solution**
   - **Budget**
3. Click **🚀 Run the Boardroom**.
4. Watch the spinner — each agent thinks in turn.
5. Read the **7 specialist tabs** and the **Investor final verdict**.
6. Click **⬇️ Download full report** to save it as Markdown.

---

## 🩹 Troubleshooting

**"Could not connect to Ollama"**
The Ollama app is not running. Open it (Windows/Mac tray icon) or run
`ollama serve` in a terminal.

**"the model 'X' is not installed"**
Run `ollama pull <model-tag>` — for example `ollama pull qwen2.5:7b`.

**Responses are very slow**
Try a smaller model: `ollama pull gemma2:2b` and set it in the sidebar.

**The app crashes with a Python error**
Make sure your virtual environment is active and `pip install -r
requirements.txt` completed without errors.

---

## 📝 License

MIT — do whatever you like, no warranty.
