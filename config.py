#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flappy Bird Klonu - Konfigürasyon Dosyası
Tüm oyun sabitleri ve ayarları burada tanımlanır
"""

import os
from typing import Dict, Tuple

# Ekran ayarları
SCREEN_WIDTH: int = 288
SCREEN_HEIGHT: int = 512
FPS: int = 60

# Renk tanımları (RGB)
COLORS: Dict[str, Tuple[int, int, int]] = {
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'BLUE': (135, 206, 235),
    'GREEN': (34, 139, 34),
    'BROWN': (139, 69, 19),
    'YELLOW': (255, 255, 0),
    'RED': (255, 0, 0),
    'GRAY': (128, 128, 128)
}

# Kuş ayarları
BIRD_WIDTH: int = 34
BIRD_HEIGHT: int = 24
BIRD_START_X: int = 50
BIRD_START_Y: int = SCREEN_HEIGHT // 2
BIRD_GRAVITY: float = 0.5
BIRD_FLAP_STRENGTH: float = -8.0
BIRD_MAX_FALL_SPEED: float = 10.0
BIRD_ANIMATION_SPEED: int = 10  # Kaç frame'de bir animasyon değişir

# Boru ayarları
PIPE_WIDTH: int = 52
PIPE_GAP: int = 100  # Borular arası boşluk
PIPE_SPEED: float = 2.0
PIPE_SPAWN_DISTANCE: int = 200  # Borular arası mesafe
PIPE_MIN_HEIGHT: int = 50
PIPE_MAX_HEIGHT: int = SCREEN_HEIGHT - PIPE_GAP - 100

# Engel ayarları
OBSTACLE_WIDTH: int = 40
OBSTACLE_HEIGHT: int = 40
OBSTACLE_SPEED: float = PIPE_SPEED
OBSTACLE_SPAWN_CHANCE: float = 0.3  # Her boru spawn'ında engel oluşma şansı

# Zemin ayarları
GROUND_HEIGHT: int = 112
GROUND_SPEED: float = PIPE_SPEED

# Skor ayarları
SCORE_FONT_SIZE: int = 48
SCORE_COLOR: Tuple[int, int, int] = COLORS['WHITE']
SCORE_POSITION: Tuple[int, int] = (SCREEN_WIDTH // 2, 50)

# Ses ayarları
SOUND_VOLUME: float = 0.7

# Dosya yolları
BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR: str = os.path.join(BASE_DIR, 'assets')
IMAGES_DIR: str = os.path.join(ASSETS_DIR, 'images')
SOUNDS_DIR: str = os.path.join(ASSETS_DIR, 'sounds')

# Asset dosya yolları
ASSETS: Dict[str, str] = {
    # Görsel dosyalar
    'character_idle': os.path.join(IMAGES_DIR, 'character_idle.png'),  # İlk görsel - ana karakter
    'character_flap1': os.path.join(IMAGES_DIR, 'character_flap1.png'),
    'character_flap2': os.path.join(IMAGES_DIR, 'character_flap2.png'),
    'pipe_top': os.path.join(IMAGES_DIR, 'pipe_top.png'),
    'pipe_bottom': os.path.join(IMAGES_DIR, 'pipe_bottom.png'),
    'obstacle': os.path.join(IMAGES_DIR, 'obstacle.png'),  # İkinci görsel - engeller
    'background': os.path.join(IMAGES_DIR, 'background.png'),
    'ground': os.path.join(IMAGES_DIR, 'ground.png'),
    
    # Ses dosyaları (şimdilik hepsi crash_sound.wav kullanıyor)
    'flap_sound': os.path.join(SOUNDS_DIR, 'crash_sound.wav'),
    'score_sound': os.path.join(SOUNDS_DIR, 'crash_sound.wav'),
    'hit_sound': os.path.join(SOUNDS_DIR, 'crash_sound.wav'),
    'crash_sound': os.path.join(SOUNDS_DIR, 'crash_sound.wav')  # Çarpışma sesi
}

# Oyun durumları
GAME_STATES: Dict[str, str] = {
    'MENU': 'menu',
    'PLAYING': 'playing',
    'GAME_OVER': 'game_over',
    'PAUSED': 'paused'
}

# Menü ayarları
MENU_TITLE_SIZE: int = 36
MENU_TEXT_SIZE: int = 24
MENU_TITLE_COLOR: Tuple[int, int, int] = COLORS['YELLOW']
MENU_TEXT_COLOR: Tuple[int, int, int] = COLORS['WHITE']

# Yüksek skor dosyası
HIGHSCORE_FILE: str = os.path.join(BASE_DIR, 'highscore.json')

# Kontroller
CONTROLS: Dict[str, str] = {
    'FLAP': 'SPACE veya Sol Mouse Tuşu',
    'PAUSE': 'P',
    'RESTART': 'R (Game Over ekranında)',
    'QUIT': 'ESC'
}