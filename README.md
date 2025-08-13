# 🧠 Tasolog - Modern Psikoloji & Mindfulness Uygulaması

**AI destekli modern psikoloji ve mindfulness uygulaması**

Tasolog, gelişmiş yapay zeka teknolojileri kullanarak duygu analizi yapar ve kişiselleştirilmiş psikolojik tavsiyeler sunar. iPhone ve mobil cihazlar için optimize edilmiş, PWA (Progressive Web App) desteğiyle native uygulama deneyimi sağlar.

## ✨ Özellikler

### 🤖 AI Destekli Analiz
- **Çoklu AI Model**: Transformers, VADER, TextBlob kullanarak kapsamlı duygu analizi
- **Gelişmiş NLP**: Türkçe dil desteği ile hassas metin analizi
- **Offline Çalışma**: API gerektirmez, tamamen yerel AI modelleri
- **Gerçek Zamanlı**: Anlık duygu analizi ve içgörüler

### 📱 Modern Mobil Deneyim
- **PWA Desteği**: Ana ekrana ekleme, offline çalışma
- **iPhone Optimizasyonu**: Safe area, notch desteği, iOS-specific optimizasyonlar
- **Responsive Tasarım**: Tüm mobil cihazlarda mükemmel görünüm
- **Touch-Friendly**: Mobil dokunmatik kullanım için optimize edilmiş

### 🎨 Kullanıcı Arayüzü
- **Modern Tasarım**: Glassmorphism, gradient arka planlar, smooth animasyonlar
- **Calming Color Palette**: Rahatlatıcı renkler ve minimalist tasarım
- **Bottom Navigation**: 5 ana bölüm ile kolay navigasyon
- **Micro-animations**: Kullanıcı deneyimini artıran animasyonlar

### 🧘‍♀️ Mindfulness Özellikleri
- **Meditasyon Seansları**: Kademeli mindfulness programları
- **Duygu Günlüğü**: Günlük duygu takibi ve analizi
- **İlerleme Takibi**: Kişisel gelişim metrikları
- **AI Sohbet**: Yapay zeka destekli danışmanlık

## 🚀 Kurulum

### Gereksinimler
- Python 3.8+
- pip (Python package manager)
- Modern web tarayıcısı

### Adım Adım Kurulum

1. **Projeyi klonlayın**
```bash
git clone <repository-url>
cd heroui-project
```

2. **Python bağımlılıklarını yükleyin**
```bash
pip install -r requirements.txt
```

3. **Uygulamayı başlatın**
```bash
python app.py
```

4. **Tarayıcıda açın**
```
http://localhost:5001
```

### Mobil Erişim (iPhone/Android)

1. **Aynı WiFi ağında**
```
http://[BILGISAYAR-IP]:5001
```

2. **Ana ekrana ekleme**
   - Safari'de sayfayı açın
   - Paylaş butonuna basın (📤)
   - "Ana Ekrana Ekle" seçin
   - "Ekle" butonuna basın

## 🛠 Teknik Detaylar

### Backend
- **Framework**: Flask (Python)
- **AI/ML**: Transformers, VADER, TextBlob
- **Models**: 
  - `cardiffnlp/twitter-roberta-base-sentiment-latest`
  - `j-hartmann/emotion-english-distilroberta-base`
- **CORS**: Flask-CORS ile cross-origin desteği

### Frontend
- **HTML5**: Modern semantic markup
- **CSS3**: CSS Grid, Flexbox, CSS Variables, Animations
- **JavaScript**: ES6+, PWA APIs, Service Worker
- **Icons**: Font Awesome 6.0
- **Fonts**: Google Fonts (Inter)

### PWA Özellikleri
- **Manifest**: PWA konfigürasyonu
- **Service Worker**: Offline desteği, cache yönetimi
- **Install Prompt**: Ana ekrana ekleme önerisi
- **iOS Support**: Apple-specific meta tags ve optimizasyonlar

## 📁 Proje Yapısı

```
heroui-project/
├── app.py                 # Ana Flask uygulaması
├── requirements.txt       # Python bağımlılıkları
├── static/
│   ├── css/
│   │   └── style.css     # Ana CSS dosyası
│   ├── js/
│   │   └── app.js        # Frontend JavaScript
│   ├── images/           # PWA icon'ları
│   ├── manifest.json     # PWA manifest
│   └── sw.js            # Service Worker
├── templates/
│   └── index.html        # Ana HTML template
└── README.md            # Bu dosya
```

## 🎯 Kullanım

### Ana Sayfa
- **Mood Tracker**: Anlık ruh hali göstergesi
- **Günlük Seri**: Süreklilik takibi
- **Hızlı İstatistikler**: Mood skoru, meditasyon süresi, günlük sayısı
- **Feature Cards**: Ana özelliklere hızlı erişim

