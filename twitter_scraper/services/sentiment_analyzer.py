"""
Sentiment Analysis Service

Multi-language sentiment analyzer:
- Indonesian: Lexicon-based + Translation
- English: VADER + TextBlob
"""

from typing import Dict
import logging
import re

# Import Indonesian analyzer
from .indonesian_sentiment import HybridIndonesianSentimentAnalyzer

# Import English analyzers
try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    VADER_AVAILABLE = True
except ImportError:
    VADER_AVAILABLE = False

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """
    Multi-language sentiment analyzer
    Auto-detect language and use appropriate method
    """
    
    def __init__(self, method: str = 'auto', language: str = 'auto'):
        """
        Initialize sentiment analyzer
        
        Args:
            method: 'auto', 'lexicon', 'hybrid', 'vader', 'textblob'
            language: 'auto', 'id' (Indonesian), 'en' (English)
        """
        self.method = method
        self.language = language
        
        # Initialize Indonesian analyzer
        self.indonesian_analyzer = HybridIndonesianSentimentAnalyzer(
            method='hybrid' if method == 'auto' else method
        )
        
        # Initialize English analyzers
        if VADER_AVAILABLE and method in ['vader', 'both', 'auto']:
            self.vader_analyzer = SentimentIntensityAnalyzer()
        else:
            self.vader_analyzer = None
    
    def _detect_language(self, text: str) -> str:
        """
        Simple language detection
        Returns 'id' for Indonesian, 'en' for English
        """
        # Common Indonesian words and patterns
        indonesian_indicators = [
            # Common particles & conjunctions
            'yang', 'adalah', 'dengan', 'untuk', 'tidak', 'ini', 'itu',
            'dari', 'di', 'ke', 'pada', 'atau', 'dan', 'juga', 'akan',
            'telah', 'sudah', 'belum', 'sangat', 'banget', 'sekali',
            'saja', 'hanya', 'bisa', 'dapat', 'harus', 'mau', 'ingin',
            # Company/location specific
            'indonesia', 'perusahaan', 'karyawan', 'lapangan', 'kerja',
            # Verbs
            'membuka', 'menurun', 'meningkat', 'berkembang',
            # Time markers
            'hari', 'bulan', 'tahun', 'minggu',
            # Common words
            'baru', 'lama', 'banyak', 'sedikit', 'besar', 'kecil',
            'baik', 'buruk', 'bagus', 'jelek', 'rugi', 'untung',
            'naik', 'turun', 'bubar', 'tutup', 'buka',
            # Prefix indicators (me-, ber-, pe-, ter-)
            'kinerja', 'harga', 'saham', 'phk', 'cuaca', 'cerah'
        ]
        
        text_lower = text.lower()
        words = re.findall(r'\w+', text_lower)
        
        if not words:
            return 'en'  # default to English
        
        # Count Indonesian indicators
        id_count = sum(1 for word in words if word in indonesian_indicators)
        
        # Check for Indonesian prefixes (me-, ber-, pe-, ter-, ke-, se-)
        prefix_pattern = r'\b(me|ber|pe|ter|ke|se)[a-z]{3,}\b'
        prefix_matches = len(re.findall(prefix_pattern, text_lower))
        
        # If any Indonesian indicators found OR has Indonesian prefixes, treat as Indonesian
        # Lower threshold to 5% or at least 1 indicator
        if len(words) > 0 and ((id_count / len(words)) > 0.05 or id_count >= 1 or prefix_matches >= 1):
            return 'id'
        
        return 'en'
    
    def analyze(self, text: str) -> Dict:
        """
        Analyze sentiment dari text with auto language detection
        
        Args:
            text: Text yang akan dianalisis
            
        Returns:
            Dictionary dengan hasil sentiment analysis
        """
        if not text or not text.strip():
            return {
                'sentiment': 'neutral',
                'score': 0.0,
                'details': {
                    'positive': 0.0,
                    'neutral': 1.0,
                    'negative': 0.0
                },
                'language': 'unknown'
            }
        
        # Detect language if auto
        detected_lang = self.language
        if self.language == 'auto':
            detected_lang = self._detect_language(text)
        
        # Use appropriate analyzer based on language
        if detected_lang == 'id':
            result = self.indonesian_analyzer.analyze(text)
            result['language'] = 'id'
            return result
        else:
            # Use English analyzers
            if self.method == 'vader' and self.vader_analyzer:
                result = self._analyze_vader(text)
            elif self.method == 'textblob' and TEXTBLOB_AVAILABLE:
                result = self._analyze_textblob(text)
            else:  # auto or both
                if self.vader_analyzer:
                    result = self._analyze_vader(text)
                elif TEXTBLOB_AVAILABLE:
                    result = self._analyze_textblob(text)
                else:
                    # Fallback to Indonesian analyzer
                    result = self.indonesian_analyzer.analyze(text)
            
            result['language'] = 'en'
            return result
    
    def _analyze_vader(self, text: str) -> Dict:
        """
        Analyze sentiment menggunakan VADER
        
        VADER is specifically attuned to sentiments expressed in social media.
        It's good at handling:
        - Emoji and emoticons
        - Slang
        - Capitalization for emphasis
        - Punctuation for emphasis
        
        Args:
            text: Text to analyze
            
        Returns:
            Sentiment analysis result
        """
        try:
            scores = self.vader_analyzer.polarity_scores(text)
            
            # VADER returns: neg, neu, pos, compound
            # compound score: -1 (most negative) to +1 (most positive)
            compound_score = scores['compound']
            
            # Determine sentiment category
            if compound_score >= 0.05:
                sentiment = 'positive'
            elif compound_score <= -0.05:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            return {
                'sentiment': sentiment,
                'score': compound_score,
                'details': {
                    'positive': scores['pos'],
                    'neutral': scores['neu'],
                    'negative': scores['neg']
                }
            }
            
        except Exception as e:
            logger.error(f"Error in VADER analysis: {str(e)}")
            return {
                'sentiment': 'neutral',
                'score': 0.0,
                'details': {
                    'positive': 0.0,
                    'neutral': 1.0,
                    'negative': 0.0
                }
            }
    
    def _analyze_textblob(self, text: str) -> Dict:
        """
        Analyze sentiment menggunakan TextBlob
        
        TextBlob provides polarity score from -1 to 1:
        - polarity > 0: positive
        - polarity < 0: negative
        - polarity = 0: neutral
        
        Args:
            text: Text to analyze
            
        Returns:
            Sentiment analysis result
        """
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            # Determine sentiment category
            if polarity > 0.1:
                sentiment = 'positive'
            elif polarity < -0.1:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            # Convert polarity to positive/neutral/negative scores
            if polarity > 0:
                positive = polarity
                negative = 0
                neutral = 1 - polarity
            elif polarity < 0:
                positive = 0
                negative = abs(polarity)
                neutral = 1 - abs(polarity)
            else:
                positive = 0
                negative = 0
                neutral = 1.0
            
            return {
                'sentiment': sentiment,
                'score': polarity,
                'details': {
                    'positive': positive,
                    'neutral': neutral,
                    'negative': negative
                }
            }
            
        except Exception as e:
            logger.error(f"Error in TextBlob analysis: {str(e)}")
            return {
                'sentiment': 'neutral',
                'score': 0.0,
                'details': {
                    'positive': 0.0,
                    'neutral': 1.0,
                    'negative': 0.0
                }
            }
    
    def batch_analyze(self, texts: list) -> list:
        """
        Analyze sentiment untuk multiple texts
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            List of sentiment analysis results
        """
        results = []
        
        for text in texts:
            result = self.analyze(text)
            results.append(result)
        
        return results
    
    def get_statistics(self, results: list) -> Dict:
        """
        Calculate statistics dari batch analysis results
        
        Args:
            results: List of sentiment analysis results
            
        Returns:
            Statistics dictionary
        """
        if not results:
            return {
                'total': 0,
                'positive': 0,
                'neutral': 0,
                'negative': 0,
                'positive_percentage': 0.0,
                'neutral_percentage': 0.0,
                'negative_percentage': 0.0,
                'average_score': 0.0
            }
        
        total = len(results)
        positive_count = sum(1 for r in results if r['sentiment'] == 'positive')
        neutral_count = sum(1 for r in results if r['sentiment'] == 'neutral')
        negative_count = sum(1 for r in results if r['sentiment'] == 'negative')
        
        total_score = sum(r['score'] for r in results)
        average_score = total_score / total if total > 0 else 0.0
        
        return {
            'total': total,
            'positive': positive_count,
            'neutral': neutral_count,
            'negative': negative_count,
            'positive_percentage': round((positive_count / total) * 100, 2),
            'neutral_percentage': round((neutral_count / total) * 100, 2),
            'negative_percentage': round((negative_count / total) * 100, 2),
            'average_score': round(average_score, 4)
        }
