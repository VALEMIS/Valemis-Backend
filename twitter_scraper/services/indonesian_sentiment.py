"""
Indonesian Sentiment Analysis Service

Multi-layer approach untuk analisis sentiment bahasa Indonesia:
1. Lexicon-based (fast, offline)
2. Translation + VADER (fallback)
3. Pre-trained Indonesian model (most accurate)
"""

from typing import Dict, Tuple
import re
import logging

logger = logging.getLogger(__name__)


class IndonesianLexiconAnalyzer:
    """
    Lexicon-based sentiment analyzer untuk bahasa Indonesia
    Menggunakan kamus kata positif dan negatif
    """
    
    def __init__(self):
        # Kata-kata positif dalam bahasa Indonesia  
        self.positive_words = {
            'bagus', 'baik', 'hebat', 'luar biasa', 'sempurna', 'mantap',
            'keren', 'sukses', 'berhasil', 'memuaskan', 'senang', 'gembira',
            'suka', 'cinta', 'sayang', 'indah', 'cantik', 'menakjubkan',
            'membantu', 'bermanfaat', 'positif', 'optimis', 'maju', 'berkembang',
            'meningkat', 'untung', 'profit', 'keuntungan', 'pertumbuhan',
            'inovasi', 'kreatif', 'produktif', 'efisien', 'efektif',
            'terima kasih', 'terimakasih', 'thanks', 'makasih', 'recommended',
            'berkualitas', 'terpercaya', 'profesional', 'ramah', 'cepat',
            'mudah', 'nyaman', 'aman', 'lengkap', 'modern', 'canggih',
            'cemerlang', 'gemilang', 'brilian', 'pintar', 'cerdas',
            'peduli', 'perhatian', 'responsif', 'solid', 'kuat', 'tangguh',
            'menyenangkan', 'menghibur', 'seru', 'asyik', 'wow', 'amazing',
            # Added words for business/employment context
            'membuka', 'buka', 'meluncurkan', 'launch', 'ekspansi',
            'lapangan', 'kerja', 'pekerjaan', 'lowongan', 'rekrutmen',
            'naik', 'pertumbuhan', 'peningkatan', 'kenaikan', 'signifikan',
            'cerah', 'terang', 'jelas', 'transparan', 'terbuka'
        }
        
        # Kata-kata negatif dalam bahasa Indonesia
        self.negative_words = {
            'buruk', 'jelek', 'gagal', 'rugi', 'kerugian', 'merugi',
            'bangkrut', 'gulung tikar', 'bubar', 'tutup', 'collapse',
            'kecewa', 'mengecewakan', 'sedih', 'marah', 'kesal', 'jengkel',
            'benci', 'tidak suka', 'bosan', 'boring', 'lambat', 'lelet',
            'susah', 'sulit', 'ribet', 'rumit', 'berbelit', 'complicated',
            'mahal', 'overpriced', 'tidak worth', 'zonk', 'mengecewakan',
            'sampah', 'jelek', 'payah', 'parah', 'hancur', 'rusak',
            'error', 'bug', 'bermasalah', 'trouble', 'problem', 'issue',
            'mengerikan', 'ngeri', 'serem', 'menakutkan', 'bahaya',
            'korupsi', 'korup', 'curang', 'penipuan', 'tipu', 'bohong',
            'tidak jujur', 'tidak amanah', 'tidak profesional',
            'tidak bertanggung jawab', 'tidak peduli', 'acuh',
            'lambat', 'telat', 'terlambat', 'delay', 'pending',
            'reject', 'ditolak', 'gagal', 'fail', 'minus', 'negatif',
            'menurun', 'turun', 'jatuh', 'drop', 'anjlok',
            'krisis', 'resesi', 'defisit', 'hutang', 'utang',
            'polusi', 'pencemaran', 'kerusakan', 'merusak', 'destroy',
            # Added words for business/employment context
            'phk', 'pecat', 'dipecat', 'pemecatan', 'dikeluarkan',
            'pengurangan', 'cut', 'pemangkasan', 'kinerja', 'menurun',
            'drastis', 'tajam', 'merosot', 'ambruk', 'macet',
            'harusnya', 'seharusnya'  # Often used with negative context
        }        # Kata-kata intensifier (penguat)
        self.intensifiers = {
            'sangat': 1.5, 'amat': 1.5, 'banget': 1.8, 'sekali': 1.5,
            'benar-benar': 1.7, 'sungguh': 1.5, 'paling': 1.6,
            'super': 1.7, 'ultra': 1.8, 'extra': 1.5,
            'terlalu': 1.4, 'agak': 0.5, 'kurang': 0.5, 'cukup': 0.7,
            'lumayan': 0.6, 'rada': 0.5
        }
        
        # Kata negasi
        self.negations = {
            'tidak', 'bukan', 'jangan', 'belum', 'tak', 'gak', 'nggak',
            'enggak', 'ga', 'ngga', 'ngg', 'ndak', 'kagak'
        }
    
    def _preprocess(self, text: str) -> str:
        """Preprocessing text"""
        text = text.lower()
        # Remove URLs
        text = re.sub(r'http\S+|www.\S+', '', text)
        # Remove mentions
        text = re.sub(r'@\w+', '', text)
        # Remove hashtags (keep the word)
        text = re.sub(r'#', '', text)
        return text
    
    def _tokenize(self, text: str) -> list:
        """Simple tokenization"""
        # Split by whitespace and punctuation
        tokens = re.findall(r'\w+', text)
        return tokens
    
    def analyze(self, text: str) -> Dict:
        """
        Analyze sentiment menggunakan lexicon-based approach
        
        Returns:
            Dictionary dengan sentiment, score, dan details
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
                'method': 'lexicon'
            }
        
        # Preprocess
        processed_text = self._preprocess(text)
        tokens = self._tokenize(processed_text)
        
        if not tokens:
            return {
                'sentiment': 'neutral',
                'score': 0.0,
                'details': {
                    'positive': 0.0,
                    'neutral': 1.0,
                    'negative': 0.0
                },
                'method': 'lexicon'
            }
        
        # Calculate sentiment
        positive_score = 0.0
        negative_score = 0.0
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            # Check for intensifier
            intensifier = 1.0
            if token in self.intensifiers:
                intensifier = self.intensifiers[token]
                i += 1
                if i >= len(tokens):
                    break
                token = tokens[i]
            
            # Check for negation
            negated = False
            if token in self.negations:
                negated = True
                i += 1
                if i >= len(tokens):
                    break
                token = tokens[i]
            
            # Check sentiment
            if token in self.positive_words:
                score = 1.0 * intensifier
                if negated:
                    negative_score += score  # negated positive = negative
                else:
                    positive_score += score
            elif token in self.negative_words:
                score = 1.0 * intensifier
                if negated:
                    positive_score += score  # negated negative = positive
                else:
                    negative_score += score
            
            i += 1
        
        # Normalize scores
        total_score = positive_score + negative_score
        
        if total_score == 0:
            # No sentiment words found
            return {
                'sentiment': 'neutral',
                'score': 0.0,
                'details': {
                    'positive': 0.0,
                    'neutral': 1.0,
                    'negative': 0.0
                },
                'method': 'lexicon'
            }
        
        # Calculate percentages
        pos_pct = positive_score / total_score
        neg_pct = negative_score / total_score
        
        # Calculate compound score (-1 to 1)
        compound = (positive_score - negative_score) / total_score
        
        # Determine sentiment category
        if compound >= 0.1:
            sentiment = 'positive'
        elif compound <= -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            'sentiment': sentiment,
            'score': round(compound, 4),
            'details': {
                'positive': round(pos_pct, 4),
                'neutral': round(1 - pos_pct - neg_pct, 4) if pos_pct + neg_pct < 1 else 0.0,
                'negative': round(neg_pct, 4)
            },
            'method': 'lexicon',
            'word_counts': {
                'positive_words': int(positive_score),
                'negative_words': int(negative_score)
            }
        }


class TranslationBasedAnalyzer:
    """
    Sentiment analyzer dengan translation ke bahasa Inggris
    Fallback method jika lexicon tidak confident
    """
    
    def __init__(self):
        try:
            from deep_translator import GoogleTranslator
            self.translator = GoogleTranslator(source='id', target='en')
            self.available = True
        except ImportError:
            logger.warning("deep-translator not installed. Translation method unavailable.")
            self.available = False
        
        # Import VADER
        try:
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
            self.vader = SentimentIntensityAnalyzer()
        except ImportError:
            logger.error("vaderSentiment not installed")
            self.vader = None
    
    def analyze(self, text: str) -> Dict:
        """Translate to English then analyze with VADER"""
        if not self.available or not self.vader:
            return None
        
        try:
            # Translate to English
            translated = self.translator.translate(text)
            
            # Analyze with VADER
            scores = self.vader.polarity_scores(translated)
            compound = scores['compound']
            
            # Determine sentiment
            if compound >= 0.05:
                sentiment = 'positive'
            elif compound <= -0.05:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            return {
                'sentiment': sentiment,
                'score': compound,
                'details': {
                    'positive': scores['pos'],
                    'neutral': scores['neu'],
                    'negative': scores['neg']
                },
                'method': 'translation+vader',
                'translated_text': translated
            }
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            return None


class HybridIndonesianSentimentAnalyzer:
    """
    Hybrid analyzer yang menggabungkan multiple methods
    untuk hasil terbaik
    """
    
    def __init__(self, method: str = 'hybrid'):
        """
        Initialize analyzer
        
        Args:
            method: 'lexicon', 'translation', 'hybrid', or 'auto'
        """
        self.method = method
        self.lexicon_analyzer = IndonesianLexiconAnalyzer()
        self.translation_analyzer = TranslationBasedAnalyzer()
    
    def analyze(self, text: str) -> Dict:
        """
        Analyze sentiment dengan hybrid approach
        
        Returns:
            Dictionary dengan sentiment analysis result
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
                'method': 'none'
            }
        
        # Method 1: Lexicon-based (fast, always run)
        lexicon_result = self.lexicon_analyzer.analyze(text)
        
        if self.method == 'lexicon':
            return lexicon_result
        
        # Method 2: Translation-based (if available)
        translation_result = None
        if self.method in ['translation', 'hybrid', 'auto']:
            translation_result = self.translation_analyzer.analyze(text)
        
        if self.method == 'translation':
            return translation_result if translation_result else lexicon_result
        
        # Hybrid: Combine results
        if self.method == 'hybrid' and translation_result:
            # Average the scores
            combined_score = (lexicon_result['score'] + translation_result['score']) / 2
            
            # Determine sentiment from combined score
            if combined_score >= 0.1:
                sentiment = 'positive'
            elif combined_score <= -0.1:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            return {
                'sentiment': sentiment,
                'score': round(combined_score, 4),
                'details': {
                    'positive': round((lexicon_result['details']['positive'] + 
                                     translation_result['details']['positive']) / 2, 4),
                    'neutral': round((lexicon_result['details']['neutral'] + 
                                    translation_result['details']['neutral']) / 2, 4),
                    'negative': round((lexicon_result['details']['negative'] + 
                                     translation_result['details']['negative']) / 2, 4)
                },
                'method': 'hybrid',
                'lexicon_result': lexicon_result,
                'translation_result': translation_result
            }
        
        # Auto: Use lexicon as primary, translation as validation
        if self.method == 'auto':
            # If lexicon is confident (score > 0.3), use it
            if abs(lexicon_result['score']) > 0.3:
                return lexicon_result
            
            # Otherwise, use translation if available
            if translation_result:
                return translation_result
        
        # Default: return lexicon result
        return lexicon_result
