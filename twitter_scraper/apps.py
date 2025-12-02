from django.apps import AppConfig


class TwitterScraperConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'twitter_scraper'
    verbose_name = 'Twitter Scraper & Sentiment Analysis'
