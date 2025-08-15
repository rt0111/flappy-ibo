#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flappy Bird Klonu - Ana Dosya
Python 3.10+ ve Pygame 2.5+ ile çalışır
"""

import argparse
import sys
from game import Game


def main():
    """Ana fonksiyon - oyunu başlatır"""
    parser = argparse.ArgumentParser(description='Flappy Bird Klonu')
    parser.add_argument('--windowed', action='store_true', 
                       help='Pencere modunda çalıştır')
    parser.add_argument('--fullscreen', action='store_true', 
                       help='Tam ekran modunda çalıştır')
    parser.add_argument('--large', action='store_true', 
                       help='Büyük ekran modunda çalıştır (2x boyut)')
    
    args = parser.parse_args()
    
    # Çelişkili argümanları kontrol et
    if args.windowed and args.fullscreen:
        print("Hata: --windowed ve --fullscreen aynı anda kullanılamaz!")
        sys.exit(1)
    
    if args.large and args.fullscreen:
        print("Hata: --large ve --fullscreen aynı anda kullanılamaz!")
        sys.exit(1)
    
    # Oyunu başlat
    try:
        game = Game(fullscreen=args.fullscreen, large_screen=args.large)
        game.run()
    except Exception as e:
        print(f"Oyun başlatılırken hata oluştu: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()