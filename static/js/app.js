// Modern Psychology App JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // PWA Installation
    let deferredPrompt;
    const installButton = document.createElement('button');
    installButton.style.display = 'none';
    installButton.id = 'install-button';
    installButton.innerHTML = 'Ana Ekrana Ekle';
    installButton.className = 'install-btn';
    document.body.appendChild(installButton);

    // PWA Install Prompt Elements
    const pwaInstallPrompt = document.getElementById('pwa-install-prompt');
    const pwaInstallBtn = document.getElementById('pwa-install-btn');
    const pwaLaterBtn = document.getElementById('pwa-later-btn');
    const pwaCloseBtn = document.getElementById('pwa-close-btn');



    // PWA Install Event
    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;
        installButton.style.display = 'block';
        
        // Show PWA install prompt after loading
        setTimeout(() => {
            showPWAInstallPrompt();
        }, 3000); // 3 saniye sonra göster
        
        installButton.addEventListener('click', () => {
            deferredPrompt.prompt();
            deferredPrompt.userChoice.then((choiceResult) => {
                if (choiceResult.outcome === 'accepted') {
                    console.log('PWA installed');
                    hidePWAInstallPrompt();
                }
                deferredPrompt = null;
                installButton.style.display = 'none';
            });
        });
    });

    // PWA Installed Event
    window.addEventListener('appinstalled', () => {
        console.log('PWA was installed');
        installButton.style.display = 'none';
        hidePWAInstallPrompt();
    });

    // PWA Install Prompt Functions
    function showPWAInstallPrompt() {
        // Element kontrolü
        if (!pwaInstallPrompt) {
            return;
        }
        
        // Check if user has already dismissed or installed
        if (localStorage.getItem('pwa-install-dismissed') || localStorage.getItem('pwa-installed')) {
            return;
        }
        
        try {
            // Önce prompt'u görünür yap
            pwaInstallPrompt.style.display = 'flex';
            pwaInstallPrompt.style.visibility = 'visible';
            pwaInstallPrompt.style.opacity = '1';
            pwaInstallPrompt.style.zIndex = '99999';
            document.body.style.overflow = 'hidden';
            
            // Animasyonlu açılış
            setTimeout(() => {
                pwaInstallPrompt.classList.add('show');
                
                // İçerik animasyonu
                const content = pwaInstallPrompt.querySelector('.pwa-install-content');
                if (content) {
                    content.style.animation = 'slideUpScale 0.5s ease-out';
                }
            }, 100);
            
            // Track when shown
            const now = Date.now();
            localStorage.setItem('pwa-last-shown', now.toString());
            
        } catch (error) {
            console.error('Error showing PWA prompt:', error);
        }
    }

    function hidePWAInstallPrompt() {
        if (!pwaInstallPrompt) return;
        
        pwaInstallPrompt.classList.remove('show');
        
        // Exit animation
        const content = pwaInstallPrompt.querySelector('.pwa-install-content');
        if (content) {
            content.style.animation = 'slideDownScale 0.3s ease-in';
        }
        
        // Hide after animation
        setTimeout(() => {
            pwaInstallPrompt.style.display = 'none';
            document.body.style.overflow = '';
        }, 300);
    }

    // Track user interaction
    function trackUserInteraction() {
        sessionStorage.setItem('user-interacted', 'true');
    }

    // Reset PWA prompt for testing (can be called from console)
    window.resetPWAPrompt = function() {
        localStorage.removeItem('pwa-install-dismissed');
        localStorage.removeItem('pwa-installed');
        localStorage.removeItem('pwa-last-shown');
        sessionStorage.removeItem('user-interacted');
        location.reload();
    };

    // PWA Install Prompt Event Listeners
    if (pwaInstallBtn) {
        pwaInstallBtn.addEventListener('click', () => {
            // For iOS, show tutorial steps
            if (/iPad|iPhone|iPod/.test(navigator.userAgent)) {
                // Show success message
                if (typeof showFeatureMessage === 'function') {
                    showFeatureMessage('Ana ekrana ekleme talimatları gösterildi!');
                }
                hidePWAInstallPrompt();
                localStorage.setItem('pwa-install-dismissed', 'true');
            } else {
                // For other devices, use native install prompt
                if (deferredPrompt) {
                    deferredPrompt.prompt();
                    deferredPrompt.userChoice.then((choiceResult) => {
                        if (choiceResult.outcome === 'accepted') {
                            console.log('PWA installed');
                            localStorage.setItem('pwa-installed', 'true');
                        }
                        deferredPrompt = null;
                        hidePWAInstallPrompt();
                    });
                }
            }
        });
    }

    if (pwaLaterBtn) {
        pwaLaterBtn.addEventListener('click', () => {
            hidePWAInstallPrompt();
            localStorage.setItem('pwa-install-dismissed', 'true');
        });
    }

    if (pwaCloseBtn) {
        pwaCloseBtn.addEventListener('click', () => {
            hidePWAInstallPrompt();
            localStorage.setItem('pwa-install-dismissed', 'true');
        });
    }

    // Close PWA prompt when clicking outside
    if (pwaInstallPrompt) {
        pwaInstallPrompt.addEventListener('click', (e) => {
            if (e.target === pwaInstallPrompt) {
                hidePWAInstallPrompt();
                localStorage.setItem('pwa-install-dismissed', 'true');
            }
        });
    }

    // iPhone Specific Optimizations
    if (/iPad|iPhone|iPod/.test(navigator.userAgent)) {
        // iOS specific optimizations
        document.body.classList.add('ios-device');
        
        // Prevent zoom on double tap
        let lastTouchEnd = 0;
        document.addEventListener('touchend', function (event) {
            const now = (new Date()).getTime();
            if (now - lastTouchEnd <= 300) {
                event.preventDefault();
            }
            lastTouchEnd = now;
        }, false);
        
        // Better touch handling
        document.addEventListener('touchstart', function() {}, {passive: true});
        document.addEventListener('touchmove', function() {}, {passive: true});
        
        // iOS Safari specific fixes
        document.addEventListener('gesturestart', function(e) {
            e.preventDefault();
        });
        
        document.addEventListener('gesturechange', function(e) {
            e.preventDefault();
        });
        
        document.addEventListener('gestureend', function(e) {
            e.preventDefault();
        });
        
        // Fix for iOS Safari 100vh issue
        function setVH() {
            let vh = window.innerHeight * 0.01;
            document.documentElement.style.setProperty('--vh', `${vh}px`);
        }
        
        setVH();
        window.addEventListener('resize', setVH);
        window.addEventListener('orientationchange', setVH);
    }

    // Service Worker Registration
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/sw.js')
                .then((registration) => {
                    console.log('SW registered: ', registration);
                })
                .catch((registrationError) => {
                    console.log('SW registration failed: ', registrationError);
                });
        });
    }

    // DOM Elements
    const loadingScreen = document.getElementById('loading-screen');
    const progressFill = document.getElementById('progress-fill');
    const loadingText = document.getElementById('loading-text');
    const appContainer = document.getElementById('app-container');
    
    // Home Section
    const homeSection = document.getElementById('home-section');
    
    // Header Elements
    const greetingText = document.getElementById('greeting-text');
    const currentMood = document.getElementById('current-mood');
    const moodLabel = document.getElementById('mood-label');
    const notificationBell = document.getElementById('notification-bell');
    const notificationBadge = document.getElementById('notification-badge');
    const notificationPanel = document.getElementById('notification-panel');
    const closeNotifications = document.getElementById('close-notifications');
    
    // Quick Actions
    const dailyReflectionBtn = document.getElementById('daily-reflection-btn');
    
    // Feature Cards
    const meditationCard = document.getElementById('meditation-card');
    const journalCard = document.getElementById('journal-card');
    const progressCard = document.getElementById('progress-card');
    const supportCard = document.getElementById('support-card');
    
    // Analysis Section
    const analysisSection = document.getElementById('analysis-section');
    const emotionText = document.getElementById('emotion-text');
    const charCount = document.getElementById('char-count');
    const analyzeBtn = document.getElementById('analyze-btn');
    
    // Results Elements
    const resultsSection = document.getElementById('results-section');
    const aiStatusCard = document.getElementById('ai-status-card');
    const aiStatusText = document.getElementById('ai-status-text');
    const sentimentSummary = document.getElementById('sentiment-summary');
    const overallSentiment = document.getElementById('overall-sentiment');
    const insightsContent = document.getElementById('insights-content');
    const sentenceCount = document.getElementById('sentence-count');
    const wordCount = document.getElementById('word-count');
    const uniqueWords = document.getElementById('unique-words');
    const lexicalDiversity = document.getElementById('lexical-diversity');
    const sentimentModelIcon = document.getElementById('sentiment-model-icon');
    const emotionModelIcon = document.getElementById('emotion-model-icon');
    const turkishModelIcon = document.getElementById('turkish-model-icon');
    const embeddingModelIcon = document.getElementById('embedding-model-icon');
    const adviceList = document.getElementById('advice-list');
    
    // Meditation Section
    const meditationSection = document.getElementById('meditation-section');
    const categoryCards = document.querySelectorAll('.category-card');
    const sessionCards = document.querySelectorAll('.session-card');
    
    // Journal Section
    const journalSection = document.getElementById('journal-section');
    const journalBtns = document.querySelectorAll('.journal-btn');
    const entryCards = document.querySelectorAll('.entry-card');
    
    // Chat Section
    const chatSection = document.getElementById('chat-section');
    const chatMessages = document.getElementById('chat-messages');
    const chatInputField = document.getElementById('chat-input-field');
    const sendMessageBtn = document.getElementById('send-message-btn');
    
    // Profile Section
    const profileSection = document.getElementById('profile-section');
    const menuItems = document.querySelectorAll('.menu-item');
    
    // Bottom Navigation
    const navItems = document.querySelectorAll('.nav-item');
    
    // Error Modal
    const errorModal = document.getElementById('error-modal');
    const errorMessage = document.getElementById('error-message');
    
    // Initialize App
    initializeApp();
    
    function initializeApp() {
        simulateAILoading();
        initializeEventListeners();
        updateGreeting();
        addAnimations();
        checkAIStatus();
        initializeStreakAnimation();
    }
    
    function simulateAILoading() {
        const loadingTexts = [
            'AI modelleri yükleniyor...',
            'Duygu analizi modelleri hazırlanıyor...',
            'Psikolojik tavsiye sistemi aktifleştiriliyor...',
            'Mindfulness özellikleri yükleniyor...',
            'Tasolog hazır!'
        ];
        
        let currentText = 0;
        let progress = 0;
        
        const interval = setInterval(() => {
            progress += Math.random() * 20;
            if (progress > 100) progress = 100;
            
            progressFill.style.width = progress + '%';
            
            if (currentText < loadingTexts.length - 1 && progress > (currentText + 1) * 20) {
                loadingText.textContent = loadingTexts[currentText];
                currentText++;
            }
            
            if (progress >= 100) {
                clearInterval(interval);
                loadingText.textContent = loadingTexts[loadingTexts.length - 1];
                
                setTimeout(() => {
                    loadingScreen.style.opacity = '0';
                    
                    setTimeout(() => {
                        loadingScreen.style.display = 'none';
                        appContainer.style.display = 'block';
                        
                        // Loading tamamlandıktan sonra PWA prompt göster
                        setTimeout(() => {
                            showPWAInstallPrompt();
                        }, 1000);
                    }, 500);
                }, 1000);
            }
        }, 400);
    }
    
    function updateGreeting() {
        const hour = new Date().getHours();
        let greeting = '';
        
        if (hour < 12) {
            greeting = 'Günaydın! Nasıl hissediyorsun?';
        } else if (hour < 18) {
            greeting = 'Merhaba! Nasıl hissediyorsun?';
        } else {
            greeting = 'İyi akşamlar! Nasıl hissediyorsun?';
        }
        
        greetingText.textContent = greeting;
    }
    
    function initializeEventListeners() {
        // Track user interactions
        document.addEventListener('click', trackUserInteraction);
        document.addEventListener('touchstart', trackUserInteraction);
        
        // Quick Actions
        dailyReflectionBtn.addEventListener('click', () => {
            showAnalysisSection();
        });
        
        // Feature Cards
        meditationCard.addEventListener('click', () => {
            showMeditationSection();
        });
        
        journalCard.addEventListener('click', () => {
            showJournalSection();
        });
        
        progressCard.addEventListener('click', () => {
            showFeatureMessage('İlerleme takibi yakında!');
        });
        
        supportCard.addEventListener('click', () => {
            showChatSection();
        });
        
        // Notifications
        notificationBell.addEventListener('click', () => {
            showNotificationPanel();
        });
        
        closeNotifications.addEventListener('click', () => {
            hideNotificationPanel();
        });
        
        // Text Input
        emotionText.addEventListener('input', updateCharCount);
        emotionText.addEventListener('keydown', handleKeydown);
        
        // Analyze Button
        analyzeBtn.addEventListener('click', analyzeEmotion);
        
        // Meditation
        categoryCards.forEach(card => {
            card.addEventListener('click', () => {
                selectCategory(card);
            });
        });
        
        sessionCards.forEach(card => {
            card.addEventListener('click', () => {
                playSession(card);
            });
        });
        
        // Journal
        journalBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                handleJournalAction(btn);
            });
        });
        
        entryCards.forEach(card => {
            card.addEventListener('click', () => {
                openJournalEntry(card);
            });
        });
        
        // Chat
        sendMessageBtn.addEventListener('click', sendMessage);
        chatInputField.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Profile
        menuItems.forEach(item => {
            item.addEventListener('click', () => {
                handleMenuAction(item);
            });
        });
        
        // Bottom Navigation
        navItems.forEach(item => {
            item.addEventListener('click', () => {
                const section = item.dataset.section;
                handleNavigation(section);
            });
        });
        
        // Keyboard Shortcuts
        document.addEventListener('keydown', handleKeyboardShortcuts);
        
        // Touch Support
        addTouchSupport();
    }
    
    function showAnalysisSection() {
        hideAllSections();
        analysisSection.style.display = 'block';
        emotionText.focus();
    }
    
    function showMeditationSection() {
        hideAllSections();
        meditationSection.style.display = 'block';
    }
    
    function showJournalSection() {
        hideAllSections();
        journalSection.style.display = 'block';
    }
    
    function showChatSection() {
        hideAllSections();
        chatSection.style.display = 'block';
        chatInputField.focus();
    }
    
    function showProfileSection() {
        hideAllSections();
        profileSection.style.display = 'block';
    }
    
    function hideAllSections() {
        const sections = [
            homeSection,
            analysisSection, 
            meditationSection, 
            journalSection, 
            chatSection, 
            profileSection
        ];
        
        sections.forEach(section => {
            if (section) section.style.display = 'none';
        });
    }
    
    function showNotificationPanel() {
        notificationPanel.classList.add('show');
        document.body.style.overflow = 'hidden';
    }
    
    function hideNotificationPanel() {
        notificationPanel.classList.remove('show');
        document.body.style.overflow = '';
    }
    
    function selectCategory(card) {
        categoryCards.forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        
        // Simulate category change
        const category = card.dataset.category;
        showFeatureMessage(`${category} kategorisi seçildi!`);
    }
    
    function playSession(card) {
        const sessionTitle = card.querySelector('h4').textContent;
        showFeatureMessage(`${sessionTitle} başlatılıyor...`);
        
        // Simulate session start
        setTimeout(() => {
            showFeatureMessage('Meditasyon seansı başladı!');
        }, 1000);
    }
    
    function handleJournalAction(btn) {
        if (btn.classList.contains('primary')) {
            showFeatureMessage('Yeni günlük oluşturuluyor...');
        } else {
            showFeatureMessage('İstatistikler gösteriliyor...');
        }
    }
    
    function openJournalEntry(card) {
        const title = card.querySelector('h4').textContent;
        showFeatureMessage(`${title} açılıyor...`);
    }
    
    function sendMessage() {
        const message = chatInputField.value.trim();
        if (!message) return;
        
        // Add user message
        addChatMessage(message, 'user');
        chatInputField.value = '';
        
        // Simulate AI response
        setTimeout(() => {
            const responses = [
                'Bu konuda sana nasıl yardımcı olabilirim?',
                'Anlıyorum, bu durumda şunları önerebilirim...',
                'Duygularını paylaştığın için teşekkürler. Bu konuda daha detaylı konuşalım.',
                'Bu durumu birlikte analiz edelim. Nasıl hissettiğini anlatabilir misin?'
            ];
            const randomResponse = responses[Math.floor(Math.random() * responses.length)];
            addChatMessage(randomResponse, 'ai');
        }, 1000);
    }
    
    function addChatMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
        
        const content = document.createElement('div');
        content.className = 'message-content';
        content.innerHTML = `<p>${text}</p>`;
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function handleMenuAction(item) {
        const action = item.querySelector('span').textContent;
        showFeatureMessage(`${action} açılıyor...`);
    }
    
    function showFeatureMessage(message) {
        // Create a temporary notification
        const notification = document.createElement('div');
        notification.className = 'feature-notification';
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: var(--primary-color);
            color: white;
            padding: 12px 24px;
            border-radius: 25px;
            font-size: 14px;
            font-weight: 500;
            z-index: 10000;
            box-shadow: var(--shadow-lg);
            animation: slideDown 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideUp 0.3s ease';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 2000);
    }
    
    function updateCharCount() {
        const count = emotionText.value.length;
        charCount.textContent = count;
        
        if (count > 1600) {
            charCount.style.color = '#ef4444';
        } else if (count > 1200) {
            charCount.style.color = '#f59e0b';
        } else {
            charCount.style.color = '#94a3b8';
        }
    }
    
    function handleKeydown(e) {
        if (e.ctrlKey && e.key === 'Enter') {
            analyzeEmotion();
        }
    }
    
    function handleKeyboardShortcuts(e) {
        if (e.ctrlKey && e.key === 'k') {
            e.preventDefault();
            showAnalysisSection();
        }
    }
    
    async function analyzeEmotion() {
        const text = emotionText.value.trim();
        
        if (text.length < 10) {
            showError('Lütfen daha detaylı bir açıklama yazın (en az 10 karakter)');
            return;
        }
        
        setLoadingState(true);
        
        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                displayResults(data);
                updateMoodTracker(data.summary);
            } else {
                showError(data.error || 'Analiz sırasında bir hata oluştu');
            }
        } catch (error) {
            showError('Bağlantı hatası: ' + error.message);
        } finally {
            setLoadingState(false);
        }
    }
    
    function updateMoodTracker(summary) {
        const sentiment = summary.overall_sentiment;
        const emotion = summary.emotion;
        
        // Update mood emoji
        const moodEmoji = currentMood.querySelector('i');
        const moodText = moodLabel;
        
        switch (sentiment) {
            case 'positive':
                moodEmoji.className = 'fas fa-laugh';
                moodEmoji.style.color = '#10b981';
                moodText.textContent = 'Mutlu';
                break;
            case 'negative':
                moodEmoji.className = 'fas fa-sad-tear';
                moodEmoji.style.color = '#ef4444';
                moodText.textContent = 'Üzgün';
                break;
            default:
                moodEmoji.className = 'fas fa-meh';
                moodEmoji.style.color = '#f59e0b';
                moodText.textContent = 'Nötr';
        }
        
        // Add animation
        currentMood.style.transform = 'scale(1.2)';
        setTimeout(() => {
            currentMood.style.transform = 'scale(1)';
        }, 200);
    }
    
    function displayResults(data) {
        updateAIStatus(data.summary.ai_models_loaded);
        updateSentimentSummary(data.summary);
        updateDetailedAnalysis(data.analysis);
        updateTextAnalysis(data.analysis);
        updateInsights(data.insights);
        updateAdvice(data.advice);
        
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
        
        // Add animations
        const elements = resultsSection.querySelectorAll('.analysis-card, .advice-item, .insight-item');
        elements.forEach((element, index) => {
            element.style.animationDelay = `${index * 0.1}s`;
            element.classList.add('fade-in');
        });
    }
    
    function updateAIStatus(loaded) {
        const statusText = loaded ? 'AI modelleri aktif' : 'Temel analiz kullanılıyor';
        const statusColor = loaded ? '#10b981' : '#f59e0b';
        
        aiStatusText.textContent = statusText;
        aiStatusCard.style.background = loaded 
            ? 'linear-gradient(135deg, #10b981, #34d399)'
            : 'linear-gradient(135deg, #f59e0b, #fbbf24)';
        
        // Update model icons
        const icons = [sentimentModelIcon, emotionModelIcon, turkishModelIcon, embeddingModelIcon];
        icons.forEach(icon => {
            if (loaded) {
                icon.className = 'fas fa-check-circle';
                icon.style.color = '#10b981';
            } else {
                icon.className = 'fas fa-times-circle';
                icon.style.color = '#ef4444';
            }
        });
    }
    
    function updateSentimentSummary(summary) {
        const sentiment = summary.overall_sentiment;
        const confidence = summary.confidence;
        const emotion = summary.emotion;
        
        let sentimentText = '';
        let iconClass = '';
        let iconColor = '';
        
        switch (sentiment) {
            case 'positive':
                sentimentText = `Pozitif (${Math.round(confidence * 100)}% güven)`;
                iconClass = 'fas fa-heart';
                iconColor = '#10b981';
                break;
            case 'negative':
                sentimentText = `Negatif (${Math.round(confidence * 100)}% güven)`;
                iconClass = 'fas fa-heart-broken';
                iconColor = '#ef4444';
                break;
            default:
                sentimentText = `Nötr (${Math.round(confidence * 100)}% güven)`;
                iconClass = 'fas fa-heart';
                iconColor = '#f59e0b';
        }
        
        overallSentiment.textContent = sentimentText;
        
        const summaryIcon = sentimentSummary.querySelector('.summary-icon i');
        summaryIcon.className = iconClass;
        summaryIcon.style.color = 'white';
        sentimentSummary.querySelector('.summary-icon').style.background = `linear-gradient(135deg, ${iconColor}, ${iconColor}dd)`;
    }
    
    function updateDetailedAnalysis(analysis) {
        // Update VADER scores if available
        if (analysis.vader) {
            const { pos, neg, neu, compound } = analysis.vader;
            // You can add more detailed analysis display here
        }
    }
    
    function updateTextAnalysis(analysis) {
        const textAnalysis = analysis.text_analysis;
        
        sentenceCount.textContent = textAnalysis.sentence_count;
        wordCount.textContent = textAnalysis.word_count;
        uniqueWords.textContent = textAnalysis.unique_words;
        lexicalDiversity.textContent = Math.round(textAnalysis.lexical_diversity * 100) + '%';
    }
    
    function updateInsights(insights) {
        insightsContent.innerHTML = '';
        
        insights.forEach(insight => {
            const insightItem = document.createElement('div');
            insightItem.className = 'insight-item';
            insightItem.innerHTML = `<p>${insight}</p>`;
            insightsContent.appendChild(insightItem);
        });
    }
    
    function updateAdvice(advice) {
        adviceList.innerHTML = '';
        
        advice.forEach(item => {
            const adviceItem = document.createElement('div');
            adviceItem.className = 'advice-item';
            adviceItem.innerHTML = `<p>${item}</p>`;
            adviceList.appendChild(adviceItem);
        });
    }
    
    function setLoadingState(loading) {
        if (loading) {
            analyzeBtn.classList.add('loading');
            analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span>AI Analiz Ediliyor...</span>';
            analyzeBtn.disabled = true;
        } else {
            analyzeBtn.classList.remove('loading');
            analyzeBtn.innerHTML = '<i class="fas fa-magic"></i><span>AI Analiz Et</span>';
            analyzeBtn.disabled = false;
        }
    }
    
    function handleNavigation(section) {
        // Remove active class from all nav items
        navItems.forEach(item => item.classList.remove('active'));
        
        // Add active class to clicked item
        const activeItem = document.querySelector(`[data-section="${section}"]`);
        if (activeItem) {
            activeItem.classList.add('active');
        }
        
        // Handle section navigation
        switch (section) {
            case 'home':
                showHomeSection();
                break;
            case 'journal':
                showJournalSection();
                break;
            case 'meditation':
                showMeditationSection();
                break;
            case 'chat':
                showChatSection();
                break;
            case 'profile':
                showProfileSection();
                break;
        }
    }
    
    function showHomeSection() {
        hideAllSections();
        homeSection.style.display = 'block';
    }
    
    function checkAIStatus() {
        fetch('/health')
            .then(response => response.json())
            .then(data => {
                if (data.ai_models_loaded) {
                    console.log('✅ AI modelleri yüklendi');
                } else {
                    console.log('⚠️ Temel analiz kullanılıyor');
                }
            })
            .catch(error => {
                console.log('❌ AI durumu kontrol edilemedi');
            });
    }
    
    function initializeStreakAnimation() {
        const streakDays = document.querySelectorAll('.streak-day');
        streakDays.forEach((day, index) => {
            setTimeout(() => {
                day.classList.add('active');
            }, index * 100);
        });
    }
    
    function showError(message) {
        errorMessage.textContent = message;
        errorModal.classList.add('show');
    }
    
    function closeErrorModal() {
        errorModal.classList.remove('show');
    }
    
    function addTouchSupport() {
        // Add touch feedback to interactive elements
        const touchElements = document.querySelectorAll('.feature-card, .action-card, .nav-item, .session-card, .entry-card, .menu-item');
        
        touchElements.forEach(element => {
            element.addEventListener('touchstart', function() {
                this.style.transform = 'scale(0.95)';
            });
            
            element.addEventListener('touchend', function() {
                this.style.transform = '';
            });
        });
    }
    
    function addAnimations() {
        // Add entrance animations
        const animateElements = document.querySelectorAll('.action-card, .feature-card, .progress-widget, .streak-widget, .stat-card');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                }
            });
        }, { threshold: 0.1 });
        
        animateElements.forEach(element => {
            observer.observe(element);
        });
        
        // Add hover animations
        const hoverElements = document.querySelectorAll('.feature-card, .action-card, .session-card, .entry-card');
        hoverElements.forEach(element => {
            element.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-4px)';
            });
            
            element.addEventListener('mouseleave', function() {
                this.style.transform = '';
            });
        });
    }
    
    // Global functions
    window.closeErrorModal = closeErrorModal;
    
    // Add CSS animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideDown {
            from { transform: translateX(-50%) translateY(-20px); opacity: 0; }
            to { transform: translateX(-50%) translateY(0); opacity: 1; }
        }
        
        @keyframes slideUp {
            from { transform: translateX(-50%) translateY(0); opacity: 1; }
            to { transform: translateX(-50%) translateY(-20px); opacity: 0; }
        }
        
        .feature-notification {
            animation: slideDown 0.3s ease;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        .notification-bell:hover {
            animation: pulse 1s infinite;
        }
    `;
    document.head.appendChild(style);
});
