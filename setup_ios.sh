#!/bin/bash
# iOS için Flappy Bird Kurulum Betiği
# Bu betik macOS'ta çalıştırılmalıdır

set -e  # Hata durumunda dur

echo "🍎 iOS için Flappy Bird Kurulum Başlatılıyor..."
echo "================================================"

# Sistem kontrolü
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ HATA: Bu betik sadece macOS'ta çalışır!"
    echo "iOS geliştirme için Mac bilgisayar gereklidir."
    exit 1
fi

# Xcode kontrolü
if ! command -v xcodebuild &> /dev/null; then
    echo "❌ HATA: Xcode bulunamadı!"
    echo "Lütfen App Store'dan Xcode'u indirin ve kurun."
    exit 1
fi

echo "✅ macOS ve Xcode tespit edildi"

# Python kontrolü
if ! command -v python3 &> /dev/null; then
    echo "❌ HATA: Python3 bulunamadı!"
    echo "Lütfen Python 3.8+ sürümünü kurun."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python $PYTHON_VERSION tespit edildi"

# Homebrew kontrolü ve kurulumu
if ! command -v brew &> /dev/null; then
    echo "📦 Homebrew kuruluyor..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "✅ Homebrew mevcut"
fi

# Gerekli araçları kur
echo "🔧 Gerekli araçlar kuruluyor..."
brew install git python3 autoconf automake libtool pkg-config
brew install --cask xquartz  # X11 desteği için

# Python sanal ortam oluştur
echo "🐍 Python sanal ortamı oluşturuluyor..."
if [ ! -d "venv_ios" ]; then
    python3 -m venv venv_ios
fi

source venv_ios/bin/activate

# Python paketlerini güncelle
echo "📦 Python paketleri kuruluyor..."
pip install --upgrade pip setuptools wheel

# kivy-ios kurulumu
echo "📱 kivy-ios kuruluyor..."
pip install kivy-ios

# iOS toolchain oluştur (uzun sürebilir)
echo "🔨 iOS toolchain oluşturuluyor... (Bu işlem 30-60 dakika sürebilir)"
echo "☕ Kahve molası verebilirsiniz!"

# Gerekli kütüphaneleri derle
toolchain build python3
toolchain build kivy

echo "✅ iOS toolchain hazır!"

# Proje klasörü oluştur
echo "📁 iOS projesi oluşturuluyor..."
if [ ! -d "FlappyBird-ios" ]; then
    toolchain create FlappyBird $(pwd)
else
    echo "⚠️  iOS projesi zaten mevcut"
fi

# Asset'leri kopyala
echo "🎨 Asset'ler kopyalanıyor..."
cp -r assets/* FlappyBird-ios/data/ 2>/dev/null || echo "⚠️  Asset kopyalama hatası (normal olabilir)"

# Ana dosyayı kopyala
cp main_ios.py FlappyBird-ios/main.py

# App icon oluştur (basit versiyon)
echo "🎯 App icon oluşturuluyor..."
if [ -f "assets/images/character_idle.png" ]; then
    # ImageMagick ile icon boyutları oluştur
    if command -v convert &> /dev/null; then
        mkdir -p FlappyBird-ios/data/icons
        
        # Farklı boyutlarda iconlar oluştur
        convert assets/images/character_idle.png -resize 20x20 FlappyBird-ios/data/icons/icon-20.png
        convert assets/images/character_idle.png -resize 29x29 FlappyBird-ios/data/icons/icon-29.png
        convert assets/images/character_idle.png -resize 40x40 FlappyBird-ios/data/icons/icon-40.png
        convert assets/images/character_idle.png -resize 60x60 FlappyBird-ios/data/icons/icon-60.png
        convert assets/images/character_idle.png -resize 76x76 FlappyBird-ios/data/icons/icon-76.png
        convert assets/images/character_idle.png -resize 83x83 FlappyBird-ios/data/icons/icon-83.5.png
        convert assets/images/character_idle.png -resize 1024x1024 FlappyBird-ios/data/icons/icon-1024.png
        
        echo "✅ App iconları oluşturuldu"
    else
        echo "⚠️  ImageMagick bulunamadı, iconlar manuel oluşturulmalı"
        echo "brew install imagemagick komutu ile kurabilirsiniz"
    fi
fi

# Xcode projesi aç
echo "🚀 Xcode projesi açılıyor..."
if [ -f "FlappyBird-ios/FlappyBird.xcodeproj/project.pbxproj" ]; then
    open FlappyBird-ios/FlappyBird.xcodeproj
else
    echo "⚠️  Xcode projesi bulunamadı"
fi

echo ""
echo "🎉 iOS Kurulumu Tamamlandı!"
echo "================================"
echo ""
echo "📋 Sonraki Adımlar:"
echo "1. Xcode'da Bundle Identifier'ı değiştirin (com.yourname.flappybird)"
echo "2. Apple Developer hesabınızı Signing & Capabilities'e ekleyin"
echo "3. iPhone Simulator'da test edin"
echo "4. Gerçek cihazda test edin"
echo "5. Archive oluşturup App Store'a yükleyin"
echo ""
echo "📱 Test için: Product > Run (⌘+R)"
echo "📦 Archive için: Product > Archive"
echo ""
echo "🆘 Sorun yaşarsanız iOS_GUIDE.md dosyasını inceleyin"
echo ""
echo "✨ Başarılar! iOS uygulamanız hazır!"

# Sanal ortamı deaktive et
deactivate