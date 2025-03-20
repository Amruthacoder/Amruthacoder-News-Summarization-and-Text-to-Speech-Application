import streamlit as st
import requests

# 🎯 Backend API Base URL
BASE_URL = "http://127.0.0.1:8000"

st.title("📰 News Sentiment Analysis with Hindi TTS 🎙️")

# ✅ User selects a company
company = st.selectbox("Choose a company:", ["apple", "samsung"])

if st.button("Fetch News & Sentiment Analysis"):
    # 🎯 API Call to Scrape & Process News
    scrape_response = requests.get(f"{BASE_URL}/scrape_news/{company}")

    if scrape_response.status_code == 200:
        st.success(f"✅ News for {company.capitalize()} scraped successfully!")

        # 🎯 Fetch Sentiment Analysis
        news_response = requests.get(f"{BASE_URL}/get_news/{company}")

        if news_response.status_code == 200:
            sentiment_data = news_response.json()

            if "Comparative Sentiment Score" in sentiment_data:
                st.subheader(f"📊 Sentiment Analysis for {company.capitalize()}")

                # ✅ **Sentiment Distribution**
                st.write("### 📊 Sentiment Distribution")
                st.json(sentiment_data["Comparative Sentiment Score"]["Sentiment Distribution"])

                # ✅ **Most Positive Article**
                st.write("### 🏆 Most Positive Article")
                st.json(sentiment_data.get("Most Positive Article", "No data available"))

                # ✅ **Coverage Differences**
                st.write("### ⚖️ Coverage Differences (Comparisons)")
                st.json(sentiment_data["Comparative Sentiment Score"].get("Coverage Differences", "No data available"))

            else:
                st.warning(f"ℹ️ No comparative sentiment data found for {company.capitalize()}.")
        else:
            st.error(f"❌ Error fetching sentiment data: {news_response.json()}")

    else:
        st.error(f"❌ Error scraping news: {scrape_response.json()}")

# 🎵 **Play Hindi Sentiment Audio**
if st.button("Play Hindi Sentiment Audio 🎵"):
    # 🎯 API Call to Generate & Fetch TTS Audio
    tts_response = requests.get(f"{BASE_URL}/get_tts/{company}")

    if tts_response.status_code == 200:
        st.success(f"🎙️ Playing Hindi sentiment analysis for {company.capitalize()}...")

        # 🎧 Embed audio in Streamlit
        st.audio(f"{BASE_URL}/get_tts/{company}", format="audio/mpeg")
    else:
        st.error(f"❌ Error fetching Hindi TTS audio: {tts_response.json()}")