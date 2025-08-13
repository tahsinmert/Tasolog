import json
import os
import sys
from http.server import BaseHTTPRequestHandler
import numpy as np

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import AI models and functions
try:
    from textblob import TextBlob
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    
    # Try to import transformers
    try:
        from transformers import pipeline
        sentiment_analyzer = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
        emotion_analyzer = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
        AI_MODELS_LOADED = True
    except Exception as e:
        print(f"AI model loading error: {e}")
        sentiment_analyzer = None
        emotion_analyzer = None
        AI_MODELS_LOADED = False
        
except ImportError as e:
    print(f"Import error: {e}")
    AI_MODELS_LOADED = False

def analyze_sentiment_advanced(text):
    """Gelişmiş duygu analizi"""
    results = {}
    
    # TextBlob analizi
    try:
        blob = TextBlob(text)
        results['textblob'] = {
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity
        }
    except Exception as e:
        results['textblob'] = {'polarity': 0, 'subjectivity': 0}
    
    # VADER analizi
    try:
        vader = SentimentIntensityAnalyzer()
        vader_scores = vader.polarity_scores(text)
        results['vader'] = vader_scores
    except Exception as e:
        results['vader'] = {'compound': 0, 'pos': 0, 'neg': 0, 'neu': 0}
    
    # Transformers analizi
    if AI_MODELS_LOADED and sentiment_analyzer:
        try:
            sentiment_result = sentiment_analyzer(text)[0]
            results['transformers_sentiment'] = {
                'label': sentiment_result['label'],
                'score': sentiment_result['score']
            }
        except Exception as e:
            results['transformers_sentiment'] = {'label': 'neutral', 'score': 0.5}
    
    # Emotion analizi
    if AI_MODELS_LOADED and emotion_analyzer:
        try:
            emotion_result = emotion_analyzer(text)[0]
            results['emotion'] = {
                'label': emotion_result['label'],
                'score': emotion_result['score']
            }
        except Exception as e:
            results['emotion'] = {'label': 'neutral', 'score': 0.5}
    
    # Text analizi
    try:
        words = text.split()
        sentences = text.split('.')
        unique_words = set(words)
        
        results['text_analysis'] = {
            'word_count': len(words),
            'sentence_count': len([s for s in sentences if s.strip()]),
            'unique_words': len(unique_words),
            'lexical_diversity': len(unique_words) / len(words) if words else 0,
            'avg_sentence_length': len(words) / len([s for s in sentences if s.strip()]) if sentences else 0
        }
    except Exception as e:
        results['text_analysis'] = {
            'word_count': 0,
            'sentence_count': 0,
            'unique_words': 0,
            'lexical_diversity': 0,
            'avg_sentence_length': 0
        }
    
    return results

def get_psychological_advice(sentiment_results):
    """Psikolojik tavsiye"""
    PSYCHOLOGICAL_ADVICE = {
        'positive': [
            "Pozitif duygularınızı paylaşarak başkalarına da ilham verebilirsiniz.",
            "Bu pozitif enerjiyi fiziksel aktivitelere yönlendirmeyi deneyin.",
            "Pozitif düşüncelerinizi günlük tutarak kaydetmeyi deneyin."
        ],
        'negative': [
            "Profesyonel destek almayı düşünebilirsiniz.",
            "Küçük adımlarla başlayın. Her gün bir iyilik yapmayı deneyin.",
            "Sosyal bağlarınızı güçlendirin. Güvendiğiniz insanlarla konuşmak size destek olacaktır."
        ],
        'neutral': [
            "Bu dengeyi korumaya çalışın. Meditasyon veya hafif egzersizler ruh halinizi destekleyebilir.",
            "Bu sakin dönemi yaratıcı projeler için kullanmayı deneyin.",
            "Düşüncelerinizi yazıya dökmeyi deneyin. Bu size netlik kazandırabilir."
        ]
    }
    
    advice = []
    vader_compound = sentiment_results.get('vader', {}).get('compound', 0)
    
    if vader_compound > 0.2:
        advice.append(np.random.choice(PSYCHOLOGICAL_ADVICE['positive']))
    elif vader_compound < -0.2:
        advice.append(np.random.choice(PSYCHOLOGICAL_ADVICE['negative']))
    else:
        advice.append(np.random.choice(PSYCHOLOGICAL_ADVICE['neutral']))
    
    return advice[:3]

def generate_insights(sentiment_results):
    """İçgörüler üret"""
    insights = []
    
    vader_compound = sentiment_results.get('vader', {}).get('compound', 0)
    
    if vader_compound > 0.5:
        insights.append("Duygularınız oldukça yoğun. Bu, duruma derinden bağlı olduğunuzu gösteriyor.")
    elif vader_compound < -0.5:
        insights.append("Duygusal yoğunluğunuz yüksek. Bu, üzerinde durulması gereken bir konu olabilir.")
    
    if sentiment_results.get('textblob', {}).get('subjectivity', 0) > 0.7:
        insights.append("Yazınız oldukça öznel. Bu, kişisel deneyimlerinizin önemli olduğunu gösteriyor.")
    
    return insights[:3]

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        try:
            # Get request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            text = data.get('text', '').strip()
            
            if not text:
                response = {'error': 'Lütfen bir metin girin'}
            elif len(text) < 10:
                response = {'error': 'Lütfen daha detaylı bir açıklama yazın (en az 10 karakter)'}
            else:
                # Analyze sentiment
                sentiment_results = analyze_sentiment_advanced(text)
                
                # Get advice and insights
                advice = get_psychological_advice(sentiment_results)
                insights = generate_insights(sentiment_results)
                
                # Format response
                response = {
                    'text': text,
                    'analysis': sentiment_results,
                    'advice': advice,
                    'insights': insights,
                    'summary': {
                        'overall_sentiment': 'positive' if sentiment_results.get('vader', {}).get('compound', 0) > 0.1 else 'negative' if sentiment_results.get('vader', {}).get('compound', 0) < -0.1 else 'neutral',
                        'confidence': abs(sentiment_results.get('vader', {}).get('compound', 0)),
                        'emotion': sentiment_results.get('emotion', {}).get('label', 'unknown'),
                        'ai_models_loaded': AI_MODELS_LOADED
                    }
                }
            
        except Exception as e:
            response = {'error': f'Analiz sırasında hata oluştu: {str(e)}'}
        
        # Send response
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        # Health check endpoint
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            'status': 'healthy',
            'ai_models_loaded': AI_MODELS_LOADED,
            'models': {
                'sentiment': AI_MODELS_LOADED,
                'emotion': AI_MODELS_LOADED,
                'turkish': AI_MODELS_LOADED,
                'embedding': AI_MODELS_LOADED
            }
        }
        
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
