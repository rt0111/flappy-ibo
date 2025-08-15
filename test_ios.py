#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iOS Test Betiği
Flappy Bird iOS uygulamasını masaüstünde test eder
"""

import sys
import os
from kivy.config import Config

# iOS simülasyonu için ayarlar
Config.set('graphics', 'width', '390')
Config.set('graphics', 'height', '844')
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'borderless', False)
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', '100')
Config.set('graphics', 'top', '100')

# iOS test modunu aktifleştir
os.environ['KIVY_PLATFORM'] = 'ios_simulator'

print("🍎 iOS Simülatörü Başlatılıyor...")
print("================================")
print("")
print("📱 iPhone 12 Pro boyutları: 390x844")
print("🎮 Dokunmatik kontroller aktif")
print("🔊 Ses efektleri test edilecek")
print("")
print("⌨️  Test kontrolleri:")
print("- Fare tıklaması = Dokunmatik")
print("- SPACE = Zıplama")
print("- ESC = Çıkış")
print("")
print("🚀 Uygulama başlatılıyor...")
print("")

# iOS uygulamasını çalıştır
try:
    from main_ios import FlappyBirdiOSApp
    app = FlappyBirdiOSApp()
    app.title = "Flappy Bird iOS Test"
    app.run()
except ImportError as e:
    print(f"❌ HATA: {e}")
    print("")
    print("📦 Gerekli kütüphaneler:")
    print("pip install kivy")
    print("")
    print("📁 Gerekli dosyalar:")
    print("- main_ios.py")
    print("- assets/ klasörü")
except Exception as e:
    print(f"❌ Uygulama hatası: {e}")
    print("")
    print("🔧 Sorun giderme:")
    print("1. main_ios.py dosyasının mevcut olduğunu kontrol edin")
    print("2. assets/ klasörünün mevcut olduğunu kontrol edin")
    print("3. Kivy'nin doğru kurulduğunu kontrol edin")
    print("")
    print("📋 Detaylı bilgi için iOS_GUIDE.md dosyasını inceleyin")