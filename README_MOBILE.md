# 📱 Flappy Bird Mobil Uygulama

Pygame tabanlı Flappy Bird oyununun Kivy ile geliştirilmiş mobil versiyonu.

## 🚀 Hızlı Başlangıç

### 1️⃣ Gereksinimler
```bash
# Python 3.8+ gerekli
python --version

# Kivy kurulumu
pip install -r requirements_mobile.txt
```

### 2️⃣ Masaüstünde Test
```bash
# Mobil uygulamayı masaüstünde çalıştır
python mobile_app.py
```

## 📱 Android APK Oluşturma

### Gereksinimler
- Linux veya macOS (Windows için WSL önerilir)
- Android SDK
- Java JDK 8+

### Adımlar

1. **Buildozer Kurulumu**
```bash
pip install buildozer
```

2. **Android Geliştirme Ortamı**
```bash
# Ubuntu/Debian için
sudo apt update
sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Android SDK kurulumu (buildozer otomatik yapacak)
```

3. **APK Oluşturma**
```bash
# İlk kez (uzun sürebilir - 30-60 dakika)
buildozer android debug

# Sonraki derlemeler (daha hızlı)
buildozer android debug
```

4. **APK Dosyası**
```
bin/flappybirdmobile-0.1-arm64-v8a-debug.apk
```

## 🎮 Oyun Kontrolleri

### Dokunmatik Kontroller
- **Ekrana dokun**: Karakter zıplama
- **Menüde dokun**: Oyunu başlat
- **Oyun bittiğinde dokun**: Yeniden başlat

### Oyun Mekaniği
- **Mavi karakter**: Ana oyuncu
- **Yeşil borular**: Klasik engeller
- **Kırmızı kareler**: Özel engeller (crash sesi ile)
- **Skor sistemi**: Boruları geçmek için puan
- **Yüksek skor**: Otomatik kayıt

## 🔧 Özelleştirme

### Ayarları Değiştirme
`mobile_app.py` dosyasındaki `MobileConfig` sınıfını düzenleyin:

```python
class MobileConfig:
    SCREEN_WIDTH = 400          # Ekran genişliği
    SCREEN_HEIGHT = 600         # Ekran yüksekliği
    CHARACTER_GRAVITY = 0.8     # Yerçekimi kuvveti
    CHARACTER_JUMP_STRENGTH = -12  # Zıplama gücü
    PIPE_SPEED = 3              # Boru hızı
    OBSTACLE_SPEED = 2          # Engel hızı
```

### Görselleri Değiştirme
- `assets/images/` klasöründeki PNG dosyalarını değiştirin
- Kivy otomatik olarak yeni görselleri yükleyecek

### Sesleri Değiştirme
- `assets/sounds/` klasöründeki WAV dosyalarını değiştirin
- Desteklenen formatlar: WAV, MP3, OGG

## 📦 Dağıtım

### Google Play Store
1. **Release APK oluştur**
```bash
buildozer android release
```

2. **APK'yı imzala**
```bash
# Keystore oluştur
keytool -genkey -v -keystore my-release-key.keystore -alias alias_name -keyalg RSA -keysize 2048 -validity 10000

# APK'yı imzala
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore my-release-key.keystore bin/flappybirdmobile-0.1-arm64-v8a-release-unsigned.apk alias_name

# Zipalign
zipalign -v 4 bin/flappybirdmobile-0.1-arm64-v8a-release-unsigned.apk FlappyBirdMobile.apk
```

3. **Google Play Console'a yükle**

### Alternatif Dağıtım
- **APK Direct**: APK dosyasını doğrudan paylaş
- **F-Droid**: Açık kaynak uygulama mağazası
- **Amazon Appstore**: Amazon cihazları için

## 🐛 Sorun Giderme

### Yaygın Sorunlar

**1. Buildozer hatası**
```bash
# Temiz derleme
buildozer android clean
buildozer android debug
```

**2. Ses çalmıyor**
- Ses dosyalarının WAV formatında olduğundan emin olun
- Dosya yollarını kontrol edin

**3. APK çalışmıyor**
- Android sürümünü kontrol edin (minimum API 21)
- Cihaz mimarisini kontrol edin (ARM64/ARMv7)

**4. Performans sorunları**
- FPS'i düşürün (Clock.schedule_interval değerini artırın)
- Grafik kalitesini azaltın

### Log Kontrolü
```bash
# Android cihazda log kontrolü
adb logcat | grep python
```

## 📋 Sistem Gereksinimleri

### Geliştirme
- **Python**: 3.8+
- **RAM**: 4GB+
- **Disk**: 10GB+ (Android SDK için)
- **OS**: Linux/macOS/Windows (WSL)

### Hedef Cihazlar
- **Android**: 5.0+ (API 21+)
- **RAM**: 1GB+
- **Çözünürlük**: 480x800+

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun
3. Değişikliklerinizi commit edin
4. Pull request gönderin

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🆘 Destek

Sorularınız için:
- GitHub Issues
- E-posta: [email]
- Discord: [server]

---

**Not**: İlk APK derlemesi uzun sürebilir (30-60 dakika). Sabırlı olun! 🕐