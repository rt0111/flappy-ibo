#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flappy Bird Klonu - Ana Oyun Dosyası
Tüm oyun sınıfları ve mantığı burada tanımlanır
"""

import pygame
import random
import json
import os
from typing import List, Tuple, Optional
from config import *


class Bird:
    """Kuş sınıfı - oyuncunun kontrol ettiği karakter"""
    
    def __init__(self, x: int, y: int):
        """Kuş nesnesini başlatır"""
        self.x = x
        self.y = y
        self.velocity = 0.0
        self.rect = pygame.Rect(x, y, BIRD_WIDTH, BIRD_HEIGHT)
        
        # Animasyon için
        self.animation_frame = 0
        self.animation_counter = 0
        
        # Görselleri yükle
        self.images = self._load_images()
        self.current_image = self.images[0]
    
    def _load_images(self) -> List[pygame.Surface]:
        """Karakter görsellerini yükler veya varsayılan oluşturur"""
        images = []
        
        # Ana karakter görseli
        try:
            if os.path.exists(ASSETS['character_idle']):
                img = pygame.image.load(ASSETS['character_idle'])
                img = pygame.transform.scale(img, (BIRD_WIDTH, BIRD_HEIGHT))
                images.append(img)
            else:
                # Varsayılan karakter görseli (mavi daire)
                img = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT), pygame.SRCALPHA)
                pygame.draw.circle(img, COLORS['BLUE'], 
                                 (BIRD_WIDTH//2, BIRD_HEIGHT//2), BIRD_WIDTH//2)
                pygame.draw.circle(img, COLORS['BLACK'], 
                                 (BIRD_WIDTH//2 + 5, BIRD_HEIGHT//2 - 3), 3)
                images.append(img)
        except pygame.error:
            # Hata durumunda varsayılan görsel
            img = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT), pygame.SRCALPHA)
            pygame.draw.circle(img, COLORS['BLUE'], 
                             (BIRD_WIDTH//2, BIRD_HEIGHT//2), BIRD_WIDTH//2)
            images.append(img)
        
        # Animasyon kareleri
        for flap_file in ['character_flap1', 'character_flap2']:
            try:
                if os.path.exists(ASSETS[flap_file]):
                    img = pygame.image.load(ASSETS[flap_file])
                    img = pygame.transform.scale(img, (BIRD_WIDTH, BIRD_HEIGHT))
                    images.append(img)
            except (pygame.error, KeyError):
                pass
        
        # En az bir görsel olduğundan emin ol
        if not images:
            img = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT), pygame.SRCALPHA)
            pygame.draw.circle(img, COLORS['BLUE'], 
                             (BIRD_WIDTH//2, BIRD_HEIGHT//2), BIRD_WIDTH//2)
            images.append(img)
        
        return images
    
    def flap(self):
        """Kuşu zıplatır"""
        self.velocity = BIRD_FLAP_STRENGTH
    
    def update(self):
        """Kuşun pozisyonunu ve animasyonunu günceller"""
        # Yerçekimi uygula
        self.velocity += BIRD_GRAVITY
        
        # Maksimum düşme hızını sınırla
        if self.velocity > BIRD_MAX_FALL_SPEED:
            self.velocity = BIRD_MAX_FALL_SPEED
        
        # Pozisyonu güncelle
        self.y += self.velocity
        self.rect.y = int(self.y)
        
        # Animasyonu güncelle
        self.animation_counter += 1
        if self.animation_counter >= BIRD_ANIMATION_SPEED:
            self.animation_counter = 0
            self.animation_frame = (self.animation_frame + 1) % len(self.images)
            self.current_image = self.images[self.animation_frame]
    
    def draw(self, screen: pygame.Surface):
        """Kuşu ekrana çizer"""
        screen.blit(self.current_image, (self.x, int(self.y)))
    
    def get_rect(self) -> pygame.Rect:
        """Çarpışma tespiti için rect döndürür"""
        return self.rect


class Pipe:
    """Boru sınıfı - engeller"""
    
    def __init__(self, x: int, gap_y: int):
        """Boru çiftini oluşturur"""
        self.x = x
        self.gap_y = gap_y
        self.passed = False
        
        # Üst ve alt boru rect'leri
        self.top_rect = pygame.Rect(x, 0, PIPE_WIDTH, gap_y)
        self.bottom_rect = pygame.Rect(x, gap_y + PIPE_GAP, PIPE_WIDTH, 
                                     SCREEN_HEIGHT - gap_y - PIPE_GAP)
        
        # Görselleri yükle
        self.top_image, self.bottom_image = self._load_images()
    
    def _load_images(self) -> Tuple[pygame.Surface, pygame.Surface]:
        """Boru görsellerini yükler veya varsayılan oluşturur"""
        try:
            # Üst boru
            if os.path.exists(ASSETS['pipe_top']):
                top_img = pygame.image.load(ASSETS['pipe_top'])
                top_img = pygame.transform.scale(top_img, (PIPE_WIDTH, self.gap_y))
            else:
                top_img = pygame.Surface((PIPE_WIDTH, self.gap_y))
                top_img.fill(COLORS['GREEN'])
                pygame.draw.rect(top_img, COLORS['BLACK'], 
                               (0, 0, PIPE_WIDTH, self.gap_y), 2)
            
            # Alt boru
            bottom_height = SCREEN_HEIGHT - self.gap_y - PIPE_GAP
            if os.path.exists(ASSETS['pipe_bottom']):
                bottom_img = pygame.image.load(ASSETS['pipe_bottom'])
                bottom_img = pygame.transform.scale(bottom_img, (PIPE_WIDTH, bottom_height))
            else:
                bottom_img = pygame.Surface((PIPE_WIDTH, bottom_height))
                bottom_img.fill(COLORS['GREEN'])
                pygame.draw.rect(bottom_img, COLORS['BLACK'], 
                               (0, 0, PIPE_WIDTH, bottom_height), 2)
            
            return top_img, bottom_img
            
        except pygame.error:
            # Hata durumunda varsayılan görsel
            top_img = pygame.Surface((PIPE_WIDTH, self.gap_y))
            top_img.fill(COLORS['GREEN'])
            
            bottom_height = SCREEN_HEIGHT - self.gap_y - PIPE_GAP
            bottom_img = pygame.Surface((PIPE_WIDTH, bottom_height))
            bottom_img.fill(COLORS['GREEN'])
            
            return top_img, bottom_img
    
    def update(self):
        """Borunun pozisyonunu günceller"""
        self.x -= PIPE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x
    
    def draw(self, screen: pygame.Surface):
        """Boruları ekrana çizer"""
        screen.blit(self.top_image, (self.x, 0))
        screen.blit(self.bottom_image, (self.x, self.gap_y + PIPE_GAP))
    
    def is_off_screen(self) -> bool:
        """Boru ekrandan çıktı mı kontrol eder"""
        return self.x + PIPE_WIDTH < 0
    
    def check_collision(self, bird_rect: pygame.Rect) -> bool:
        """Kuş ile çarpışma kontrolü"""
        return bird_rect.colliderect(self.top_rect) or bird_rect.colliderect(self.bottom_rect)
    
    def check_score(self, bird_rect: pygame.Rect) -> bool:
        """Kuş boruyu geçti mi kontrol eder"""
        if not self.passed and bird_rect.x > self.x + PIPE_WIDTH:
            self.passed = True
            return True
        return False


class PipeManager:
    """Boru yöneticisi - boruları oluşturur ve yönetir"""
    
    def __init__(self):
        """Boru yöneticisini başlatır"""
        self.pipes: List[Pipe] = []
        self.spawn_timer = 0
    
    def update(self) -> int:
        """Boruları günceller ve skor artışını döndürür"""
        score_increase = 0
        
        # Mevcut boruları güncelle
        for pipe in self.pipes[:]:
            pipe.update()
            
            # Ekrandan çıkan boruları kaldır
            if pipe.is_off_screen():
                self.pipes.remove(pipe)
        
        # Yeni boru oluştur
        self.spawn_timer += 1
        if self.spawn_timer >= PIPE_SPAWN_DISTANCE / PIPE_SPEED:
            self.spawn_timer = 0
            self.spawn_pipe()
        
        return score_increase
    
    def spawn_pipe(self):
        """Yeni boru çifti oluşturur"""
        gap_y = random.randint(PIPE_MIN_HEIGHT, PIPE_MAX_HEIGHT)
        pipe = Pipe(SCREEN_WIDTH, gap_y)
        self.pipes.append(pipe)
        return True  # Boru oluşturuldu sinyali
    
    def draw(self, screen: pygame.Surface):
        """Tüm boruları çizer"""
        for pipe in self.pipes:
            pipe.draw(screen)
    
    def check_collisions(self, bird_rect: pygame.Rect) -> bool:
        """Kuş ile boru çarpışmalarını kontrol eder"""
        for pipe in self.pipes:
            if pipe.check_collision(bird_rect):
                return True
        return False
    
    def check_score(self, bird_rect: pygame.Rect) -> int:
        """Skor artışını kontrol eder"""
        score_increase = 0
        for pipe in self.pipes:
            if pipe.check_score(bird_rect):
                score_increase += 1
        return score_increase
    
    def reset(self):
        """Tüm boruları temizler"""
        self.pipes.clear()
        self.spawn_timer = 0


class Obstacle:
    """Engel sınıfı - ikinci görseldeki engeller"""
    
    def __init__(self, x: int, y: int):
        """Engel nesnesini oluşturur"""
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
        self.image = self._load_image()
    
    def _load_image(self) -> pygame.Surface:
        """Engel görselini yükler veya varsayılan oluşturur"""
        try:
            if os.path.exists(ASSETS['obstacle']):
                img = pygame.image.load(ASSETS['obstacle'])
                img = pygame.transform.scale(img, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
                return img
            else:
                # Varsayılan engel görseli (kırmızı kare)
                img = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
                img.fill(COLORS['RED'])
                pygame.draw.rect(img, COLORS['BLACK'], 
                               (0, 0, OBSTACLE_WIDTH, OBSTACLE_HEIGHT), 2)
                return img
        except pygame.error:
            # Hata durumunda varsayılan
            img = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
            img.fill(COLORS['RED'])
            return img
    
    def update(self):
        """Engelin pozisyonunu günceller"""
        self.x -= OBSTACLE_SPEED
        self.rect.x = self.x
    
    def draw(self, screen: pygame.Surface):
        """Engeli ekrana çizer"""
        screen.blit(self.image, (self.x, self.y))
    
    def is_off_screen(self) -> bool:
        """Engel ekrandan çıktı mı kontrol eder"""
        return self.x + OBSTACLE_WIDTH < 0
    
    def check_collision(self, bird_rect: pygame.Rect) -> bool:
        """Karakter ile çarpışma kontrolü"""
        return bird_rect.colliderect(self.rect)


class ObstacleManager:
    """Engel yöneticisi - engelleri oluşturur ve yönetir"""
    
    def __init__(self):
        """Engel yöneticisini başlatır"""
        self.obstacles: List[Obstacle] = []
    
    def update(self):
        """Engelleri günceller"""
        # Mevcut engelleri güncelle
        for obstacle in self.obstacles[:]:
            obstacle.update()
            
            # Ekrandan çıkan engelleri kaldır
            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)
    
    def spawn_obstacle(self):
        """Rastgele pozisyonda yeni engel oluşturur"""
        if random.random() < OBSTACLE_SPAWN_CHANCE:
            # Rastgele y pozisyonu (zemin ve tavan arasında)
            y = random.randint(50, SCREEN_HEIGHT - GROUND_HEIGHT - OBSTACLE_HEIGHT - 50)
            obstacle = Obstacle(SCREEN_WIDTH, y)
            self.obstacles.append(obstacle)
    
    def draw(self, screen: pygame.Surface):
        """Tüm engelleri çizer"""
        for obstacle in self.obstacles:
            obstacle.draw(screen)
    
    def check_collisions(self, bird_rect: pygame.Rect) -> bool:
        """Karakter ile engel çarpışmalarını kontrol eder"""
        for obstacle in self.obstacles:
            if obstacle.check_collision(bird_rect):
                return True
        return False
    
    def reset(self):
        """Tüm engelleri temizler"""
        self.obstacles.clear()


class Ground:
    """Zemin sınıfı - hareket eden zemin"""
    
    def __init__(self):
        """Zemini başlatır"""
        self.x1 = 0
        self.x2 = SCREEN_WIDTH
        self.y = SCREEN_HEIGHT - GROUND_HEIGHT
        self.image = self._load_image()
    
    def _load_image(self) -> pygame.Surface:
        """Zemin görselini yükler veya varsayılan oluşturur"""
        try:
            if os.path.exists(ASSETS['ground']):
                img = pygame.image.load(ASSETS['ground'])
                img = pygame.transform.scale(img, (SCREEN_WIDTH, GROUND_HEIGHT))
                return img
            else:
                # Varsayılan zemin görseli
                img = pygame.Surface((SCREEN_WIDTH, GROUND_HEIGHT))
                img.fill(COLORS['BROWN'])
                # Çimen efekti
                for i in range(0, SCREEN_WIDTH, 10):
                    pygame.draw.line(img, COLORS['GREEN'], 
                                   (i, 0), (i + 5, 10), 2)
                return img
        except pygame.error:
            # Hata durumunda varsayılan
            img = pygame.Surface((SCREEN_WIDTH, GROUND_HEIGHT))
            img.fill(COLORS['BROWN'])
            return img
    
    def update(self):
        """Zemin hareketini günceller"""
        self.x1 -= GROUND_SPEED
        self.x2 -= GROUND_SPEED
        
        # Sonsuz döngü için pozisyonları sıfırla
        if self.x1 <= -SCREEN_WIDTH:
            self.x1 = SCREEN_WIDTH
        if self.x2 <= -SCREEN_WIDTH:
            self.x2 = SCREEN_WIDTH
    
    def draw(self, screen: pygame.Surface):
        """Zemini çizer"""
        screen.blit(self.image, (self.x1, self.y))
        screen.blit(self.image, (self.x2, self.y))
    
    def get_rect(self) -> pygame.Rect:
        """Çarpışma tespiti için rect döndürür"""
        return pygame.Rect(0, self.y, SCREEN_WIDTH, GROUND_HEIGHT)


class Background:
    """Arkaplan sınıfı"""
    
    def __init__(self):
        """Arkaplanı başlatır"""
        self.image = self._load_image()
    
    def _load_image(self) -> pygame.Surface:
        """Arkaplan görselini yükler veya varsayılan oluşturur"""
        try:
            if os.path.exists(ASSETS['background']):
                img = pygame.image.load(ASSETS['background'])
                img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                return img
            else:
                # Varsayılan arkaplan (gökyüzü gradyanı)
                img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                for y in range(SCREEN_HEIGHT):
                    color_ratio = y / SCREEN_HEIGHT
                    r = int(135 + (255 - 135) * color_ratio)
                    g = int(206 + (255 - 206) * color_ratio)
                    b = int(235 + (255 - 235) * color_ratio)
                    pygame.draw.line(img, (r, g, b), (0, y), (SCREEN_WIDTH, y))
                return img
        except pygame.error:
            # Hata durumunda düz mavi
            img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            img.fill(COLORS['BLUE'])
            return img
    
    def draw(self, screen: pygame.Surface):
        """Arkaplanı çizer"""
        screen.blit(self.image, (0, 0))


class SoundManager:
    """Ses yöneticisi - tüm ses efektlerini yönetir"""
    
    def __init__(self):
        """Ses yöneticisini başlatır"""
        self.sounds = {}
        self.enabled = True
        
        try:
            pygame.mixer.init()
            self._load_sounds()
        except pygame.error:
            self.enabled = False
            print("Uyarı: Ses sistemi başlatılamadı. Oyun sessiz çalışacak.")
    
    def _load_sounds(self):
        """Ses dosyalarını yükler"""
        sound_files = ['flap_sound', 'score_sound', 'hit_sound', 'crash_sound']
        
        for sound_name in sound_files:
            try:
                if os.path.exists(ASSETS[sound_name]):
                    sound = pygame.mixer.Sound(ASSETS[sound_name])
                    sound.set_volume(SOUND_VOLUME)
                    self.sounds[sound_name] = sound
                    print(f"Ses yüklendi: {sound_name}")
                else:
                    print(f"Ses dosyası bulunamadı: {ASSETS.get(sound_name, sound_name)}")
            except (pygame.error, KeyError) as e:
                print(f"Ses yükleme hatası {sound_name}: {e}")
                pass
    
    def play(self, sound_name: str):
        """Belirtilen sesi çalar"""
        if self.enabled and sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except pygame.error:
                pass


class Game:
    """Ana oyun sınıfı - tüm oyun mantığını yönetir"""
    
    def __init__(self, fullscreen: bool = False, large_screen: bool = False):
        """Oyunu başlatır"""
        pygame.init()
        
        # Ekran boyutunu belirle
        if large_screen:
            screen_width = SCREEN_WIDTH * 2
            screen_height = SCREEN_HEIGHT * 2
            self.scale_factor = 2.0
        else:
            screen_width = SCREEN_WIDTH
            screen_height = SCREEN_HEIGHT
            self.scale_factor = 1.0
        
        # Ekranı oluştur
        if fullscreen:
            self.screen = pygame.display.set_mode((screen_width, screen_height), 
                                                pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((screen_width, screen_height))
        
        pygame.display.set_caption("Flappy Bird Klonu")
        self.clock = pygame.time.Clock()
        
        # Fontları yükle
        self.score_font = pygame.font.Font(None, SCORE_FONT_SIZE)
        self.menu_title_font = pygame.font.Font(None, MENU_TITLE_SIZE)
        self.menu_text_font = pygame.font.Font(None, MENU_TEXT_SIZE)
        
        # Oyun nesnelerini oluştur
        self.bird = Bird(BIRD_START_X, BIRD_START_Y)
        self.pipe_manager = PipeManager()
        self.obstacle_manager = ObstacleManager()
        self.ground = Ground()
        self.background = Background()
        self.sound_manager = SoundManager()
        
        # Oyun durumu
        self.state = GAME_STATES['MENU']
        self.score = 0
        self.high_score = self._load_high_score()
        self.running = True
    
    def _load_high_score(self) -> int:
        """Yüksek skoru yükler"""
        try:
            if os.path.exists(HIGHSCORE_FILE):
                with open(HIGHSCORE_FILE, 'r') as f:
                    data = json.load(f)
                    return data.get('high_score', 0)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
        return 0
    
    def _save_high_score(self):
        """Yüksek skoru kaydeder"""
        try:
            with open(HIGHSCORE_FILE, 'w') as f:
                json.dump({'high_score': self.high_score}, f)
        except IOError:
            pass
    
    def handle_events(self):
        """Olayları işler"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                elif event.key == pygame.K_SPACE:
                    self._handle_flap()
                
                elif event.key == pygame.K_p:
                    self._handle_pause()
                
                elif event.key == pygame.K_r and self.state == GAME_STATES['GAME_OVER']:
                    self._restart_game()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Sol mouse tuşu
                    self._handle_flap()
    
    def _handle_flap(self):
        """Zıplama işlemini yönetir"""
        if self.state == GAME_STATES['MENU']:
            self.state = GAME_STATES['PLAYING']
            self.bird.flap()
            self.sound_manager.play('flap_sound')
        
        elif self.state == GAME_STATES['PLAYING']:
            self.bird.flap()
            self.sound_manager.play('flap_sound')
        
        elif self.state == GAME_STATES['GAME_OVER']:
            self._restart_game()
    
    def _handle_pause(self):
        """Duraklama işlemini yönetir"""
        if self.state == GAME_STATES['PLAYING']:
            self.state = GAME_STATES['PAUSED']
        elif self.state == GAME_STATES['PAUSED']:
            self.state = GAME_STATES['PLAYING']
    
    def _restart_game(self):
        """Oyunu yeniden başlatır"""
        self.bird = Bird(BIRD_START_X, BIRD_START_Y)
        self.pipe_manager.reset()
        self.obstacle_manager.reset()
        self.score = 0
        self.state = GAME_STATES['PLAYING']
    
    def update(self):
        """Oyun mantığını günceller"""
        if self.state == GAME_STATES['PLAYING']:
            # Kuşu güncelle
            self.bird.update()
            
            # Boruları güncelle ve skor kontrolü
            score_increase = self.pipe_manager.check_score(self.bird.get_rect())
            if score_increase > 0:
                self.score += score_increase
                self.sound_manager.play('score_sound')
                
                # Yüksek skor kontrolü
                if self.score > self.high_score:
                    self.high_score = self.score
                    self._save_high_score()
            
            self.pipe_manager.update()
            
            # Engelleri güncelle
            self.obstacle_manager.update()
            
            # Zemini güncelle
            self.ground.update()
            
            # Çarpışma kontrolü
            bird_rect = self.bird.get_rect()
            
            # Zemin çarpışması
            if bird_rect.colliderect(self.ground.get_rect()):
                self._game_over()
            
            # Tavan çarpışması
            if bird_rect.y < 0:
                self._game_over()
            
            # Boru çarpışması
            if self.pipe_manager.check_collisions(bird_rect):
                self._game_over_with_crash()
            
            # Engel çarpışması
            if self.obstacle_manager.check_collisions(bird_rect):
                self._game_over_with_crash()
    
    def _game_over(self):
        """Oyun bitişini yönetir"""
        self.state = GAME_STATES['GAME_OVER']
        self.sound_manager.play('hit_sound')
    
    def _game_over_with_crash(self):
        """Engel çarpışması ile oyun bitişini yönetir"""
        self.state = GAME_STATES['GAME_OVER']
        self.sound_manager.play('crash_sound')
    
    def draw(self):
        """Ekrana çizim yapar"""
        if self.scale_factor > 1.0:
            # Büyük ekran için: önce normal boyutta bir yüzey oluştur
            temp_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            
            # Arkaplanı çiz
            self.background.draw(temp_surface)
            
            if self.state != GAME_STATES['MENU']:
                # Oyun nesnelerini çiz
                self.pipe_manager.draw(temp_surface)
                self.obstacle_manager.draw(temp_surface)
                self.ground.draw(temp_surface)
                self.bird.draw(temp_surface)
                
                # Skoru çiz
                self._draw_score_scaled(temp_surface)
            
            # Durum bazlı çizimler
            if self.state == GAME_STATES['MENU']:
                self._draw_menu_scaled(temp_surface)
            elif self.state == GAME_STATES['PAUSED']:
                self._draw_pause_screen_scaled(temp_surface)
            elif self.state == GAME_STATES['GAME_OVER']:
                self._draw_game_over_screen_scaled(temp_surface)
            
            # Yüzeyi ölçeklendir ve ana ekrana çiz
            scaled_surface = pygame.transform.scale(temp_surface, 
                                                   (int(SCREEN_WIDTH * self.scale_factor), 
                                                    int(SCREEN_HEIGHT * self.scale_factor)))
            self.screen.blit(scaled_surface, (0, 0))
        else:
            # Normal boyut için
            # Arkaplanı çiz
            self.background.draw(self.screen)
            
            if self.state != GAME_STATES['MENU']:
                # Oyun nesnelerini çiz
                self.pipe_manager.draw(self.screen)
                self.obstacle_manager.draw(self.screen)
                self.ground.draw(self.screen)
                self.bird.draw(self.screen)
                
                # Skoru çiz
                self._draw_score()
            
            # Durum bazlı çizimler
            if self.state == GAME_STATES['MENU']:
                self._draw_menu()
            elif self.state == GAME_STATES['PAUSED']:
                self._draw_pause_screen()
            elif self.state == GAME_STATES['GAME_OVER']:
                self._draw_game_over_screen()
        
        pygame.display.flip()
    
    def _draw_score(self):
        """Skoru çizer"""
        score_text = self.score_font.render(str(self.score), True, SCORE_COLOR)
        score_rect = score_text.get_rect(center=SCORE_POSITION)
        self.screen.blit(score_text, score_rect)
    
    def _draw_menu(self):
        """Ana menüyü çizer"""
        # Başlık
        title_text = self.menu_title_font.render("FLAPPY BIRD", True, MENU_TITLE_COLOR)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
        self.screen.blit(title_text, title_rect)
        
        # Yüksek skor
        high_score_text = self.menu_text_font.render(f"En Yüksek Skor: {self.high_score}", 
                                                   True, MENU_TEXT_COLOR)
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(high_score_text, high_score_rect)
        
        # Başlama talimatı
        start_text = self.menu_text_font.render("SPACE veya Mouse ile Başla", 
                                              True, MENU_TEXT_COLOR)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(start_text, start_rect)
    
    def _draw_pause_screen(self):
        """Duraklama ekranını çizer"""
        # Yarı saydam overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(COLORS['BLACK'])
        self.screen.blit(overlay, (0, 0))
        
        # Duraklama metni
        pause_text = self.menu_title_font.render("DURAKLATILDI", True, COLORS['WHITE'])
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(pause_text, pause_rect)
        
        # Devam etme talimatı
        continue_text = self.menu_text_font.render("P ile Devam Et", True, COLORS['WHITE'])
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(continue_text, continue_rect)
    
    def _draw_score_scaled(self, surface: pygame.Surface):
        """Büyük ekran için skoru çizer"""
        score_text = self.score_font.render(str(self.score), True, SCORE_COLOR)
        score_rect = score_text.get_rect(center=SCORE_POSITION)
        surface.blit(score_text, score_rect)
    
    def _draw_menu_scaled(self, surface: pygame.Surface):
        """Büyük ekran için ana menüyü çizer"""
        # Başlık
        title_text = self.menu_title_font.render("FLAPPY BIRD", True, MENU_TITLE_COLOR)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
        surface.blit(title_text, title_rect)
        
        # Yüksek skor
        high_score_text = self.menu_text_font.render(f"En Yüksek Skor: {self.high_score}", 
                                                   True, MENU_TEXT_COLOR)
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        surface.blit(high_score_text, high_score_rect)
        
        # Başlama talimatı
        start_text = self.menu_text_font.render("SPACE veya Mouse ile Başla", 
                                              True, MENU_TEXT_COLOR)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        surface.blit(start_text, start_rect)
    
    def _draw_pause_screen_scaled(self, surface: pygame.Surface):
        """Büyük ekran için duraklama ekranını çizer"""
        # Yarı saydam overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(COLORS['BLACK'])
        surface.blit(overlay, (0, 0))
        
        # Duraklama metni
        pause_text = self.menu_title_font.render("DURAKLATILDI", True, COLORS['WHITE'])
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        surface.blit(pause_text, pause_rect)
        
        # Devam etme talimatı
        continue_text = self.menu_text_font.render("P ile Devam Et", True, COLORS['WHITE'])
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        surface.blit(continue_text, continue_rect)
    
    def _draw_game_over_screen_scaled(self, surface: pygame.Surface):
        """Büyük ekran için oyun bitişi ekranını çizer"""
        # Yarı saydam overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(COLORS['BLACK'])
        surface.blit(overlay, (0, 0))
        
        # Oyun bitti metni
        game_over_text = self.menu_title_font.render("OYUN BİTTİ", True, COLORS['RED'])
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        surface.blit(game_over_text, game_over_rect)
        
        # Skor
        score_text = self.menu_text_font.render(f"Skor: {self.score}", True, COLORS['WHITE'])
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        surface.blit(score_text, score_rect)
        
        # Yüksek skor
        high_score_text = self.menu_text_font.render(f"En Yüksek: {self.high_score}", True, COLORS['YELLOW'])
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30))
        surface.blit(high_score_text, high_score_rect)
        
        # Yeniden başlama talimatı
        restart_text = self.menu_text_font.render("R ile Yeniden Başla", True, COLORS['WHITE'])
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 80))
        surface.blit(restart_text, restart_rect)
    
    def _draw_game_over_screen(self):
        """Oyun bitişi ekranını çizer"""
        # Yarı saydam overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(COLORS['BLACK'])
        self.screen.blit(overlay, (0, 0))
        
        # Oyun bitti metni
        game_over_text = self.menu_title_font.render("OYUN BİTTİ", True, COLORS['RED'])
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Skor
        final_score_text = self.menu_text_font.render(f"Skor: {self.score}", True, COLORS['WHITE'])
        final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(final_score_text, final_score_rect)
        
        # Yüksek skor
        high_score_text = self.menu_text_font.render(f"En Yüksek: {self.high_score}", 
                                                   True, COLORS['WHITE'])
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30))
        self.screen.blit(high_score_text, high_score_rect)
        
        # Yeniden başlama talimatı
        restart_text = self.menu_text_font.render("R veya SPACE ile Tekrar Oyna", 
                                                True, COLORS['WHITE'])
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 70))
        self.screen.blit(restart_text, restart_rect)
    
    def run(self):
        """Ana oyun döngüsü"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()