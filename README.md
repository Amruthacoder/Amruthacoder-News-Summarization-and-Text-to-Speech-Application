# 📰 News Sentiment Analysis with Hindi TTS 🎙️

![Alt](https://static-blog.onlyoffice.com/wp-content/uploads/2023/08/14123647/ONLYOFFICE-10-text-to-speech-tools-to-consider-in-2023.png)
## 📌 Project Overview

This project is a news sentiment analysis tool that scrapes recent news articles for a given company, summarizes them, performs sentiment analysis, and generates a Hindi TTS (Text-to-Speech) summary. The analysis helps users understand media coverage trends and sentiment distribution.

## 🔥 Features

- Scrape news articles from selected sources.

- Summarize articles using the BART model.

- Perform sentiment analysis using TextBlob.

- Generate Hindi speech with gTTS.

- Provide a comparative analysis of different articles.

- FastAPI backend with endpoints for data access.

- Deployed on Hugging Face Spaces for easy access.

## 🚀 Tech Stack

- Python (FastAPI, BeautifulSoup, Requests, Pandas, NLTK)

- YAKE (Keyword extraction)

- TextBlob (Sentiment analysis)

- Facebook BART Model (Summarization)

- gTTS (Hindi Text-to-Speech)

- FastAPI (Backend API development)

- Streamlit (User interface)

- Hugging Face Spaces (Deployment)

## 📥 Installation & Setup

🛠️ 1. Clone the Repository

📦 2. Install Dependencies

▶️ 3. Run the FastAPI Server

API will be available at: http://127.0.0.1:8000/docs

🎭 4. Run the Streamlit UI (Optional)

run.py is there to serve as the entry point for running the application, handling initialization, and managing API or UI execution. 🚀

🌍 How to Use

1️⃣ Access the API

Visit Your Hugging Face Space to test it directly.

2️⃣ API Endpoints

Method

Endpoint

Description

GET

/scrape_news/{company}

Scrape news articles for a company

GET

/get_news/{company}

Get sentiment analysis report

GET

/get_tts/{company}

Get Hindi speech summary

3️⃣ Example Request

📊 Model Details

🔹 Summarization Model

- Uses Facebook BART (facebook/bart-large-cnn) for text summarization.

- Extracts key information from scraped news articles.

🔹 Sentiment Analysis

- Uses TextBlob for polarity-based sentiment scoring.

- Classifies articles as Positive, Negative, or Neutral.

🔹 Hindi TTS (Text-to-Speech)

- Uses gTTS (Google Text-to-Speech) to generate Hindi audio.

- Creates a spoken summary of sentiment analysis.

## ⚠️ Assumptions & Limitations

- Scraped articles depend on website structure and may fail if changes occur.

- Sentiment analysis is based on text polarity and may not always capture nuances.

- Only supports English text input but generates Hindi speech.

## 🚀 Deployment

🔗 Live Demo
You can try the application live on Hugging Face Spaces:  
[🖥️ News Summarization Hindi TTS](https://huggingface.co/spaces/Amruthayenikonda/News-Summarization-Hindi-TTS)

No account needed to access API docs and test endpoints!

💡 Feel free to contribute or report issues! 🎯




