"""
Twitter/X Scraper Service

Menggunakan Twitter API v2 dengan Tweepy untuk scraping tweets.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
import os

logger = logging.getLogger(__name__)


class TwitterScraper:
    """Service untuk scraping tweets dari Twitter/X"""
    
    def __init__(self):
        self.max_tweets = 100
        self.default_days = 7
        
        # Try to initialize Tweepy if credentials available
        self.use_api = False
        self.tweepy_client = None
        
        try:
            api_key = os.getenv('TWITTER_API_KEY')
            api_secret = os.getenv('TWITTER_API_SECRET')
            bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
            
            if api_key and api_secret:
                import tweepy
                
                # Twitter API v2 with Bearer Token (recommended)
                if bearer_token:
                    self.tweepy_client = tweepy.Client(bearer_token=bearer_token)
                    self.use_api = True
                    logger.info("Using Twitter API v2 with Bearer Token")
                else:
                    # Try OAuth 1.0a
                    self.tweepy_client = tweepy.Client(
                        consumer_key=api_key,
                        consumer_secret=api_secret
                    )
                    self.use_api = True
                    logger.info("Using Twitter API v2 with OAuth 1.0a")
                    
        except Exception as e:
            logger.warning(f"Failed to initialize Twitter API, will use snscrape: {str(e)}")
            self.use_api = False
    
    def scrape_by_username(
        self,
        username: str,
        days: int = None,
        max_tweets: int = None
    ) -> List[Dict]:
        """
        Scrape tweets dari username tertentu
        
        Args:
            username: Twitter username (tanpa @)
            days: Jumlah hari ke belakang
            max_tweets: Maksimum tweets yang akan di-scrape
            
        Returns:
            List of tweet dictionaries
        """
        days = days or self.default_days
        max_tweets = max_tweets or self.max_tweets
        
        # Remove @ if present
        username = username.lstrip('@')
        
        # ONLY use Twitter API - NO FALLBACK TO SNSCRAPE
        if not self.use_api or not self.tweepy_client:
            raise Exception("Twitter API is not configured. Please provide valid API credentials.")
        
        return self._scrape_with_api(username, max_tweets)
    
    def _scrape_with_api(self, username: str, max_tweets: int) -> List[Dict]:
        """
        Scrape tweets menggunakan Twitter API v2
        
        Args:
            username: Twitter username
            max_tweets: Maximum number of tweets
            
        Returns:
            List of tweet dictionaries
        """
        tweets = []
        
        try:
            # Get user ID first
            user = self.tweepy_client.get_user(username=username)
            if not user or not user.data:
                raise Exception(f"User @{username} not found")
            
            user_id = user.data.id
            user_name = user.data.username
            user_display_name = user.data.name
            
            logger.info(f"Found user: @{user_name} (ID: {user_id})")
            
            # Get user tweets with tweet fields
            response = self.tweepy_client.get_users_tweets(
                id=user_id,
                max_results=min(max_tweets, 100),  # API limit is 100 per request
                tweet_fields=['created_at', 'public_metrics', 'text'],
                exclude=['retweets', 'replies']  # Optional: exclude RTs and replies
            )
            
            if response.data:
                for tweet in response.data:
                    metrics = tweet.public_metrics
                    
                    tweet_data = {
                        'tweet_id': str(tweet.id),
                        'username': user_name,
                        'user_display_name': user_display_name,
                        'text': tweet.text,
                        'created_at': tweet.created_at,
                        'likes_count': metrics.get('like_count', 0),
                        'retweets_count': metrics.get('retweet_count', 0),
                        'replies_count': metrics.get('reply_count', 0),
                        'url': f"https://x.com/{user_name}/status/{tweet.id}",
                    }
                    
                    tweets.append(tweet_data)
                
                logger.info(f"Successfully scraped {len(tweets)} tweets using Twitter API")
            else:
                logger.warning(f"No tweets found for user @{username}")
                
        except Exception as e:
            logger.error(f"Error scraping with Twitter API: {str(e)}")
            raise Exception(f"Failed to scrape tweets with Twitter API: {str(e)}")
        
        return tweets
