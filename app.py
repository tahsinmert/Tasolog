from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import numpy as np
import pandas as pd
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)

# Gelişmiş AI modellerini yükle
print("🤖 AI modelleri yükleniyor...")

try:
    from transformers import pipeline
    
    # Duygu analizi modelleri
    sentiment_analyzer = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
    emotion_analyzer = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
    
    print("✅ AI modelleri başarıyla yüklendi!")
    AI_MODELS_LOADED = True
    
except Exception as e:
    print(f"⚠️ AI model yükleme hatası: {e}")
    print("📝 Temel duygu analizi kullanılacak")
    AI_MODELS_LOADED = False
    sentiment_analyzer = None
    emotion_analyzer = None

# Temel analiz araçları
vader_analyzer = SentimentIntensityAnalyzer()

# Gelişmiş psikolojik tavsiye veritabanı - Daha çeşitli ve akıllı
PSYCHOLOGICAL_ADVICE = {
    'positive': [
        "Harika! Pozitif düşüncelerinizi korumaya devam edin. Bu ruh haliniz hem sizin hem de çevrenizdeki insanlar için çok değerli.",
        "Pozitif enerjiniz gerçekten etkileyici. Bu enerjiyi yaratıcı projelerde kullanmayı düşünebilirsiniz.",
        "İyimser bakış açınız sizi zorluklarla başa çıkmada güçlü kılıyor. Bu özelliğinizi geliştirmeye devam edin.",
        "Pozitif duygularınızı paylaşarak başkalarına da ilham verebilirsiniz. Bu sosyal bağlarınızı güçlendirecektir.",
        "Bu pozitif enerjiyi fiziksel aktivitelere yönlendirmeyi deneyin. Egzersiz hem bedeninizi hem de ruhunuzu güçlendirir.",
        "Pozitif düşüncelerinizi günlük tutarak kaydetmeyi deneyin. Bu, zor zamanlarda size güç verecektir.",
        "Bu mutluluğu başkalarına da yaymayı deneyin. İyilik yapmak sizi daha da mutlu edecektir.",
        "Pozitif enerjinizi hedeflerinize odaklamayı deneyin. Başarı şansınız artacaktır.",
        "Bu sevinci hatırlayın ve zor zamanlarda bu anıları düşünün.",
        "Sevincinizi sanat, müzik veya yazı yoluyla ifade etmeyi deneyin."
    ],
    'negative': [
        "Zor zamanlardan geçtiğinizi anlıyorum. Bu duygular geçici ve herkes zaman zaman böyle hisseder. Kendinize nazik davranın.",
        "Negatif duygularınızı bastırmaya çalışmayın. Onları kabul etmek ve anlamak, iyileşme sürecinin ilk adımıdır.",
        "Bu duygularla başa çıkmak için derin nefes almayı ve kendinize zaman tanımayı deneyin. Her şey zamanla düzelir.",
        "Profesyonel destek almayı düşünebilirsiniz. Bir psikologla konuşmak size yeni perspektifler kazandırabilir.",
        "Küçük adımlarla başlayın. Her gün bir iyilik yapmayı deneyin - bu size umut verecektir.",
        "Sosyal bağlarınızı güçlendirin. Güvendiğiniz insanlarla konuşmak size destek olacaktır.",
        "Kendinizi meşgul edin. Yeni bir hobi veya aktivite bulmayı deneyin.",
        "Küçük aktivitelerle başlayın. Yürüyüş yapmak veya sevdiğiniz bir filmi izlemek yardımcı olabilir.",
        "Kendinize zaman tanıyın. Üzüntü geçici bir duygudur ve zamanla hafifleyecektir.",
        "Üzgün hissetmeniz tamamen normal. Bu duyguları yaşamaya izin verin, kendinizi suçlamayın."
    ],
    'neutral': [
        "Dengeli bir ruh halindesiniz. Bu durum kararlar alırken objektif olmanıza yardımcı olabilir.",
        "Sakin ve düşünceli bir ruh haliniz var. Bu zamanı kendinizi değerlendirmek için kullanabilirsiniz.",
        "Neutral duygular bazen değişim için gerekli bir ara aşamadır. Kendinizi dinlemeye devam edin.",
        "Bu dengeyi korumaya çalışın. Meditasyon veya hafif egzersizler ruh halinizi destekleyebilir.",
        "Bu sakin dönemi yaratıcı projeler için kullanmayı deneyin. Yeni hobiler keşfedebilirsiniz.",
        "Düşüncelerinizi yazıya dökmeyi deneyin. Bu size netlik kazandırabilir.",
        "Bu durumu bir öğrenme deneyimi olarak görmeyi deneyin.",
        "Kendinize zaman tanıyın ve durumu değerlendirin.",
        "Bu değişimi bir fırsat olarak görmeyi deneyin. Yeni deneyimler sizi geliştirebilir.",
        "Durumu analiz edin ve en iyi seçeneği bulmaya çalışın."
    ],
    'joy': [
        "Sevincinizi kutlayın! Bu pozitif enerjiyi yaratıcı aktivitelerde kullanmayı deneyin.",
        "Mutluluğunuzu paylaşın. Bu hem sizi hem de çevrenizdeki insanları daha da mutlu edecektir.",
        "Bu sevinci hatırlayın ve zor zamanlarda bu anıları düşünün.",
        "Sevincinizi sanat, müzik veya yazı yoluyla ifade etmeyi deneyin.",
        "Bu mutluluğu başkalarına da yaymayı deneyin. İyilik yapmak sizi daha da mutlu edecektir.",
        "Bu pozitif enerjiyi hedeflerinize odaklamayı deneyin. Başarı şansınız artacaktır.",
        "Bu sevinci hatırlayın ve zor zamanlarda bu anıları düşünün.",
        "Sevincinizi sanat, müzik veya yazı yoluyla ifade etmeyi deneyin.",
        "Bu mutluluğu başkalarına da yaymayı deneyin. İyilik yapmak sizi daha da mutlu edecektir.",
        "Bu pozitif enerjiyi hedeflerinize odaklamayı deneyin. Başarı şansınız artacaktır."
    ],
    'sadness': [
        "Üzgün hissetmeniz tamamen normal. Bu duyguları yaşamaya izin verin, kendinizi suçlamayın.",
        "Kendinize zaman tanıyın. Üzüntü geçici bir duygudur ve zamanla hafifleyecektir.",
        "Sevdiğiniz insanlarla konuşmayı deneyin. Sosyal destek iyileşme sürecinizi hızlandırabilir.",
        "Küçük aktivitelerle başlayın. Yürüyüş yapmak veya sevdiğiniz bir filmi izlemek yardımcı olabilir.",
        "Kendinizi meşgul edin. Yeni bir hobi veya aktivite bulmayı deneyin.",
        "Profesyonel yardım almayı düşünün. Bazen uzman desteği gerekebilir.",
        "Kendinize nazik davranın. Bu duyguları yaşamaya izin verin.",
        "Küçük adımlarla başlayın. Her gün bir iyilik yapmayı deneyin.",
        "Sosyal bağlarınızı güçlendirin. Güvendiğiniz insanlarla konuşmak size destek olacaktır.",
        "Bu duygularla başa çıkmak için derin nefes almayı ve kendinize zaman tanımayı deneyin."
    ],
    'anger': [
        "Öfkenizi anlıyorum. Bu duyguyu sağlıklı yollarla ifade etmek önemli. Derin nefes almayı deneyin.",
        "Öfkenizin kaynağını anlamaya çalışın. Bu size daha iyi başa çıkma stratejileri geliştirmenizde yardımcı olabilir.",
        "Fiziksel aktivite öfkenizi yönetmenize yardımcı olabilir. Egzersiz yapmayı deneyin.",
        "Öfkenizi yazıya dökmeyi deneyin. Bu, duygularınızı daha net görmenizi sağlayabilir.",
        "Kendinize zaman tanıyın. Öfke geçici bir duygudur, acele karar vermeyin.",
        "Meditasyon veya mindfulness teknikleri öfkenizi kontrol etmenize yardımcı olabilir.",
        "Bu duyguyu sağlıklı yollarla ifade etmek önemli. Derin nefes almayı deneyin.",
        "Öfkenizin kaynağını anlamaya çalışın. Bu size daha iyi başa çıkma stratejileri geliştirmenizde yardımcı olabilir.",
        "Fiziksel aktivite öfkenizi yönetmenize yardımcı olabilir. Egzersiz yapmayı deneyin.",
        "Öfkenizi yazıya dökmeyi deneyin. Bu, duygularınızı daha net görmenizi sağlayabilir."
    ],
    'fear': [
        "Korkularınızı anlıyorum. Bu duyguları kabul etmek ve onlarla yüzleşmek cesaret gerektirir.",
        "Korkularınızı küçük adımlarla ele almayı deneyin. Her küçük başarı sizi güçlendirecektir.",
        "Güvendiğiniz biriyle korkularınızı paylaşın. Bu, onları daha az korkutucu hale getirebilir.",
        "Mindfulness teknikleri korkularınızı yönetmenize yardımcı olabilir.",
        "Korkularınızı yazıya dökün. Bu, onları daha objektif değerlendirmenizi sağlar.",
        "Kendinizi eğitin. Bilgi, korkularınızı azaltmanın en iyi yoludur.",
        "Bu duyguları kabul etmek ve onlarla yüzleşmek cesaret gerektirir.",
        "Korkularınızı küçük adımlarla ele almayı deneyin. Her küçük başarı sizi güçlendirecektir.",
        "Güvendiğiniz biriyle korkularınızı paylaşın. Bu, onları daha az korkutucu hale getirebilir.",
        "Mindfulness teknikleri korkularınızı yönetmenize yardımcı olabilir."
    ],
    'surprise': [
        "Beklenmedik durumlarla karşılaşmak şaşırtıcı olabilir. Bu durumu anlamaya çalışın.",
        "Değişim bazen korkutucu olabilir ama aynı zamanda yeni fırsatlar da sunar.",
        "Bu durumu bir öğrenme deneyimi olarak görmeyi deneyin.",
        "Kendinize zaman tanıyın ve durumu değerlendirin.",
        "Bu değişimi bir fırsat olarak görmeyi deneyin. Yeni deneyimler sizi geliştirebilir.",
        "Durumu analiz edin ve en iyi seçeneği bulmaya çalışın.",
        "Bu durumu anlamaya çalışın.",
        "Değişim bazen korkutucu olabilir ama aynı zamanda yeni fırsatlar da sunar.",
        "Bu durumu bir öğrenme deneyimi olarak görmeyi deneyin.",
        "Kendinize zaman tanıyın ve durumu değerlendirin."
    ],
    'disgust': [
        "Bu duyguyu hissetmeniz normal. Kendinizi bu durumdan uzaklaştırmaya çalışın.",
        "Farklı perspektiflerden bakmayı deneyin. Bu size yeni anlayışlar kazandırabilir.",
        "Kendinizi temiz ve güvenli hissettiren aktivitelere odaklanın.",
        "Bu duyguyu geçici olarak kabul edin ve zamanla geçeceğini hatırlayın.",
        "Kendinizi meşgul edin. Başka şeylere odaklanmak yardımcı olabilir.",
        "Bu durumu analiz edin ve neden böyle hissettiğinizi anlamaya çalışın.",
        "Kendinizi bu durumdan uzaklaştırmaya çalışın.",
        "Farklı perspektiflerden bakmayı deneyin. Bu size yeni anlayışlar kazandırabilir.",
        "Kendinizi temiz ve güvenli hissettiren aktivitelere odaklanın.",
        "Bu duyguyu geçici olarak kabul edin ve zamanla geçeceğini hatırlayın."
    ]
}

