#!/usr/bin/env python3
"""
Flappy Bird Mobil Uygulama - Kivy ile
Dokunmatik kontroller ve mobil optimizasyonlu versiyon
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle, Ellipse, Color, Line
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.core.audio import SoundLoader
import random
import json
import os

# Mobil optimizasyonlu ayarlar
class MobileConfig:
    # Ekran boyutları (mobil için optimize)
    SCREEN_WIDTH = 400
    SCREEN_HEIGHT = 600
    
    # Karakter ayarları
    CHARACTER_SIZE = 30
    CHARACTER_GRAVITY = 0.8
    CHARACTER_JUMP_STRENGTH = -12
    CHARACTER_START_X = 100
    CHARACTER_START_Y = 300
    
    # Boru ayarları
    PIPE_WIDTH = 60
    PIPE_GAP = 150
    PIPE_SPEED = 3
    PIPE_SPAWN_DISTANCE = 200
    
    # Engel ayarları
    OBSTACLE_SIZE = 35
    OBSTACLE_SPEED = 2
    OBSTACLE_SPAWN_CHANCE = 0.003
    
    # Renkler
    BACKGROUND_COLOR = (0.5, 0.8, 1, 1)  # Açık mavi
    CHARACTER_COLOR = (0, 0.4, 0.8, 1)   # Mavi
    PIPE_COLOR = (0.2, 0.8, 0.2, 1)      # Yeşil
    OBSTACLE_COLOR = (0.8, 0.2, 0.2, 1)  # Kırmızı
    GROUND_COLOR = (0.8, 0.6, 0.2, 1)    # Kahverengi
    
    # Oyun durumları
    GAME_STATES = {
        'MENU': 0,
        'PLAYING': 1,
        'GAME_OVER': 2,
        'PAUSED': 3
    }

class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity_y = 0
        self.size = MobileConfig.CHARACTER_SIZE
        self.rect = [x, y, self.size, self.size]
        
    def jump(self):
        """Karakter zıplama"""
        self.velocity_y = MobileConfig.CHARACTER_JUMP_STRENGTH
        
    def update(self):
        """Karakter pozisyonunu güncelle"""
        # Yerçekimi uygula
        self.velocity_y += MobileConfig.CHARACTER_GRAVITY
        self.y += self.velocity_y
        
        # Sınırları kontrol et
        if self.y < 0:
            self.y = 0
            self.velocity_y = 0
        elif self.y > MobileConfig.SCREEN_HEIGHT - 100:  # Zemin için alan bırak
            self.y = MobileConfig.SCREEN_HEIGHT - 100
            self.velocity_y = 0
            
        self.rect = [self.x, self.y, self.size, self.size]
        
    def get_rect(self):
        return self.rect

class Pipe:
    def __init__(self, x, gap_y):
        self.x = x
        self.gap_y = gap_y
        self.width = MobileConfig.PIPE_WIDTH
        self.gap = MobileConfig.PIPE_GAP
        self.scored = False
        
        # Üst ve alt boru rectangleleri
        self.top_rect = [x, gap_y + self.gap//2, self.width, MobileConfig.SCREEN_HEIGHT]
        self.bottom_rect = [x, 0, self.width, gap_y - self.gap//2]
        
    def update(self):
        self.x -= MobileConfig.PIPE_SPEED
        self.top_rect[0] = self.x
        self.bottom_rect[0] = self.x
        
    def is_off_screen(self):
        return self.x + self.width < 0
        
    def check_collision(self, character_rect):
        char_x, char_y, char_w, char_h = character_rect
        
        # Üst boru çarpışması
        if (char_x < self.top_rect[0] + self.top_rect[2] and
            char_x + char_w > self.top_rect[0] and
            char_y + char_h > self.top_rect[1]):
            return True
            
        # Alt boru çarpışması
        if (char_x < self.bottom_rect[0] + self.bottom_rect[2] and
            char_x + char_w > self.bottom_rect[0] and
            char_y < self.bottom_rect[1] + self.bottom_rect[3]):
            return True
            
        return False
        
    def check_score(self, character_rect):
        if not self.scored and character_rect[0] > self.x + self.width:
            self.scored = True
            return True
        return False

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = MobileConfig.OBSTACLE_SIZE
        self.rect = [x, y, self.size, self.size]
        
    def update(self):
        self.x -= MobileConfig.OBSTACLE_SPEED
        self.rect[0] = self.x
        
    def is_off_screen(self):
        return self.x + self.size < 0
        
    def check_collision(self, character_rect):
        char_x, char_y, char_w, char_h = character_rect
        return (char_x < self.rect[0] + self.rect[2] and
                char_x + char_w > self.rect[0] and
                char_y < self.rect[1] + self.rect[3] and
                char_y + char_h > self.rect[1])

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Oyun durumu
        self.state = MobileConfig.GAME_STATES['MENU']
        self.score = 0
        self.high_score = self.load_high_score()
        
        # Oyun nesneleri
        self.character = Character(MobileConfig.CHARACTER_START_X, MobileConfig.CHARACTER_START_Y)
        self.pipes = []
        self.obstacles = []
        self.pipe_timer = 0
        
        # Ses dosyaları
        self.sounds = self.load_sounds()
        
        # Oyun döngüsü
        Clock.schedule_interval(self.update, 1.0/60.0)  # 60 FPS
        
        # Dokunmatik kontrol - Kivy otomatik olarak on_touch_down metodunu çağırır
        
    def load_sounds(self):
        """Ses dosyalarını yükle"""
        sounds = {}
        try:
            if os.path.exists('assets/sounds/crash_sound.wav'):
                sounds['crash'] = SoundLoader.load('assets/sounds/crash_sound.wav')
        except:
            pass
        return sounds
        
    def load_high_score(self):
        """Yüksek skoru yükle"""
        try:
            if os.path.exists('highscore.json'):
                with open('highscore.json', 'r') as f:
                    data = json.load(f)
                    return data.get('high_score', 0)
        except:
            pass
        return 0
        
    def save_high_score(self):
        """Yüksek skoru kaydet"""
        try:
            with open('highscore.json', 'w') as f:
                json.dump({'high_score': self.high_score}, f)
        except:
            pass
            
    def on_touch_down(self, touch):
        """Dokunmatik kontrol"""
        if self.state == MobileConfig.GAME_STATES['MENU']:
            self.start_game()
        elif self.state == MobileConfig.GAME_STATES['PLAYING']:
            self.character.jump()
        elif self.state == MobileConfig.GAME_STATES['GAME_OVER']:
            self.restart_game()
        elif self.state == MobileConfig.GAME_STATES['PAUSED']:
            self.state = MobileConfig.GAME_STATES['PLAYING']
        return True
            
    def start_game(self):
        """Oyunu başlat"""
        self.state = MobileConfig.GAME_STATES['PLAYING']
        self.score = 0
        self.character = Character(MobileConfig.CHARACTER_START_X, MobileConfig.CHARACTER_START_Y)
        self.pipes = []
        self.obstacles = []
        self.pipe_timer = 0
        
    def restart_game(self):
        """Oyunu yeniden başlat"""
        self.start_game()
        
    def game_over(self, crash_sound=False):
        """Oyun bitişi"""
        self.state = MobileConfig.GAME_STATES['GAME_OVER']
        
        # Yüksek skor kontrolü
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
            
        # Ses çal
        if crash_sound and 'crash' in self.sounds and self.sounds['crash']:
            self.sounds['crash'].play()
            
    def update(self, dt):
        """Oyun döngüsü"""
        if self.state != MobileConfig.GAME_STATES['PLAYING']:
            return
            
        # Karakteri güncelle
        self.character.update()
        
        # Boruları güncelle
        self.pipe_timer += 1
        if self.pipe_timer >= MobileConfig.PIPE_SPAWN_DISTANCE:
            gap_y = random.randint(100, MobileConfig.SCREEN_HEIGHT - 200)
            self.pipes.append(Pipe(MobileConfig.SCREEN_WIDTH, gap_y))
            self.pipe_timer = 0
            
        for pipe in self.pipes[:]:
            pipe.update()
            
            # Skor kontrolü
            if pipe.check_score(self.character.get_rect()):
                self.score += 1
                
            # Çarpışma kontrolü
            if pipe.check_collision(self.character.get_rect()):
                self.game_over()
                return
                
            # Ekran dışı kontrolü
            if pipe.is_off_screen():
                self.pipes.remove(pipe)
                
        # Engelleri güncelle
        if random.random() < MobileConfig.OBSTACLE_SPAWN_CHANCE:
            y = random.randint(50, MobileConfig.SCREEN_HEIGHT - 150)
            self.obstacles.append(Obstacle(MobileConfig.SCREEN_WIDTH, y))
            
        for obstacle in self.obstacles[:]:
            obstacle.update()
            
            # Çarpışma kontrolü
            if obstacle.check_collision(self.character.get_rect()):
                self.game_over(crash_sound=True)
                return
                
            # Ekran dışı kontrolü
            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)
                
        # Zemin çarpışması
        if self.character.y >= MobileConfig.SCREEN_HEIGHT - 100:
            self.game_over()
            
        # Tavan çarpışması
        if self.character.y <= 0:
            self.game_over()
            
        # Çizimi güncelle
        self.canvas.clear()
        self.draw()
        
    def draw(self):
        """Oyunu çiz"""
        with self.canvas:
            # Arkaplan
            Color(*MobileConfig.BACKGROUND_COLOR)
            Rectangle(pos=(0, 0), size=(MobileConfig.SCREEN_WIDTH, MobileConfig.SCREEN_HEIGHT))
            
            # Zemin
            Color(*MobileConfig.GROUND_COLOR)
            Rectangle(pos=(0, 0), size=(MobileConfig.SCREEN_WIDTH, 100))
            
            if self.state != MobileConfig.GAME_STATES['MENU']:
                # Boruları çiz
                Color(*MobileConfig.PIPE_COLOR)
                for pipe in self.pipes:
                    Rectangle(pos=(pipe.top_rect[0], pipe.top_rect[1]), 
                             size=(pipe.top_rect[2], pipe.top_rect[3]))
                    Rectangle(pos=(pipe.bottom_rect[0], pipe.bottom_rect[1]), 
                             size=(pipe.bottom_rect[2], pipe.bottom_rect[3]))
                    
                # Engelleri çiz
                Color(*MobileConfig.OBSTACLE_COLOR)
                for obstacle in self.obstacles:
                    Rectangle(pos=(obstacle.rect[0], obstacle.rect[1]), 
                             size=(obstacle.rect[2], obstacle.rect[3]))
                    
                # Karakteri çiz
                Color(*MobileConfig.CHARACTER_COLOR)
                Ellipse(pos=(self.character.x, self.character.y), 
                       size=(self.character.size, self.character.size))
                       
                # Göz ekle
                Color(1, 1, 1, 1)  # Beyaz
                Ellipse(pos=(self.character.x + 8, self.character.y + 18), size=(6, 6))
                Color(0, 0, 0, 1)  # Siyah
                Ellipse(pos=(self.character.x + 9, self.character.y + 19), size=(4, 4))

class MenuWidget(FloatLayout):
    def __init__(self, game_widget, **kwargs):
        super().__init__(**kwargs)
        self.game_widget = game_widget
        
        # Başlık
        title = Label(text='Flappy Bird\nMobil', 
                     font_size='30sp',
                     halign='center',
                     pos_hint={'center_x': 0.5, 'center_y': 0.7})
        self.add_widget(title)
        
        # Başlat butonu
        start_btn = Button(text='BAŞLAT', 
                          size_hint=(0.6, 0.1),
                          pos_hint={'center_x': 0.5, 'center_y': 0.5})
        start_btn.bind(on_press=self.start_game)
        self.add_widget(start_btn)
        
        # Yüksek skor
        self.high_score_label = Label(text=f'En Yüksek Skor: {self.game_widget.high_score}',
                                     font_size='16sp',
                                     pos_hint={'center_x': 0.5, 'center_y': 0.3})
        self.add_widget(self.high_score_label)
        
    def start_game(self, instance):
        self.game_widget.start_game()
        self.parent.remove_widget(self)

class GameOverWidget(FloatLayout):
    def __init__(self, game_widget, **kwargs):
        super().__init__(**kwargs)
        self.game_widget = game_widget
        
        # Oyun bitti yazısı
        game_over_label = Label(text='OYUN BİTTİ!', 
                               font_size='24sp',
                               pos_hint={'center_x': 0.5, 'center_y': 0.7})
        self.add_widget(game_over_label)
        
        # Skor
        score_label = Label(text=f'Skor: {self.game_widget.score}',
                           font_size='18sp',
                           pos_hint={'center_x': 0.5, 'center_y': 0.6})
        self.add_widget(score_label)
        
        # En yüksek skor
        high_score_label = Label(text=f'En Yüksek: {self.game_widget.high_score}',
                                font_size='16sp',
                                pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(high_score_label)
        
        # Tekrar oyna butonu
        restart_btn = Button(text='TEKRAR OYNA', 
                            size_hint=(0.6, 0.1),
                            pos_hint={'center_x': 0.5, 'center_y': 0.3})
        restart_btn.bind(on_press=self.restart_game)
        self.add_widget(restart_btn)
        
    def restart_game(self, instance):
        self.game_widget.restart_game()
        self.parent.remove_widget(self)

class FlappyBirdMobileApp(App):
    def build(self):
        # Ana layout
        main_layout = FloatLayout()
        
        # Oyun widget'ı
        self.game_widget = GameWidget(size=(MobileConfig.SCREEN_WIDTH, MobileConfig.SCREEN_HEIGHT))
        main_layout.add_widget(self.game_widget)
        
        # Menü widget'ı
        self.menu_widget = MenuWidget(self.game_widget)
        main_layout.add_widget(self.menu_widget)
        
        # Oyun durumu kontrolü
        Clock.schedule_interval(self.check_game_state, 1.0/30.0)
        
        # Pencere boyutunu ayarla
        Window.size = (MobileConfig.SCREEN_WIDTH, MobileConfig.SCREEN_HEIGHT)
        
        return main_layout
        
    def check_game_state(self, dt):
        """Oyun durumunu kontrol et ve UI'yi güncelle"""
        if self.game_widget.state == MobileConfig.GAME_STATES['GAME_OVER']:
            # Game over ekranını göster
            if not any(isinstance(child, GameOverWidget) for child in self.root.children):
                game_over_widget = GameOverWidget(self.game_widget)
                self.root.add_widget(game_over_widget)
                
        # Skor güncelleme
        if hasattr(self, 'score_label'):
            self.score_label.text = f'Skor: {self.game_widget.score}'
            
    def on_start(self):
        """Uygulama başladığında"""
        # Skor label'ı ekle
        self.score_label = Label(text=f'Skor: {self.game_widget.score}',
                                font_size='18sp',
                                pos_hint={'center_x': 0.5, 'top': 0.95})
        self.root.add_widget(self.score_label)

if __name__ == '__main__':
    FlappyBirdMobileApp().run()