import os
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import nltk
import yake
from transformers import pipeline
from textblob import TextBlob
from gtts import gTTS
import json

# Download necessary NLTK data
nltk.download("punkt")
nltk.download("stopwords")

# Initialize YAKE and Summarizer
kw_extractor = yake.KeywordExtractor(lan="en", n=2, dedupLim=0.9, top=5)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Scrape and save articles
def scrape_articles(company, urls):
    """Scrapes news articles and saves them in `data/{company}_articles/`."""
    
    dir_path = f"data/{company}_articles"
    os.makedirs(dir_path, exist_ok=True)
    output_txt = f"{dir_path}/{company}_articles.txt"

    articles_data = {}

    for idx, url in enumerate(urls, start=1):
        try:
            time.sleep(2)
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.find("h1").text.strip() if soup.find("h1") else "No title found"
            content = " ".join([p.text.strip() for p in soup.find_all("p")])

            articles_data[idx] = {"title": title, "url": url, "content": content}
            print(f"✅ Scraped: {title}")

        except requests.RequestException as e:
            print(f"❌ Error scraping {url}: {str(e)}")

    # Save articles to text file with correct article numbers
    with open(output_txt, 'w', encoding='utf-8') as f:
        for article_number, data in articles_data.items():
            f.write(f"\n{'='*80}\n")
            f.write(f"Article Number: {article_number}\n")  
            f.write(f"TITLE: {data['title']}\n")
            f.write(f"URL: {data['url']}\n")
            f.write("-"*50 + "\n")
            f.write("CONTENT:\n")
            f.write(data['content'])
            f.write(f"\n{'='*80}\n")

    return output_txt

# Process articles & sentiment analysis**
def process_articles(company):
    """Reads scraped articles and generates summaries, sentiment analysis, and comparative insights."""
    
    dir_path = f"data/{company}_articles"
    input_txt = f"{dir_path}/{company}_articles.txt"
    output_json = f"{dir_path}/{company}_articles_sentiment.json"
    audio_path = f"/get_tts/{company}"  

    if not os.path.exists(input_txt):
        return {"error": f"No articles file found for {company}!"}

    with open(input_txt, "r", encoding="utf-8") as f:
        content = f.read()

    articles = content.strip().split("=" * 80)
    if not articles:
        return {"error": f"No valid articles found for {company}!"}

    data_list = []
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}

    for article in articles:
        lines = article.strip().split("\n")
        if len(lines) < 5:
            continue

        article_number = int(lines[0].replace("Article Number: ", "").strip())  
        title = lines[1].replace("TITLE: ", "").strip()
        url = lines[2].replace("URL: ", "").strip()
        article_content = "\n".join(lines[4:]).strip()

        summary = summarizer(article_content[:500], max_length=100, min_length=30, do_sample=False)[0]["summary_text"]
        keywords = [kw[0] for kw in kw_extractor.extract_keywords(article_content)]
        polarity = TextBlob(summary).sentiment.polarity

        if polarity > 0:
            sentiment = "Positive"
        elif polarity < -0.1:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        sentiment_counts[sentiment] += 1

        data_list.append({
            "Article Number": article_number,  
            "Title": title,
            "URL": url,
            "Summary": summary,
            "Sentiment": sentiment,
            "Keywords": keywords
        })

    #Generate Comparative Sentiment Analysis
    comparisons = []
    for i in range(len(data_list) - 1):
        comparisons.append({
            "Comparison": f"Article {data_list[i]['Article Number']} discusses {', '.join(data_list[i]['Keywords'])}, "
                          f"while Article {data_list[i+1]['Article Number']} focuses on {', '.join(data_list[i+1]['Keywords'])}.",
            "Impact": f"Article {data_list[i]['Article Number']} may impact {data_list[i]['Sentiment']} market trends, "
                      f"while Article {data_list[i+1]['Article Number']} could affect {data_list[i+1]['Sentiment']} consumer perceptions."
        })

    # Final Sentiment Analysis
    most_common_sentiment = max(sentiment_counts, key=sentiment_counts.get)

    final_analysis = f"{company} की हाल की खबरें ज्यादातर {most_common_sentiment} हैं।"

    # JSON Report
    sentiment_report = {
        "Company": company.capitalize(),
        "Articles": sorted(data_list, key=lambda x: x["Article Number"]), 
        "Sentiment Distribution": sentiment_counts,
        "Comparative Sentiment Score": {
            "Sentiment Distribution": sentiment_counts,
            "Coverage Differences": comparisons
        },
        "Final Sentiment Analysis": final_analysis,  
        "Audio": f"[Play Hindi Speech]({audio_path})"
    }

    # Save JSON report
    with open(output_json, "w", encoding="utf-8") as json_file:
        json.dump(sentiment_report, json_file, ensure_ascii=False, indent=4)

    return output_json

# Generate Hindi TTS
def generate_tts(company):
    """Creates Hindi TTS audio for sentiment analysis."""
    
    dir_path = f"data/{company}_articles"
    json_path = f"{dir_path}/{company}_articles_sentiment.json"
    tts_path = f"{dir_path}/{company}_sentiment_hindi.mp3"

    with open(json_path, "r", encoding="utf-8") as f:
        sentiment_data = json.load(f)

    sentiment_text = (
        f"{company} की हाल की खबरें ज्यादातर {max(sentiment_data['Sentiment Distribution'], key=sentiment_data['Sentiment Distribution'].get)} हैं। "
        f"कुल {sentiment_data['Sentiment Distribution']['Positive']} सकारात्मक, "
        f"{sentiment_data['Sentiment Distribution']['Negative']} नकारात्मक, "
        f"और {sentiment_data['Sentiment Distribution']['Neutral']} तटस्थ लेख मिले।"
    )

    tts = gTTS(sentiment_text, lang="hi", slow=False)
    tts.save(tts_path)

    return tts_path