def preprocess_text(text):
    """Metni ön işleme"""
    # Küçük harfe çevir
    text = text.lower()
    # Özel karakterleri temizle
    text = re.sub(r'[^\w\s]', '', text)
    return text

def analyze_sentiment_advanced(text):
    """Gelişmiş duygu analizi"""
    results = {}
    
    # Temel analizler
    blob = TextBlob(text)
    results['textblob'] = {
        'polarity': blob.sentiment.polarity,
        'subjectivity': blob.sentiment.subjectivity
    }
    
    vader_scores = vader_analyzer.polarity_scores(text)
    results['vader'] = vader_scores
    
    # AI modelleri varsa kullan
    if AI_MODELS_LOADED:
        try:
            # Sentiment analizi
            sentiment_result = sentiment_analyzer(text)[0]
            results['transformers_sentiment'] = sentiment_result
            
            # Duygu analizi
            emotion_result = emotion_analyzer(text)[0]
            results['emotion'] = emotion_result
            
        except Exception as e:
            print(f"AI model analizi hatası: {e}")
    
    # Gelişmiş metin analizi
    sentences = text.split('.')
    words = text.split()
    
    results['text_analysis'] = {
        'sentence_count': len([s for s in sentences if s.strip()]),
        'word_count': len(words),
        'avg_sentence_length': len(words) / len([s for s in sentences if s.strip()]) if len([s for s in sentences if s.strip()]) > 0 else 0,
        'unique_words': len(set(words)),
        'lexical_diversity': len(set(words)) / len(words) if words else 0
    }
    
    return results

