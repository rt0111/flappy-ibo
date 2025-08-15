#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flappy Bird iOS Uygulaması
iOS için optimize edilmiş Kivy tabanlı mobil oyun
"""

import os
import sys
from kivy.config import Config
from kivy.utils import platform

# iOS için özel konfigürasyon
if platform == 'ios':
    # iPhone boyutları (iPhone 12/13/14 için)
    Config.set('graphics', 'width', '390')
    Config.set('graphics', 'height', '844')
    Config.set('graphics', 'resizable', False)
    Config.set('graphics', 'borderless', True)
    Config.set('graphics', 'fullscreen', 'auto')
    
    # iOS performans optimizasyonları
    Config.set('graphics', 'multisamples', '0')
    Config.set('graphics', 'vsync', '1')
    Config.set('input', 'mouse', 'mouse,disable_multitouch')
else:
    # Masaüstü test için
    Config.set('graphics', 'width', '390')
    Config.set('graphics', 'height', '844')
    Config.set('graphics', 'resizable', True)

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.core.audio import SoundLoader
from kivy.resources import resource_find
import random
import json

# iOS için haptic feedback
if platform == 'ios':
    try:
        from pyobjus import autoclass
        UIImpactFeedbackGenerator = autoclass('UIImpactFeedbackGenerator')
        haptic_available = True
    except ImportError:
        haptic_available = False
else:
    haptic_available = False

class iOSConfig:
    """iOS için optimize edilmiş oyun konfigürasyonu"""
    
    # Ekran boyutları (iPhone için optimize)
    SCREEN_WIDTH = 390
    SCREEN_HEIGHT = 844
    
    # Karakter ayarları
    CHARACTER_SIZE = 30
    CHARACTER_GRAVITY = 0.6  # iOS için daha yumuşak
    CHARACTER_JUMP_STRENGTH = -10
    CHARACTER_MAX_VELOCITY = 8
    
    # Boru ayarları
    PIPE_WIDTH = 60
    PIPE_GAP = 180  # iOS için daha geniş
    PIPE_SPEED = 2.5  # iOS için daha yavaş
    PIPE_SPAWN_DISTANCE = 300
    
    # Engel ayarları
    OBSTACLE_SIZE = 25
    OBSTACLE_SPEED = 2
    OBSTACLE_SPAWN_CHANCE = 0.3
    
    # Renkler (iOS tasarım rehberine uygun)
    COLORS = {
        'background': (0.53, 0.81, 0.92, 1),  # Sky blue
        'character': (0.2, 0.6, 1, 1),        # iOS blue
        'character_eye': (1, 1, 1, 1),        # White
        'pipe': (0.2, 0.8, 0.2, 1),           # Green
        'obstacle': (1, 0.3, 0.3, 1),         # Red
        'ground': (0.8, 0.7, 0.4, 1),         # Brown
        'text': (1, 1, 1, 1),                 # White
        'shadow': (0, 0, 0, 0.3)              # Shadow
    }
    
    # Oyun durumları
    GAME_STATES = {
        'MENU': 'menu',
        'PLAYING': 'playing',
        'GAME_OVER': 'game_over',
        'PAUSED': 'paused'
    }

class iOSCharacter:
    """iOS için optimize edilmiş karakter sınıfı"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity_y = 0
        self.size = iOSConfig.CHARACTER_SIZE
        self.animation_frame = 0
        self.animation_timer = 0
        
    def update(self, dt):
        # Yerçekimi
        self.velocity_y += iOSConfig.CHARACTER_GRAVITY
        
        # Maksimum hız sınırı
        if self.velocity_y > iOSConfig.CHARACTER_MAX_VELOCITY:
            self.velocity_y = iOSConfig.CHARACTER_MAX_VELOCITY
        elif self.velocity_y < -iOSConfig.CHARACTER_MAX_VELOCITY:
            self.velocity_y = -iOSConfig.CHARACTER_MAX_VELOCITY
            
        # Pozisyon güncelleme
        self.y += self.velocity_y
        
        # Animasyon
        self.animation_timer += dt
        if self.animation_timer > 0.2:
            self.animation_frame = (self.animation_frame + 1) % 3
            self.animation_timer = 0
    
    def jump(self):
        self.velocity_y = iOSConfig.CHARACTER_JUMP_STRENGTH
        
        # iOS haptic feedback
        if haptic_available:
            try:
                feedback = UIImpactFeedbackGenerator.alloc().init()
                feedback.impactOccurred()
            except:
                pass
    
    def get_rect(self):
        return (self.x - self.size//2, self.y - self.size//2, self.size, self.size)
    
    def draw(self, widget):
        with widget.canvas:
            # Gölge efekti
            Color(*iOSConfig.COLORS['shadow'])
            Ellipse(pos=(self.x - self.size//2 + 2, self.y - self.size//2 - 2), 
                   size=(self.size, self.size))
            
            # Ana karakter
            Color(*iOSConfig.COLORS['character'])
            Ellipse(pos=(self.x - self.size//2, self.y - self.size//2), 
                   size=(self.size, self.size))
            
            # Göz
            Color(*iOSConfig.COLORS['character_eye'])
            eye_size = self.size // 4
            Ellipse(pos=(self.x - eye_size//2 + 5, self.y + 3), 
                   size=(eye_size, eye_size))
            
            # Kanat animasyonu
            if self.animation_frame == 1:
                Color(1, 1, 1, 0.7)
                wing_points = [
                    self.x - 10, self.y + 5,
                    self.x - 20, self.y + 10,
                    self.x - 15, self.y - 5,
                    self.x - 5, self.y
                ]
                Line(points=wing_points, width=2)

class iOSPipe:
    """iOS için optimize edilmiş boru sınıfı"""
    
    def __init__(self, x):
        self.x = x
        self.gap_y = random.randint(150, iOSConfig.SCREEN_HEIGHT - 200)
        self.width = iOSConfig.PIPE_WIDTH
        self.passed = False
        
    def update(self, dt):
        self.x -= iOSConfig.PIPE_SPEED
        
    def get_rects(self):
        # Üst boru
        top_rect = (self.x, self.gap_y + iOSConfig.PIPE_GAP//2, 
                   self.width, iOSConfig.SCREEN_HEIGHT)
        # Alt boru
        bottom_rect = (self.x, 0, self.width, self.gap_y - iOSConfig.PIPE_GAP//2)
        return top_rect, bottom_rect
    
    def draw(self, widget):
        top_rect, bottom_rect = self.get_rects()
        
        with widget.canvas:
            # Boru gölgesi
            Color(*iOSConfig.COLORS['shadow'])
            Rectangle(pos=(top_rect[0] + 2, top_rect[1] - 2), 
                     size=(top_rect[2], top_rect[3]))
            Rectangle(pos=(bottom_rect[0] + 2, bottom_rect[1] - 2), 
                     size=(bottom_rect[2], bottom_rect[3]))
            
            # Ana borular
            Color(*iOSConfig.COLORS['pipe'])
            Rectangle(pos=(top_rect[0], top_rect[1]), 
                     size=(top_rect[2], top_rect[3]))
            Rectangle(pos=(bottom_rect[0], bottom_rect[1]), 
                     size=(bottom_rect[2], bottom_rect[3]))
            
            # Boru kenarları
            Color(0.1, 0.6, 0.1, 1)
            Line(rectangle=(top_rect[0], top_rect[1], top_rect[2], top_rect[3]), width=2)
            Line(rectangle=(bottom_rect[0], bottom_rect[1], bottom_rect[2], bottom_rect[3]), width=2)

class iOSObstacle:
    """iOS için optimize edilmiş engel sınıfı"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = iOSConfig.OBSTACLE_SIZE
        self.rotation = 0
        
    def update(self, dt):
        self.x -= iOSConfig.OBSTACLE_SPEED
        self.rotation += 2  # Dönen animasyon
        
    def get_rect(self):
        return (self.x - self.size//2, self.y - self.size//2, self.size, self.size)
    
    def draw(self, widget):
        with widget.canvas:
            # Engel gölgesi
            Color(*iOSConfig.COLORS['shadow'])
            Rectangle(pos=(self.x - self.size//2 + 2, self.y - self.size//2 - 2), 
                     size=(self.size, self.size))
            
            # Ana engel
            Color(*iOSConfig.COLORS['obstacle'])
            Rectangle(pos=(self.x - self.size//2, self.y - self.size//2), 
                     size=(self.size, self.size))
            
            # Tehlike işareti
            Color(1, 1, 0, 1)  # Sarı
            triangle_points = [
                self.x, self.y + 8,
                self.x - 6, self.y - 4,
                self.x + 6, self.y - 4
            ]
            Line(points=triangle_points + [triangle_points[0], triangle_points[1]], width=2)
            
            # Ünlem işareti
            Color(1, 1, 1, 1)
            Line(points=[self.x, self.y + 2, self.x, self.y - 2], width=2)
            Ellipse(pos=(self.x - 1, self.y - 6), size=(2, 2))

class iOSGameWidget(Widget):
    """iOS için optimize edilmiş ana oyun widget'ı"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (iOSConfig.SCREEN_WIDTH, iOSConfig.SCREEN_HEIGHT)
        
        # Oyun durumu
        self.state = iOSConfig.GAME_STATES['MENU']
        
        # Oyun nesneleri
        self.character = iOSCharacter(100, iOSConfig.SCREEN_HEIGHT // 2)
        self.pipes = []
        self.obstacles = []
        
        # Skor
        self.score = 0
        self.high_score = self.load_high_score()
        
        # Zamanlayıcılar
        self.pipe_timer = 0
        self.obstacle_timer = 0
        
        # Ses dosyaları
        self.load_sounds()
        
        # Oyun döngüsü
        Clock.schedule_interval(self.update, 1.0/60.0)  # 60 FPS
        
        # iOS için dokunmatik optimizasyon
        if platform == 'ios':
            Window.softinput_mode = 'below_target'
    
    def load_sounds(self):
        """Ses dosyalarını yükle"""
        try:
            crash_path = resource_find('crash_sound.wav')
            if not crash_path:
                crash_path = os.path.join('assets', 'sounds', 'crash_sound.wav')
            self.crash_sound = SoundLoader.load(crash_path)
        except:
            self.crash_sound = None
    
    def load_high_score(self):
        """Yüksek skoru yükle"""
        try:
            with open('highscore.json', 'r') as f:
                data = json.load(f)
                return data.get('high_score', 0)
        except:
            return 0
    
    def save_high_score(self):
        """Yüksek skoru kaydet"""
        try:
            with open('highscore.json', 'w') as f:
                json.dump({'high_score': self.high_score}, f)
        except:
            pass
    
    def on_touch_down(self, touch):
        """iOS dokunmatik kontrol"""
        if self.state == iOSConfig.GAME_STATES['MENU']:
            self.start_game()
        elif self.state == iOSConfig.GAME_STATES['PLAYING']:
            self.character.jump()
        elif self.state == iOSConfig.GAME_STATES['GAME_OVER']:
            self.restart_game()
        elif self.state == iOSConfig.GAME_STATES['PAUSED']:
            self.state = iOSConfig.GAME_STATES['PLAYING']
        return True
    
    def start_game(self):
        """Oyunu başlat"""
        self.state = iOSConfig.GAME_STATES['PLAYING']
        self.score = 0
        self.character = iOSCharacter(100, iOSConfig.SCREEN_HEIGHT // 2)
        self.pipes = []
        self.obstacles = []
        self.pipe_timer = 0
        self.obstacle_timer = 0
    
    def restart_game(self):
        """Oyunu yeniden başlat"""
        self.start_game()
    
    def update(self, dt):
        """Oyun döngüsü"""
        if self.state != iOSConfig.GAME_STATES['PLAYING']:
            return
        
        # Karakter güncelleme
        self.character.update(dt)
        
        # Zemin ve tavan kontrolü
        if self.character.y <= 50 or self.character.y >= iOSConfig.SCREEN_HEIGHT - 50:
            self.game_over()
            return
        
        # Boru oluşturma
        self.pipe_timer += dt
        if self.pipe_timer > 2.0:  # iOS için daha uzun aralık
            self.pipes.append(iOSPipe(iOSConfig.SCREEN_WIDTH))
            self.pipe_timer = 0
        
        # Engel oluşturma
        self.obstacle_timer += dt
        if self.obstacle_timer > 3.0 and random.random() < iOSConfig.OBSTACLE_SPAWN_CHANCE:
            obstacle_y = random.randint(100, iOSConfig.SCREEN_HEIGHT - 100)
            self.obstacles.append(iOSObstacle(iOSConfig.SCREEN_WIDTH, obstacle_y))
            self.obstacle_timer = 0
        
        # Borular güncelleme
        for pipe in self.pipes[:]:
            pipe.update(dt)
            
            # Skor kontrolü
            if not pipe.passed and pipe.x + pipe.width < self.character.x:
                pipe.passed = True
                self.score += 1
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()
            
            # Çarpışma kontrolü
            char_rect = self.character.get_rect()
            top_rect, bottom_rect = pipe.get_rects()
            
            if (self.rects_collide(char_rect, top_rect) or 
                self.rects_collide(char_rect, bottom_rect)):
                self.game_over()
                return
            
            # Ekran dışı borular
            if pipe.x + pipe.width < 0:
                self.pipes.remove(pipe)
        
        # Engeller güncelleme
        for obstacle in self.obstacles[:]:
            obstacle.update(dt)
            
            # Çarpışma kontrolü
            if self.rects_collide(self.character.get_rect(), obstacle.get_rect()):
                self.game_over_with_crash()
                return
            
            # Ekran dışı engeller
            if obstacle.x + obstacle.size < 0:
                self.obstacles.remove(obstacle)
        
        # Çizimi yenile
        self.canvas.clear()
        self.draw_game()
    
    def rects_collide(self, rect1, rect2):
        """Dikdörtgen çarpışma kontrolü"""
        return (rect1[0] < rect2[0] + rect2[2] and
                rect1[0] + rect1[2] > rect2[0] and
                rect1[1] < rect2[1] + rect2[3] and
                rect1[1] + rect1[3] > rect2[1])
    
    def game_over(self):
        """Oyun bitti"""
        self.state = iOSConfig.GAME_STATES['GAME_OVER']
    
    def game_over_with_crash(self):
        """Çarpışma ile oyun bitti"""
        if self.crash_sound:
            self.crash_sound.play()
        
        # iOS haptic feedback
        if haptic_available:
            try:
                feedback = UIImpactFeedbackGenerator.alloc().init()
                feedback.impactOccurred()
            except:
                pass
        
        self.game_over()
    
    def draw_game(self):
        """Oyunu çiz"""
        with self.canvas:
            # Arka plan
            Color(*iOSConfig.COLORS['background'])
            Rectangle(pos=(0, 0), size=(iOSConfig.SCREEN_WIDTH, iOSConfig.SCREEN_HEIGHT))
            
            # Zemin
            Color(*iOSConfig.COLORS['ground'])
            Rectangle(pos=(0, 0), size=(iOSConfig.SCREEN_WIDTH, 50))
            
            # Tavan
            Rectangle(pos=(0, iOSConfig.SCREEN_HEIGHT - 50), 
                     size=(iOSConfig.SCREEN_WIDTH, 50))
        
        # Borular
        for pipe in self.pipes:
            pipe.draw(self)
        
        # Engeller
        for obstacle in self.obstacles:
            obstacle.draw(self)
        
        # Karakter
        self.character.draw(self)
        
        # UI çiz
        self.draw_ui()
    
    def draw_ui(self):
        """Kullanıcı arayüzünü çiz"""
        # Skor metni için label widget'ları kullanacağız
        pass

class FlappyBirdiOSApp(App):
    """iOS için optimize edilmiş Flappy Bird uygulaması"""
    
    def build(self):
        # Ana layout
        root = BoxLayout(orientation='vertical')
        
        # Oyun widget'ı
        self.game_widget = iOSGameWidget()
        
        # UI overlay
        self.ui_layout = BoxLayout(orientation='vertical', size_hint=(1, None), height=100)
        
        # Skor label'ı
        self.score_label = Label(
            text='Skor: 0 | En Yüksek: 0',
            font_size='20sp',
            color=iOSConfig.COLORS['text'],
            size_hint=(1, None),
            height=50
        )
        
        # Durum label'ı
        self.status_label = Label(
            text='Başlamak için ekrana dokunun',
            font_size='16sp',
            color=iOSConfig.COLORS['text'],
            size_hint=(1, None),
            height=50
        )
        
        # Layout'a ekle
        self.ui_layout.add_widget(self.score_label)
        self.ui_layout.add_widget(self.status_label)
        
        root.add_widget(self.game_widget)
        root.add_widget(self.ui_layout)
        
        # UI güncelleme zamanlayıcısı
        Clock.schedule_interval(self.update_ui, 1.0/30.0)
        
        # iOS için pencere ayarları
        if platform == 'ios':
            Window.clearcolor = iOSConfig.COLORS['background']
        
        return root
    
    def update_ui(self, dt):
        """UI'yi güncelle"""
        # Skor güncelleme
        self.score_label.text = f'Skor: {self.game_widget.score} | En Yüksek: {self.game_widget.high_score}'
        
        # Durum mesajı
        if self.game_widget.state == iOSConfig.GAME_STATES['MENU']:
            self.status_label.text = 'Başlamak için ekrana dokunun'
        elif self.game_widget.state == iOSConfig.GAME_STATES['PLAYING']:
            self.status_label.text = 'Zıplamak için ekrana dokunun'
        elif self.game_widget.state == iOSConfig.GAME_STATES['GAME_OVER']:
            self.status_label.text = 'Oyun Bitti! Yeniden başlamak için dokunun'
        elif self.game_widget.state == iOSConfig.GAME_STATES['PAUSED']:
            self.status_label.text = 'Duraklatıldı - Devam etmek için dokunun'
    
    def on_pause(self):
        """iOS arka plan geçişi"""
        if self.game_widget.state == iOSConfig.GAME_STATES['PLAYING']:
            self.game_widget.state = iOSConfig.GAME_STATES['PAUSED']
        return True
    
    def on_resume(self):
        """iOS ön plan geçişi"""
        pass

if __name__ == '__main__':
    # iOS için özel başlatma
    if platform == 'ios':
        print("🍎 iOS'ta Flappy Bird başlatılıyor...")
    else:
        print("🖥️ Masaüstünde iOS simülasyonu başlatılıyor...")
    
    FlappyBirdiOSApp().run()