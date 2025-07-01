import streamlit as st
import os
from dotenv import load_dotenv
import pandas as pd
from tavily import TavilyClient
import datetime

# ✅ Set page config at the top
st.set_page_config(page_title="AI Investing News Report", layout="centered")

# Load environment variables from .env
load_dotenv()

# Input for API keys
st.title("📰 AI Investing Deep News Tool")

st.markdown("""
Enter your API keys below. These are not stored and are only used during your session.
""")

openai_api_key = st.text_input("🔑 OpenAI API Key", type="password")
tavily_api_key = st.text_input("🔑 Tavily API Key", type="password")

# Input for topic
search_topic = st.text_input("💡 Investment Topic", value="Nuclear energy")

# Slider for date range
today = datetime.date.today()
default_start = today - datetime.timedelta(days=30)
date_range = st.slider(
    "🗓️ Period filter",
    min_value=today - datetime.timedelta(days=180),
    max_value=today,
    value=(default_start, today),
    format="YYYY-MM-DD"
)

# Search button
if st.button("Search News"):
    if not tavily_api_key:
        st.error("Please enter your Tavily API key.")
    else:
        try:
            client = TavilyClient(api_key=tavily_api_key)

            queries = [
                search_topic,
                f"{search_topic} AND startup",
                f"{search_topic} AND funding",
                f"{search_topic} AND acquisition"
            ]

            all_results = []
            for q in queries:
                st.write(f"🔍 Tavily query: {q}")
                response = client.search(
                    query=q,
                    search_depth="advanced",
                    include_domains=["techcrunch.com", "crunchbase.com", "venturebeat.com"],
                    max_results=5
                )
                results = response.get("results", [])
                all_results.extend(results)

            st.success(f"✅ Collected {len(all_results)} articles")

            # Convert to DataFrame
            df = pd.DataFrame(all_results)

            # Ensure expected columns exist
            for col in ["published_date", "title", "url", "content"]:
                if col not in df.columns:
                    df[col] = ""

            # Parse and filter by date
            df["published_date"] = pd.to_datetime(df["published_date"], errors="coerce")
            mask = (df["published_date"] >= pd.to_datetime(date_range[0])) & \
                   (df["published_date"] <= pd.to_datetime(date_range[1]))
            filtered_df = df[mask]

            st.markdown(f"### ✨ Showing {len(filtered_df)} articles from selected period")

            for _, row in filtered_df.iterrows():
                st.markdown(f"### [{row['title']}]({row['url']})")
                if pd.notnull(row["published_date"]):
                    st.markdown(f"*Published:* {row['published_date'].strftime('%Y-%m-%d')}")
                st.markdown(row["content"][:500] + "...")
                st.markdown("---")

        except Exception as e:
            st.error(f"Error occurred: {e}")
