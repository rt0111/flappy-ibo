#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iOS App Icon Oluşturucu
Flappy Bird için gerekli tüm icon boyutlarını oluşturur
"""

import os
from PIL import Image, ImageDraw, ImageFont
import json

def create_app_icon(size, output_path):
    """iOS app icon oluştur"""
    # Yeni image oluştur
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Arka plan gradyanı (mavi tonları)
    for y in range(size):
        ratio = y / size
        r = int(135 + (70 * ratio))  # 135 -> 205
        g = int(206 + (49 * ratio))  # 206 -> 255
        b = 235  # Sabit mavi
        color = (r, g, b, 255)
        draw.line([(0, y), (size, y)], fill=color)
    
    # Ana karakter (mavi daire)
    char_size = size // 3
    char_x = size // 2
    char_y = size // 2
    
    # Karakter gölgesi
    shadow_offset = size // 40
    draw.ellipse([
        char_x - char_size//2 + shadow_offset,
        char_y - char_size//2 + shadow_offset,
        char_x + char_size//2 + shadow_offset,
        char_y + char_size//2 + shadow_offset
    ], fill=(0, 0, 0, 100))
    
    # Ana karakter
    draw.ellipse([
        char_x - char_size//2,
        char_y - char_size//2,
        char_x + char_size//2,
        char_y + char_size//2
    ], fill=(51, 153, 255, 255))  # Mavi
    
    # Karakter gözü
    eye_size = char_size // 6
    eye_x = char_x + char_size // 6
    eye_y = char_y - char_size // 8
    
    draw.ellipse([
        eye_x - eye_size//2,
        eye_y - eye_size//2,
        eye_x + eye_size//2,
        eye_y + eye_size//2
    ], fill=(255, 255, 255, 255))  # Beyaz göz
    
    # Göz bebeği
    pupil_size = eye_size // 2
    draw.ellipse([
        eye_x - pupil_size//2,
        eye_y - pupil_size//2,
        eye_x + pupil_size//2,
        eye_y + pupil_size//2
    ], fill=(0, 0, 0, 255))  # Siyah bebek
    
    # Kanat
    wing_points = [
        (char_x - char_size//3, char_y),
        (char_x - char_size//2 - char_size//4, char_y - char_size//4),
        (char_x - char_size//2, char_y - char_size//6),
        (char_x - char_size//4, char_y + char_size//8)
    ]
    draw.polygon(wing_points, fill=(255, 255, 255, 200))
    
    # Gaga
    beak_points = [
        (char_x + char_size//3, char_y),
        (char_x + char_size//2, char_y - char_size//8),
        (char_x + char_size//2, char_y + char_size//8)
    ]
    draw.polygon(beak_points, fill=(255, 165, 0, 255))  # Turuncu
    
    # Kaydet
    img.save(output_path, 'PNG')
    print(f"✅ {size}x{size} icon oluşturuldu: {output_path}")

def create_all_ios_icons():
    """Tüm iOS icon boyutlarını oluştur"""
    
    # Çıktı klasörü
    icons_dir = os.path.join('assets', 'ios_icons')
    os.makedirs(icons_dir, exist_ok=True)
    
    # iOS için gerekli icon boyutları
    icon_sizes = {
        # iPhone
        'icon-20.png': 20,
        'icon-20@2x.png': 40,
        'icon-20@3x.png': 60,
        'icon-29.png': 29,
        'icon-29@2x.png': 58,
        'icon-29@3x.png': 87,
        'icon-40.png': 40,
        'icon-40@2x.png': 80,
        'icon-40@3x.png': 120,
        'icon-60@2x.png': 120,
        'icon-60@3x.png': 180,
        
        # iPad
        'icon-20-ipad.png': 20,
        'icon-20@2x-ipad.png': 40,
        'icon-29-ipad.png': 29,
        'icon-29@2x-ipad.png': 58,
        'icon-40-ipad.png': 40,
        'icon-40@2x-ipad.png': 80,
        'icon-76.png': 76,
        'icon-76@2x.png': 152,
        'icon-83.5@2x.png': 167,
        
        # App Store
        'icon-1024.png': 1024,
        
        # Genel boyutlar
        'app_icon.png': 512,
        'app_icon_small.png': 256
    }
    
    print("🎨 iOS App Iconları Oluşturuluyor...")
    print("====================================")
    
    for filename, size in icon_sizes.items():
        output_path = os.path.join(icons_dir, filename)
        create_app_icon(size, output_path)
    
    # Contents.json oluştur (Xcode için)
    contents_json = {
        "images": [
            {
                "size": "20x20",
                "idiom": "iphone",
                "filename": "icon-20@2x.png",
                "scale": "2x"
            },
            {
                "size": "20x20",
                "idiom": "iphone",
                "filename": "icon-20@3x.png",
                "scale": "3x"
            },
            {
                "size": "29x29",
                "idiom": "iphone",
                "filename": "icon-29@2x.png",
                "scale": "2x"
            },
            {
                "size": "29x29",
                "idiom": "iphone",
                "filename": "icon-29@3x.png",
                "scale": "3x"
            },
            {
                "size": "40x40",
                "idiom": "iphone",
                "filename": "icon-40@2x.png",
                "scale": "2x"
            },
            {
                "size": "40x40",
                "idiom": "iphone",
                "filename": "icon-40@3x.png",
                "scale": "3x"
            },
            {
                "size": "60x60",
                "idiom": "iphone",
                "filename": "icon-60@2x.png",
                "scale": "2x"
            },
            {
                "size": "60x60",
                "idiom": "iphone",
                "filename": "icon-60@3x.png",
                "scale": "3x"
            },
            {
                "size": "20x20",
                "idiom": "ipad",
                "filename": "icon-20-ipad.png",
                "scale": "1x"
            },
            {
                "size": "20x20",
                "idiom": "ipad",
                "filename": "icon-20@2x-ipad.png",
                "scale": "2x"
            },
            {
                "size": "29x29",
                "idiom": "ipad",
                "filename": "icon-29-ipad.png",
                "scale": "1x"
            },
            {
                "size": "29x29",
                "idiom": "ipad",
                "filename": "icon-29@2x-ipad.png",
                "scale": "2x"
            },
            {
                "size": "40x40",
                "idiom": "ipad",
                "filename": "icon-40-ipad.png",
                "scale": "1x"
            },
            {
                "size": "40x40",
                "idiom": "ipad",
                "filename": "icon-40@2x-ipad.png",
                "scale": "2x"
            },
            {
                "size": "76x76",
                "idiom": "ipad",
                "filename": "icon-76.png",
                "scale": "1x"
            },
            {
                "size": "76x76",
                "idiom": "ipad",
                "filename": "icon-76@2x.png",
                "scale": "2x"
            },
            {
                "size": "83.5x83.5",
                "idiom": "ipad",
                "filename": "icon-83.5@2x.png",
                "scale": "2x"
            },
            {
                "size": "1024x1024",
                "idiom": "ios-marketing",
                "filename": "icon-1024.png",
                "scale": "1x"
            }
        ],
        "info": {
            "version": 1,
            "author": "xcode"
        }
    }
    
    # Contents.json kaydet
    contents_path = os.path.join(icons_dir, 'Contents.json')
    with open(contents_path, 'w') as f:
        json.dump(contents_json, f, indent=2)
    
    print(f"✅ Contents.json oluşturuldu: {contents_path}")
    
    print("")
    print("🎉 Tüm iOS iconları başarıyla oluşturuldu!")
    print("===========================================")
    print("")
    print("📁 Iconlar şu klasörde: assets/ios_icons/")
    print("")
    print("📋 Xcode'da kullanım:")
    print("1. Xcode projesini açın")
    print("2. Assets.xcassets > AppIcon'a gidin")
    print("3. assets/ios_icons/ klasöründeki iconları sürükleyip bırakın")
    print("4. Her boyut için uygun dosyayı seçin")
    print("")
    print("💡 İpucu: Contents.json dosyası otomatik eşleştirme için kullanılabilir")

def create_launch_screen():
    """iOS launch screen oluştur"""
    
    # Launch screen boyutları (iPhone 12 Pro için)
    width, height = 390, 844
    
    img = Image.new('RGB', (width, height), (135, 206, 235))  # Sky blue
    draw = ImageDraw.Draw(img)
    
    # Gradyan arka plan
    for y in range(height):
        ratio = y / height
        r = int(135 + (70 * ratio))
        g = int(206 + (49 * ratio))
        b = 235
        color = (r, g, b)
        draw.line([(0, y), (width, y)], fill=color)
    
    # Merkez logo
    logo_size = 120
    logo_x = width // 2
    logo_y = height // 2 - 50
    
    # Logo gölgesi
    shadow_offset = 4
    draw.ellipse([
        logo_x - logo_size//2 + shadow_offset,
        logo_y - logo_size//2 + shadow_offset,
        logo_x + logo_size//2 + shadow_offset,
        logo_y + logo_size//2 + shadow_offset
    ], fill=(0, 0, 0, 100))
    
    # Ana logo
    draw.ellipse([
        logo_x - logo_size//2,
        logo_y - logo_size//2,
        logo_x + logo_size//2,
        logo_y + logo_size//2
    ], fill=(51, 153, 255))
    
    # Logo gözü
    eye_size = logo_size // 6
    eye_x = logo_x + logo_size // 6
    eye_y = logo_y - logo_size // 8
    
    draw.ellipse([
        eye_x - eye_size//2,
        eye_y - eye_size//2,
        eye_x + eye_size//2,
        eye_y + eye_size//2
    ], fill=(255, 255, 255))
    
    # Göz bebeği
    pupil_size = eye_size // 2
    draw.ellipse([
        eye_x - pupil_size//2,
        eye_y - pupil_size//2,
        eye_x + pupil_size//2,
        eye_y + pupil_size//2
    ], fill=(0, 0, 0))
    
    # Başlık metni
    try:
        # Sistem fontunu kullanmaya çalış
        font_size = 32
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        # Varsayılan font
        font = ImageFont.load_default()
    
    title_text = "Flappy Bird"
    text_bbox = draw.textbbox((0, 0), title_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (width - text_width) // 2
    text_y = logo_y + logo_size//2 + 30
    
    # Metin gölgesi
    draw.text((text_x + 2, text_y + 2), title_text, fill=(0, 0, 0, 150), font=font)
    # Ana metin
    draw.text((text_x, text_y), title_text, fill=(255, 255, 255), font=font)
    
    # Alt metin
    subtitle_text = "Yükleniyor..."
    try:
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
    except:
        subtitle_font = ImageFont.load_default()
    
    subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    subtitle_y = text_y + 50
    
    draw.text((subtitle_x, subtitle_y), subtitle_text, fill=(255, 255, 255, 200), font=subtitle_font)
    
    # Kaydet
    launch_path = os.path.join('assets', 'ios_icons', 'launch_screen.png')
    img.save(launch_path, 'PNG')
    print(f"✅ Launch screen oluşturuldu: {launch_path}")

if __name__ == '__main__':
    try:
        print("🍎 iOS Icon Oluşturucu Başlatılıyor...")
        print("=====================================")
        
        # Pillow kontrolü
        print("📦 Pillow kütüphanesi kontrol ediliyor...")
        
        # Ana iconları oluştur
        create_all_ios_icons()
        
        # Launch screen oluştur
        print("")
        print("🚀 Launch screen oluşturuluyor...")
        create_launch_screen()
        
        print("")
        print("🎉 iOS Asset'leri başarıyla oluşturuldu!")
        print("========================================")
        print("")
        print("📱 Sonraki adımlar:")
        print("1. assets/ios_icons/ klasörünü kontrol edin")
        print("2. Xcode projesinde Assets.xcassets'e iconları ekleyin")
        print("3. Launch screen'i LaunchScreen.storyboard'a ekleyin")
        print("")
        print("✨ iOS uygulamanız için tüm görseller hazır!")
        
    except ImportError:
        print("❌ HATA: Pillow kütüphanesi bulunamadı!")
        print("")
        print("📦 Kurulum için:")
        print("pip install Pillow")
        print("")
        print("Sonra tekrar çalıştırın:")
        print("python create_ios_icons.py")
    except Exception as e:
        print(f"❌ HATA: {str(e)}")
        print("")
        print("🆘 Sorun yaşıyorsanız iOS_GUIDE.md dosyasını inceleyin")