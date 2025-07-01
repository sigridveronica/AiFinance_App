import streamlit as st
import os
from dotenv import load_dotenv
import pandas as pd
from tavily import TavilyClient
import datetime
import sys

# ✅ Must be first Streamlit call
st.set_page_config(page_title="AI Investing News Report", layout="centered")

# Load environment variables
load_dotenv()

# Set compatibility for Rust/PyO3-related builds
os.environ["PYO3_USE_ABI3_FORWARD_COMPATIBILITY"] = "1"

# Debug info (optional)
st.write("Python version:", sys.version)

st.title("📰 AI Investing Deep News Tool")

st.markdown("""
Enter your API keys below. These are not stored and are only used during your session.
""")

# User input for Tavily API key
tavily_api_key = st.text_input("🔑 Tavily API Key", type="password")

# Get the search topic
search_topic = st.text_input("💡 Investment Topic", value="Nuclear energy")

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

            # Create DataFrame
            df = pd.DataFrame(all_results)

            # ✅ Handle missing columns gracefully
            expected_cols = ["title", "url", "content", "published_date"]
            for col in expected_cols:
                if col not in df.columns:
                    df[col] = ""

            # Format dates
            if "published_date" in df.columns:
                try:
                    df["published_date"] = pd.to_datetime(df["published_date"], errors="coerce")
                except Exception as e:
                    st.warning(f"Couldn't parse dates: {e}")

            # Display results
            for idx, row in df.iterrows():
                st.markdown(f"### [{row['title']}]({row['url']})")
                st.markdown(f"*Published:* {row['published_date']}")
                st.markdown(row["content"][:500] + "...")
                st.markdown("---")

        except Exception as e:
            st.error(f"Error occurred: {e}")
