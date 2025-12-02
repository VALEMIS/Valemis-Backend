# Valemis Backend - Twitter Sentiment Analysis API

Django REST API untuk scraping Twitter/X dan analisis sentiment berbahasa Indonesia & Inggris.

## Features

- ✅ Scraping tweets menggunakan Twitter API v2 (Tweepy)
- ✅ Sentiment analysis untuk Bahasa Indonesia (via translation + VADER)
- ✅ Sentiment analysis untuk English (VADER)
- ✅ Auto language detection
- ✅ Comprehensive account analysis dengan statistik

## API Endpoints

### 1. Health Check
```bash
GET /api/twitter/health/
```

Response:
```json
{
  "status": "ok",
  "message": "Twitter Scraper API is running",
  "timestamp": "2025-12-02T09:34:08.397537+00:00"
}
```

### 2. Analyze Account
```bash
POST /api/twitter/analyze-account/
Content-Type: application/json

{
  "username": "twitter_username",
  "max_tweets": 20,
  "days": 7
}
```

Response:
```json
{
  "status": "success",
  "data": {
    "username": "username",
    "analyzed_at": "2025-12-02T09:34:08Z",
    "total_tweets": 20,
    "sentiment_distribution": {
      "positive": {"count": 10, "percentage": 50.0},
      "neutral": {"count": 5, "percentage": 25.0},
      "negative": {"count": 5, "percentage": 25.0}
    },
    "average_score": 0.15,
    "overall_sentiment": "POSITIVE",
    "conclusion": "Account @username cenderung posting tweets dengan sentimen positif",
    "tweets": [
      {
        "tweet_id": "123456789",
        "text": "Tweet content...",
        "created_at": "2025-12-02T00:00:00Z",
        "likes_count": 100,
        "retweets_count": 50,
        "replies_count": 10,
        "url": "https://x.com/username/status/123456789",
        "sentiment": "positive",
        "score": 0.85,
        "language": "id",
        "details": {
          "positive": 0.85,
          "neutral": 0.15,
          "negative": 0.0
        }
      }
    ]
  }
}
```

## Setup

### 1. Clone & Install
```bash
cd /Users/fabian/Code/valemis/valemis-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Twitter API
Buat file `.env`:
```bash
TWITTER_BEARER_TOKEN=your_bearer_token_here
```

Dapatkan Bearer Token dari: https://developer.twitter.com/en/portal/dashboard

### 3. Run Server
```bash
python manage.py runserver
```

Server berjalan di: `http://localhost:8000`

## Testing

```bash
# Health check
curl http://localhost:8000/api/twitter/health/

# Analyze account
curl -X POST http://localhost:8000/api/twitter/analyze-account/ \
  -H "Content-Type: application/json" \
  -d '{"username": "elonmusk", "max_tweets": 10}'
```

## Project Structure

```
valemis-backend/
├── twitter_scraper/
│   ├── services/
│   │   ├── scraper.py              # Twitter API v2 scraper (Tweepy)
│   │   ├── sentiment_analyzer.py   # Multi-language sentiment
│   │   └── indonesian_sentiment.py # Indonesian lexicon analyzer
│   ├── views.py                    # API endpoints
│   └── urls.py                     # URL routing
├── valemis_backend/
│   ├── settings.py                 # Django settings
│   └── urls.py                     # Main URL config
├── manage.py
├── requirements.txt
└── .env                            # API credentials (gitignored)
```

## Dependencies

- **Django 4.2.7** - Web framework
- **djangorestframework** - REST API
- **tweepy** - Twitter API v2 client
- **vaderSentiment** - English sentiment analysis
- **deep-translator** - Indonesian translation for sentiment

## Rate Limits

Twitter API v2 Free Tier:
- **Essential**: 500K tweets/month
- **Elevated**: 2M tweets/month
- Max 100 tweets per request
- Max 300 requests per 15 minutes

## Tech Stack

- Python 3.9.6
- Django 4.2.7
- Twitter API v2
- VADER Sentiment Analysis
- Google Translate (deep-translator)

## Notes

- Twitter API credentials required (Bearer Token)
- Free tier has rate limits
- Indonesian sentiment via translation + VADER
- Real-time scraping (no database storage)