### AI Duygu Analizi
1. **Duygu Paylaşımı**: Günlük deneyimlerinizi yazın
2. **AI Analiz**: Çoklu model ile duygu analizi
3. **Psikolojik Tavsiyeler**: Kişiselleştirilmiş öneriler
4. **İçgörüler**: AI destekli kişisel anlayışlar

### Meditasyon
- **Başlangıç, Orta, İleri**: Seviyeli mindfulness programları
- **Nefes Farkındalığı**: 5 dakikalık temel seanslar
- **Vücut Taraması**: 10 dakikalık orta seviye
- **Sevgi Meditasyonu**: 15 dakikalık ileri seviye

### Günlük
- **Duygu Takibi**: Günlük mood kayıtları
- **İstatistikler**: Trend analizi ve ilerleme
- **Geçmiş Girişler**: Duygu geçmişini görüntüleme

## 🤖 AI Modelleri

### Sentiment Analysis
- **VADER**: Sosyal medya metinleri için optimize
- **TextBlob**: Genel amaçlı duygu analizi
- **RoBERTa**: Twitter tabanlı gelişmiş model

### Emotion Detection
- **DistilRoBERTa**: 7 temel duygu sınıflandırması
  - Joy (Sevinç)
  - Sadness (Üzüntü)
  - Anger (Öfke)
  - Fear (Korku)
  - Surprise (Şaşkınlık)
  - Disgust (Tiksinti)
  - Neutral (Nötr)

### Text Analysis
- **Kelime Sayısı**: Metin uzunluğu analizi
- **Cümle Yapısı**: Dilbilgisel analiz
- **Kelime Çeşitliliği**: Vocabulary richness
- **Subjektiflik**: Nesnel/öznel metin tespiti

## 🎨 Tasarım Sistemi

### Color Palette
- **Primary**: `#6366f1` (Indigo)
- **Secondary**: `#10b981` (Emerald)
- **Accent**: `#f59e0b` (Amber)
- **Background**: `#ffffff` (White)
- **Text**: `#1e293b` (Slate)

### Typography
- **Font Family**: Inter (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700
- **Modern Sans-serif**: Clean ve okunabilir

### Animations
- **Micro-interactions**: Hover, tap, focus effects
- **Page Transitions**: Smooth section switching
- **Loading States**: Progressive loading indicators
- **PWA Install**: Modern prompt animations

## 📱 Mobil Optimizasyonlar

### iPhone/iOS
- **Safe Area**: Notch ve home indicator desteği
- **Touch Handling**: iOS-specific gesture prevention
- **Status Bar**: Black-translucent styling
- **Viewport**: 100vh issue çözümü

### Android
- **Material Design**: Android guidelines uyumluluğu
- **Navigation**: Back button handling
- **Notifications**: PWA notification desteği

## 🔧 Development

### Debug Modu
```javascript
// Console'da test fonksiyonları
resetPWAPrompt()  // PWA ayarlarını sıfırla
```

### Environment Variables
```bash
# Port değiştirme
export PORT=5001

# Debug modu
export FLASK_DEBUG=1
```

### Performance
- **Service Worker**: Asset caching
- **Lazy Loading**: On-demand resource loading
- **Minification**: Production build optimizasyonu

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production
```bash
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

### Docker (Opsiyonel)
```dockerfile
FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

## 📊 Özellik Listesi

### ✅ Tamamlanan
- [x] AI destekli duygu analizi
- [x] PWA desteği ve ana ekrana ekleme
- [x] iPhone optimizasyonları
- [x] Modern UI/UX tasarımı
- [x] Offline çalışma
- [x] Multi-language AI models
- [x] Responsive design
- [x] Service Worker implementation

### 🔄 Geliştirme Aşamasında
- [ ] Push notification desteği
- [ ] Advanced analytics dashboard
- [ ] Social sharing features
- [ ] Export/import functionality

### 💡 Gelecek Planları
- [ ] Multi-language support
- [ ] Voice-to-text integration
- [ ] Advanced AI coaching
- [ ] Community features

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'i push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 📞 İletişim

- **Proje**: Tasolog - Modern Psikoloji & Mindfulness
- **Teknoloji**: Flask + AI/ML + PWA
- **Platform**: Web, iOS, Android

## 🙏 Teşekkürler

- **Hugging Face**: AI model desteği
- **Font Awesome**: Icon library
- **Google Fonts**: Typography
- **Modern CSS**: Design inspiration

---

**Tasolog ile mental sağlığınızı güçlendirin! 🧠✨**

*Modern teknoloji ile geleneksel psikoloji bilimini birleştiren, kişiselleştirilmiş mental sağlık deneyimi.*