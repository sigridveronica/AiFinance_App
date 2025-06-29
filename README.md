# 🧠 AiFinance App

An interactive AI-powered financial analysis tool that processes news articles and generates value-investment insights using LLMs and signal tagging.

---

## 🚀 Features

- Analyze financial news using FinBERT and extract investment signals.
- Automatically generate recommendations: **Invest**, **Watch**, or **Avoid**.
- Fetch news summaries and convert them into investor reports.
- Deployable via **Streamlit** for easy online access – no local setup required for users.

---

## 🗂 Folder Structure

```
├── app.py                   # Streamlit frontend
├── requirements.txt         # Python dependencies
├── .env.example             # Template for environment variables
├── src/
│   ├── main.py              # Entrypoint for CLI use
│   ├── news_analysis.py     # Loads news and generates reports
│   ├── fin_interpreter.py   # Uses FinBERT + signal tagging
│   └── md_html.py           # Converts Markdown to HTML (optional)
├── external/
│   └── FinGPT/              # Cloned FinGPT repo (add if needed)
```

---

## ✅ Requirements

To run the project locally:

- Python >= 3.9, < 3.13 (⚠️ Streamlit Cloud currently uses 3.13 by default)
- `torch==2.2.2` (May be incompatible with Python 3.13)
- HuggingFace Transformers
- Langchain
- Pandas
- Streamlit

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` file:

```bash
cp .env.example .env
```

Add your API keys to `.env`:

```
OPENAI_KEY=your_openai_key
TAVILY_KEY=your_tavily_key
```

---

## 💻 Run Locally

```bash
streamlit run app.py
```

Or use CLI version:

```bash
python src/main.py
```

---

## ☁️ Deploy Online (Streamlit)

This repo is ready for **Streamlit Community Cloud**:

1. Push your repo to GitHub.
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud) and deploy it.
3. Set the environment variables (`OPENAI_KEY`, `TAVILY_KEY`) in the Streamlit app settings.

You don't need to share `.env`, just add the variables via the web interface.

If you're getting Torch install errors:
- Try removing or loosening the `torch==2.2.2` pin.
- Or specify an earlier Python version using a `runtime.txt` file (e.g. `python-3.10.13`).

---

## 🧪 Example Use

Input:
> "Tesla announced record-breaking deliveries in Q2 and strong future demand."

Output:
```json
{
  "sentiment": "positive",
  "confidence": 0.93,
  "investment_decision": "Invest",
  "signals": ["demand", "record"]
}
```

---

## 📄 License

MIT – feel free to fork and build on it!
