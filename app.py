import streamlit as st
import os
from dotenv import load_dotenv
import pandas as pd
from tavily import TavilyClient
import datetime
import sys

# Optional: Load .env if local
load_dotenv()

# Ensures Rust compatibility with certain packages
os.environ["PYO3_USE_ABI3_FORWARD_COMPATIBILITY"] = "1"

# Version info
st.write("Python version:", sys.version)

# === STREAMLIT UI ===
st.set_page_config(page_title="AI Investing News Report", layout="centered")
st.title("📰 AI Investing Deep News Tool")

st.markdown("""
Enter your API keys below. We do **not** store them. They are only used during your session.
""")

openai_key = st.text_input("🔑 OpenAI API Key", type="password")
tavily_key = st.text_input("🔍 Tavily API Key", type="password")

keyword = st.text_input("Enter a topic (e.g., nuclear energy, AI, lithium):")
days = st.slider("How many days of news?", min_value=1, max_value=30, value=7)

if st.button("Generate Report"):
    if not openai_key or not tavily_key:
        st.error("Please enter both API keys.")
    elif not keyword:
        st.error("Please enter a topic keyword.")
    else:
        with st.spinner("Fetching and analyzing news..."):
            try:
                # Create Tavily client
                tavily_client = TavilyClient(api_key=tavily_key)

                # Define search queries
                queries = [
                    keyword,
                    f"{keyword} AND startup",
                    f"{keyword} AND funding",
                    f"{keyword} AND acquisition",
                ]

                all_results = []

                for query in queries:
                    st.write(f"🔍 Tavily query: {query}")
                    response = tavily_client.search(
                        query=query,
                        search_depth="advanced",
                        max_results=5
                    )
                    results = response.get("results", [])
                    all_results.extend(results)

                if not all_results:
                    st.warning("No articles found. Try a different topic.")
                else:
                    df = pd.DataFrame(all_results)
                    st.success(f"✅ Collected {len(df)} articles")

                    # Display only existing columns
                    columns_to_show = [col for col in ["title", "url", "published_date"] if col in df.columns]
                    st.dataframe(df[columns_to_show])

                    # Save to markdown
                    date_str = datetime.date.today().isoformat()
                    md_path = f"{keyword.replace(' ', '_').lower()}_{date_str}.md"

                    with open(md_path, "w") as f:
                        for row in all_results:
                            title = row.get("title", "No title")
                            url = row.get("url", "No URL")
                            date = row.get("published_date", "Date unknown")
                            f.write(f"### {title}\n\n{url}\n\nPublished: {date}\n\n---\n\n")

                    st.markdown(f"📄 Markdown saved: `{md_path}`")

            except Exception as e:
                st.error(f"Error occurred: {e}")
