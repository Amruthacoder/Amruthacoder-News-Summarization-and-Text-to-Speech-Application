from fastapi import FastAPI
from fastapi.responses import FileResponse
import utils
import json
import os

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to News Sentiment Analysis API!"}

# 📌 **Scrape news for a company**
@app.get("/scrape_news/{company}")
def scrape_news(company: str):
    urls = {
        "apple": [
            "https://appleinsider.com/articles/25/01/29/apple-vision-pro-review-one-year-later-time-to-exit-the-preview",
            "https://appleinsider.com/articles/25/03/11/m4-macbook-air-review-roundup-welcome-upgrade-but-no-surprises",
            "https://appleinsider.com/articles/25/03/12/iphone-16e-review-all-the-bells-none-of-the-whistles-on-this-battery-heavy-device",
            "https://appleinsider.com/inside/iphone-16e/vs/iphone-16e-vs-iphone-16-a-new-apple-intelligence-powered-entry-level-option",
            "https://appleinsider.com/articles/25/03/18/pebbles-new-smartwatches-take-on-apple-watch-with-longer-battery-life",
            "https://appleinsider.com/articles/25/03/11/rumored-ios-19-macos-16-design-changes-will-be-polarizing-as-always",
            "https://appleinsider.com/articles/25/01/24/airpods-4---four-month-review-the-best-apple-earbuds-for-most-people",
            "https://appleinsider.com/inside/iphone-16e/vs/iphone-16e-vs-iphone-se-3-a-quantum-leap-forward",
            "https://appleinsider.com/articles/25/03/05/new-m4-macbook-air-fixes-the-lines-biggest-problem",
            "https://appleinsider.com/articles/25/01/14/apple-watch-series-10-three-month-review-iterative-isnt-a-bad-word"
        ],
        "samsung": [
            "https://www.cnet.com/tech/computing/i-tried-google-and-samsungs-next-gen-android-xr-headsets-and-glasses-and-the-killer-app-is-ai/",
            "https://www.theverge.com/2025/1/22/24349736/samsung-project-moohan-photos-android-xr-headset",
            "https://www.digitaltrends.com/computing/samsung-xr-headset-display/",
            "https://www.techradar.com/computing/virtual-reality-augmented-reality/samsungs-android-xr-headset-could-avoid-the-apple-vision-pros-biggest-mistake-according-to-this-leak",
            "https://www.gizmodo.com/samsungs-project-moohan-vision-pros-best-features-2000555771",
            "https://www.theverge.com/2024/12/12/24319528/google-android-xr-samsung-project-moohan-smart-glasses?utm_source=chatgpt.com",
            "https://www.tomsguide.com/computing/vr-ar/samsungs-project-moohan-could-have-better-displays-than-apple-vision-pro-heres-how",
            "https://news.samsung.com/global/unlock-the-infinite-possibilities-of-xr-with-galaxy-ai",
            "https://www.provideocoalition.com/project-moohan-samsungs-xr-headset-launches-this-year/",
            "https://www.nbcnewyork.com/news/business/money-report/samsung-to-launch-its-apple-vision-pro-rival-headset-this-year/6172201/"
        ]
    }

    company = company.lower()
    if company not in urls:
        return {"status": "error", "message": "Company not found"}

    # ✅ Scrape articles
    utils.scrape_articles(company, urls[company])

    articles_txt_path = f"data/{company}_articles/{company}_articles.txt"
    if not os.path.exists(articles_txt_path):
        return {"error": f"Scraping completed, but no articles file found for {company}!"}

    # ✅ Process articles
    process_result = utils.process_articles(company)
    if isinstance(process_result, dict) and "error" in process_result:
        return {"status": "error", "message": process_result["error"]}

    return {"status": "success", "company": company, "articles_scraped": len(urls[company])}

@app.get("/get_news/{company}")
def get_news(company: str):
    json_path = f"data/{company.lower()}_articles/{company.lower()}_articles_sentiment.json"

    if not os.path.exists(json_path):
        return {"error": f"No sentiment report found for {company}. Run `/scrape_news/{company}` first."}

    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)
    
# 📌 **Get Hindi TTS sentiment audio**
@app.get("/get_tts/{company}", response_class=FileResponse)
def get_tts(company: str):
    """Generate and return Hindi TTS sentiment analysis for the given company."""
    
    tts_path = f"data/{company.lower()}_articles/{company.lower()}_sentiment_hindi.mp3"

    if not os.path.exists(tts_path):
        print(f"🔄 Generating TTS for {company}...")
        tts_result = utils.generate_tts(company.lower())

        if isinstance(tts_result, dict) and "error" in tts_result:
            return {"error": tts_result["error"]}

    return FileResponse(tts_path, media_type="audio/mpeg", headers={"Content-Disposition": "inline"})