from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone

from .services.scraper import TwitterScraper
from .services.sentiment_analyzer import SentimentAnalyzer

import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
def health_check(request):
    """
    Simple health check endpoint
    """
    return Response({
        'status': 'ok',
        'message': 'Twitter Scraper API is running',
        'timestamp': timezone.now().isoformat()
    })


@api_view(['POST'])
def analyze_account(request):
    """
    Comprehensive endpoint untuk analyze Twitter account:
    - Scrape tweets dari account
    - Analyze sentiment untuk setiap tweet
    - Generate statistics dan conclusion
    
    Request body:
    {
        "username": "twitter_username",
        "max_tweets": 20,  // optional, default 20
        "days": 7  // optional, default 7
    }
    
    Response:
    {
        "status": "success",
        "data": {
            "username": "username",
            "analyzed_at": "2024-01-01T00:00:00Z",
            "total_tweets": 20,
            "sentiment_distribution": {
                "positive": {"count": 10, "percentage": 50.0},
                "neutral": {"count": 5, "percentage": 25.0},
                "negative": {"count": 5, "percentage": 25.0}
            },
            "average_score": 0.15,
            "overall_sentiment": "POSITIVE",
            "conclusion": "Account @username cenderung posting tweets dengan sentimen positif",
            "tweets": [...]
        }
    }
    """
    username = request.data.get('username', '').strip().replace('@', '')
    max_tweets = request.data.get('max_tweets', 20)
    days = request.data.get('days', 7)
    
    if not username:
        return Response({
            'status': 'error',
            'message': 'Username is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Initialize services
        scraper = TwitterScraper()
        analyzer = SentimentAnalyzer(method='auto', language='auto')
        
        logger.info(f"Scraping tweets from @{username}...")
        
        # Scrape tweets using Twitter API
        tweets_data = scraper.scrape_by_username(username, days=days, max_tweets=max_tweets)
        
        if not tweets_data:
            return Response({
                'status': 'error',
                'message': f'No tweets found for @{username}'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Analyze sentiment for each tweet
        results = []
        positive_count = 0
        neutral_count = 0
        negative_count = 0
        total_score = 0
        
        for tweet in tweets_data:
            text = tweet.get('text', '')
            
            # Analyze sentiment
            sentiment_result = analyzer.analyze(text)
            
            sentiment = sentiment_result['sentiment']
            score = sentiment_result['score']
            language = sentiment_result.get('language', 'unknown')
            
            # Count by sentiment
            if sentiment == 'positive':
                positive_count += 1
            elif sentiment == 'negative':
                negative_count += 1
            else:
                neutral_count += 1
            
            total_score += score
            
            # Store result
            result = {
                'tweet_id': tweet.get('tweet_id'),
                'text': text,
                'created_at': tweet.get('created_at'),
                'likes_count': tweet.get('likes_count', 0),
                'retweets_count': tweet.get('retweets_count', 0),
                'replies_count': tweet.get('replies_count', 0),
                'url': tweet.get('url', ''),
                'sentiment': sentiment,
                'score': round(score, 3),
                'language': language,
                'details': {
                    'positive': round(sentiment_result.get('details', {}).get('positive', 0), 3),
                    'neutral': round(sentiment_result.get('details', {}).get('neutral', 0), 3),
                    'negative': round(sentiment_result.get('details', {}).get('negative', 0), 3)
                }
            }
            results.append(result)
        
        # Calculate overall conclusion
        total_tweets = len(results)
        average_score = total_score / total_tweets if total_tweets > 0 else 0
        
        positive_pct = (positive_count / total_tweets * 100) if total_tweets > 0 else 0
        neutral_pct = (neutral_count / total_tweets * 100) if total_tweets > 0 else 0
        negative_pct = (negative_count / total_tweets * 100) if total_tweets > 0 else 0
        
        # Determine overall sentiment
        if average_score > 0.2:
            overall_sentiment = 'POSITIVE'
            conclusion = f"Account @{username} cenderung posting tweets dengan sentimen positif"
        elif average_score < -0.2:
            overall_sentiment = 'NEGATIVE'
            conclusion = f"Account @{username} cenderung posting tweets dengan sentimen negatif"
        else:
            overall_sentiment = 'NEUTRAL'
            conclusion = f"Account @{username} cenderung posting tweets dengan sentimen netral/seimbang"
        
        # Create response
        response_data = {
            'username': username,
            'analyzed_at': timezone.now().isoformat(),
            'total_tweets': total_tweets,
            'sentiment_distribution': {
                'positive': {
                    'count': positive_count,
                    'percentage': round(positive_pct, 2)
                },
                'neutral': {
                    'count': neutral_count,
                    'percentage': round(neutral_pct, 2)
                },
                'negative': {
                    'count': negative_count,
                    'percentage': round(negative_pct, 2)
                }
            },
            'average_score': round(average_score, 3),
            'overall_sentiment': overall_sentiment,
            'conclusion': conclusion,
            'tweets': results
        }
        
        logger.info(f"Successfully analyzed {total_tweets} tweets from @{username}")
        
        return Response({
            'status': 'success',
            'data': response_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error analyzing account @{username}: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Failed to analyze account: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