def get_psychological_advice(sentiment_results):
    """Gelişmiş psikolojik tavsiye"""
    advice = []
    
    # Genel duygu durumuna göre tavsiye
    vader_compound = sentiment_results.get('vader', {}).get('compound', 0)
    textblob_polarity = sentiment_results.get('textblob', {}).get('polarity', 0)
    
    # Daha akıllı tavsiye seçimi
    if vader_compound > 0.2 or textblob_polarity > 0.2:
        advice.append(np.random.choice(PSYCHOLOGICAL_ADVICE['positive']))
    elif vader_compound < -0.2 or textblob_polarity < -0.2:
        advice.append(np.random.choice(PSYCHOLOGICAL_ADVICE['negative']))
    else:
        advice.append(np.random.choice(PSYCHOLOGICAL_ADVICE['neutral']))
    
    # Spesifik duyguya göre tavsiye
    emotion = sentiment_results.get('emotion', {}).get('label', '').lower()
    if emotion in PSYCHOLOGICAL_ADVICE:
        advice.append(np.random.choice(PSYCHOLOGICAL_ADVICE[emotion]))
    
    # Metin analizi bazlı ek tavsiyeler
    text_analysis = sentiment_results.get('text_analysis', {})
    if text_analysis.get('sentence_count', 0) > 5:
        advice.append("Detaylı düşüncelerinizi paylaştığınız için teşekkürler. Bu derinlik, kendinizi daha iyi anlamanıza yardımcı olur.")
    
    if text_analysis.get('lexical_diversity', 0) > 0.7:
        advice.append("Zengin kelime dağarcığınız düşüncelerinizi net bir şekilde ifade etmenizi sağlıyor. Bu yetenek, iletişiminizi güçlendirir.")
    
    # Daha çeşitli tavsiyeler için ek seçimler
    if len(advice) < 3:
        all_advice = []
        for category in PSYCHOLOGICAL_ADVICE.values():
            all_advice.extend(category)
        additional_advice = np.random.choice(all_advice, min(3 - len(advice), 2), replace=False)
        advice.extend(additional_advice)
    
    return advice[:4]  # Maksimum 4 tavsiye

