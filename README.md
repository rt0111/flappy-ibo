# Flappy Ibo

Python 3.10+ ve Pygame 2.5+ ile geliştirilmiş klasik Flappy Bird oyununun klonu.

## Özellikler

- 🐦 Klasik Flappy Ibo oyun mekaniği
- 🎮 SPACE tuşu veya mouse ile kontrol
- 🏆 Yüksek skor sistemi
- ⏸️ Duraklama özelliği (P tuşu)
- 🔊 Ses efektleri (opsiyonel)
- 🎨 Kolay asset değiştirme sistemi
- 📱 288x512 piksel klasik mobil çözünürlük
- 🖥️ Pencere ve tam ekran modu desteği

## Kurulum

### 1. Sanal Ortam Oluşturma

```bash
# Windows
python -m venv flappybird_env
flappybird_env\Scripts\activate

# macOS/Linux
python3 -m venv flappybird_env
source flappybird_env/bin/activate
```

### 2. Gerekli Paketleri Yükleme

```bash
pip install -r requirements.txt
```

### 3. Oyunu Çalıştırma

```bash
# Normal pencere modunda
python main.py

# Tam ekran modunda
python main.py --fullscreen

# Pencere modunda (açık belirtim)
python main.py --windowed
```

## Kontroller

- **SPACE** veya **Sol Mouse Tuşu**: Kuşu zıplat
- **P**: Oyunu duraklat/devam ettir
- **R**: Oyun bittiğinde yeniden başlat
- **ESC**: Oyundan çık

## Proje Yapısı

```
flappybird/
├── main.py              # Ana çalıştırma dosyası
├── game.py              # Oyun mantığı ve sınıflar
├── config.py            # Tüm ayarlar ve sabitler
├── requirements.txt     # Gerekli Python paketleri
├── README.md           # Bu dosya
├── highscore.json      # Yüksek skor (otomatik oluşur)
└── assets/
    ├── images/
    │   ├── bird_idle.png      # Kuş varsayılan görseli
    │   ├── bird_flap1.png     # Kuş animasyon kare 1 (opsiyonel)
    │   ├── bird_flap2.png     # Kuş animasyon kare 2 (opsiyonel)
    │   ├── pipe_top.png       # Üst boru görseli
    │   ├── pipe_bottom.png    # Alt boru görseli
    │   ├── background.png     # Arkaplan görseli
    │   └── ground.png         # Zemin görseli
    └── sounds/
        ├── flap.wav           # Zıplama sesi
        ├── score.wav          # Skor sesi
        └── hit.wav            # Çarpışma sesi
```

## Görselleri Nasıl Değiştiririm?

Oyunun görsellerini değiştirmek çok kolay! İşte 5 adımlı rehber:

### 1. Mevcut Görselleri Yedekle
```bash
# Güvenlik için mevcut assets klasörünü yedekle
cp -r assets assets_backup
```

### 2. Yeni Görsellerinizi Hazırlayın
- **Önerilen boyutlar:**
  - `bird_idle.png`: 34x24 piksel
  - `pipe_top.png` ve `pipe_bottom.png`: 52 piksel genişlik, yükseklik değişken
  - `background.png`: 288x512 piksel
  - `ground.png`: 288x112 piksel
- **Format:** PNG önerilir (şeffaflık desteği için)

### 3. Dosyaları Doğru İsimlerle Kaydedin
Yeni görsellerinizi aşağıdaki isimlerle kaydedin:
- `bird_idle.png` (zorunlu)
- `bird_flap1.png` (opsiyonel - animasyon için)
- `bird_flap2.png` (opsiyonel - animasyon için)
- `pipe_top.png`
- `pipe_bottom.png`
- `background.png`
- `ground.png`

### 4. Assets/Images Klasörüne Kopyalayın
```bash
# Yeni görsellerinizi assets/images/ klasörüne kopyalayın
cp yeni_gorseller/* assets/images/
```

### 5. Oyunu Çalıştırın
```bash
python main.py
```

**Not:** Eğer bir görsel dosyası bulunamazsa, oyun otomatik olarak varsayılan renkli şekiller kullanacaktır.

## Ses Dosyalarını Değiştirme

Ses dosyalarını değiştirmek için:

1. WAV formatında ses dosyalarınızı hazırlayın
2. Dosyaları şu isimlerle kaydedin:
   - `flap.wav` (zıplama sesi)
   - `score.wav` (skor sesi)
   - `hit.wav` (çarpışma sesi)
3. `assets/sounds/` klasörüne kopyalayın

## Oyun Ayarlarını Değiştirme

`config.py` dosyasını düzenleyerek oyun ayarlarını değiştirebilirsiniz:

- **Zorluk:** `BIRD_GRAVITY`, `BIRD_FLAP_STRENGTH`, `PIPE_SPEED`
- **Görünüm:** `SCREEN_WIDTH`, `SCREEN_HEIGHT`, `FPS`
- **Renkler:** `COLORS` sözlüğü
- **Boyutlar:** `BIRD_WIDTH`, `PIPE_WIDTH`, `PIPE_GAP` vb.

## Troubleshooting (Sorun Giderme)

### Oyun Başlamıyor

**Problem:** `ModuleNotFoundError: No module named 'pygame'`

**Çözüm:**
```bash
pip install pygame==2.5.2
```

### Ses Çalışmıyor

**Problem:** Ses efektleri duyulmuyor

**Çözüm:**
- Ses dosyalarının `assets/sounds/` klasöründe olduğunu kontrol edin
- Ses dosyalarının WAV formatında olduğunu kontrol edin
- Sistem ses seviyesini kontrol edin
- Oyun sessiz modda çalışmaya devam edecektir

### Görsel Sorunları

**Problem:** Görseller bozuk görünüyor

**Çözüm:**
- Görsel dosyalarının PNG formatında olduğunu kontrol edin
- Dosya isimlerinin tam olarak eşleştiğini kontrol edin
- Dosya yollarında Türkçe karakter kullanmayın

### Performans Sorunları

**Problem:** Oyun yavaş çalışıyor

**Çözüm:**
- `config.py` dosyasında `FPS` değerini düşürün (örn. 30)
- Görsel dosyalarının boyutlarını küçültün
- Diğer uygulamaları kapatın

### Python Sürüm Hatası

**Problem:** `SyntaxError` veya uyumsuzluk hataları

**Çözüm:**
```bash
# Python sürümünüzü kontrol edin
python --version

# Python 3.10+ gereklidir
```

## Geliştirme

Oyunu geliştirmek istiyorsanız:

1. Kodu fork edin
2. Yeni özellikler ekleyin
3. `config.py` dosyasına yeni ayarlar ekleyin
4. Kodunuzu test edin
5. Pull request gönderin

## Lisans

Bu proje eğitim amaçlı geliştirilmiştir. Özgürce kullanabilir ve değiştirebilirsiniz.

## Katkıda Bulunanlar

- Trae AI - Kod geliştirme ve optimizasyon

---

**İyi oyunlar! 🐦**