def generate_insights(sentiment_results):
    """Gelişmiş içgörüler üret"""
    insights = []
    
    # Duygu yoğunluğu analizi
    vader_compound = abs(sentiment_results.get('vader', {}).get('compound', 0))
    if vader_compound > 0.5:
        insights.append("Duygularınız oldukça yoğun. Bu, duruma derinden bağlı olduğunuzu gösteriyor.")
    elif vader_compound < 0.2:
        insights.append("Duygularınız dengeli. Bu, durumu objektif değerlendirdiğinizi gösteriyor.")
    
    # Öznellik analizi
    subjectivity = sentiment_results.get('textblob', {}).get('subjectivity', 0)
    if subjectivity > 0.7:
        insights.append("Yazınız oldukça öznel. Bu, kişisel deneyimlerinizin önemli olduğunu gösteriyor.")
    elif subjectivity < 0.3:
        insights.append("Yazınız oldukça nesnel. Bu, durumu mantıklı bir şekilde değerlendirdiğinizi gösteriyor.")
    
    # Metin yapısı analizi
    text_analysis = sentiment_results.get('text_analysis', {})
    if text_analysis.get('sentence_count', 0) > 10:
        insights.append("Detaylı bir analiz yapmışsınız. Bu, durumu kapsamlı bir şekilde değerlendirdiğinizi gösteriyor.")
    
    # AI model sonuçlarına göre ek içgörüler
    if sentiment_results.get('transformers_sentiment'):
        sentiment_label = sentiment_results['transformers_sentiment']['label']
        sentiment_score = sentiment_results['transformers_sentiment']['score']
        
        if sentiment_score > 0.8:
            insights.append(f"AI analizi {sentiment_label} duygusunu yüksek güvenle tespit etti. Bu sonuç oldukça güvenilir.")
        elif sentiment_score > 0.6:
            insights.append(f"AI analizi {sentiment_label} duygusunu orta güvenle tespit etti.")
    
    if sentiment_results.get('emotion'):
        emotion_label = sentiment_results['emotion']['label']
        emotion_score = sentiment_results['emotion']['score']
        
        if emotion_score > 0.5:
            insights.append(f"Temel duygunuz {emotion_label} olarak tespit edildi. Bu duyguya odaklanmanız faydalı olabilir.")
    
    # Daha çeşitli içgörüler için ek seçimler
    additional_insights = [
        "Duygularınızı düzenli olarak takip etmek, ruh halinizi anlamanıza yardımcı olur.",
        "Bu analiz, kendinizi daha iyi tanımanız için bir başlangıç noktası olabilir.",
        "Duygularınızı yazıya dökmek, onları daha net görmenizi sağlar.",
        "Her duygu geçicidir ve değişim doğaldır.",
        "Kendinizi dinlemek, en iyi rehberinizdir."
    ]
    
    if len(insights) < 3:
        additional = np.random.choice(additional_insights, min(3 - len(insights), 2), replace=False)
        insights.extend(additional)
    
    return insights[:4]  # Maksimum 4 içgörü

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Lütfen bir metin girin'}), 400
        
        if len(text) < 10:
            return jsonify({'error': 'Lütfen daha detaylı bir açıklama yazın (en az 10 karakter)'}), 400
        
        # Gelişmiş duygu analizi
        sentiment_results = analyze_sentiment_advanced(text)
        
        # Psikolojik tavsiye
        advice = get_psychological_advice(sentiment_results)
        
        # İçgörüler
        insights = generate_insights(sentiment_results)
        
        # Sonuçları formatla
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
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': f'Analiz sırasında hata oluştu: {str(e)}'}), 500

@app.route('/health')
def health():
    """AI model durumunu kontrol et"""
    return jsonify({
        'status': 'healthy',
        'ai_models_loaded': AI_MODELS_LOADED,
        'models': {
            'sentiment': AI_MODELS_LOADED,
            'emotion': AI_MODELS_LOADED,
            'turkish': AI_MODELS_LOADED,
            'embedding': AI_MODELS_LOADED
        }
    })

@app.route('/manifest.json')
def manifest():
    """PWA manifest dosyası"""
    return send_from_directory('static', 'manifest.json')

@app.route('/sw.js')
def service_worker():
    """Service worker dosyası"""
    return send_from_directory('static', 'sw.js')

@app.route('/static/images/<path:filename>')
def serve_icons(filename):
    """Icon dosyalarını serve et"""
    return send_from_directory('static/images', filename)

if __name__ == '__main__':
    print("🚀 Tasolog AI uygulaması başlatılıyor...")
    print("🤖 AI Modelleri:", "✅ Yüklendi" if AI_MODELS_LOADED else "⚠️ Temel modeller")
    print("📱 http://localhost:5001 adresinde erişilebilir")
    app.run(debug=True, host='0.0.0.0', port=5001)
