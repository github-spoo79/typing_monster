import pygame
import time
import random
import math
from config import Config as cfg
from collider import Collider

class Player(pygame.sprite.Sprite):
    def __init__(self, main, pos, idle, left_attack, right_attack, death):
        super().__init__()
        self.id = "barrier"
        self.main = main
        self.images = []
        self.idle_images = idle
        self.death_images = death
        #print(len(self.death_images))
        self.attack_images = {"LEFT": left_attack, "RIGHT": right_attack}
        
        self.images = self.idle_images
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        
        self.animation_index = 0
        self.animation_interval_count = 0
        self.animation_interval_increment = 1
        
        self.player_status = cfg.IDLE
        self.animation_intervals = {"IDLE": 15, "ATTACK": 8, "DEATH": 15}
        self.animation_interval = self.animation_intervals["IDLE"]
        self.collider = Collider(self.rect.x
                               , self.rect.y
                               , self.rect.width
                               , self.rect.height / 2
                               , 0
                               , self.rect.height * (1/2))
        self.live = True
        self.death_time = 0
       
    def update(self):   
        loop = True
        
        if self.live:
            if self.player_status == cfg.ATTACK:
                self.idle()
        else:
            loop = False

        self.animation(loop)            
            
    def attack(self, direction):
        if self.player_status != cfg.ATTACK:
            self.player_status = cfg.ATTACK
            self.images = self.attack_images.get(direction, self.attack_images["RIGHT"])
            self.animation_interval = self.animation_intervals["ATTACK"]
            self.animation_index = 0
    
    def animation(self, loop=True):
        self.animation_interval_count += 1
        if loop:
            if self.animation_interval_count >= self.animation_interval:
                self.animation_interval_count = 0
                self.animation_index = (self.animation_index + 1) % len(self.images)
                self.image = self.images[self.animation_index]
        else:
            if self.animation_index >= len(self.images) - 1:
                self.image = self.images[len(self.images) - 1]
            else:
                if self.animation_interval_count >= self.animation_interval:
                    self.animation_interval_count = 0
                    self.animation_index += 1
                    self.image = self.images[self.animation_index]
    
    def idle(self):
        if self.animation_index == 0 and self.animation_interval_count == 0:
            self.player_status = cfg.IDLE
            self.images = self.idle_images
            self.animation_interval = self.animation_intervals["IDLE"]
            self.animation_index = 0
            
    def death(self):
        self.player_status = cfg.DEATH
        self.images = self.death_images
        self.animation_interval = self.animation_intervals["DEATH"]
        self.animation_index = 0
        self.main.game_status = cfg.GAME_OVER
        self.main.resources.player_scream.play()
            
    def damage(self, power):
        if self.live:
            self.live = False
            self.death_time = time.time()
            self.death()
        
        return True            

class PlayerText(pygame.sprite.Sprite):
    def __init__(self, main, pos):
        super().__init__()
        self.main = main
        self.font = pygame.font.Font(cfg.GAME_FONT_DIR + "HBIOS-SYS.ttf", 24)
        self.display_text = ""
        self.edit_pos = 0
        self.text = ""
        self.text_editing = ""
        self.text_editing_pos = 0        
        self.font_color = cfg.BLACK
        self.bg_color = cfg.WHITE
        self.pos = pos
        self.padding = 5
        text_surface = self.font.render(self.display_text, True, self.font_color)
        padded_width = text_surface.get_width() + 2 * self.padding
        padded_height = text_surface.get_height() + 2 * self.padding
        self.image = pygame.Surface((padded_width, padded_height))
        self.image.fill(self.bg_color)
        self.image.blit(text_surface, (self.padding, self.padding))        
        self.rect = self.image.get_rect(center=pos)
        self.keydown_cnt = 0
        self.keydown_start_time = 0 
        self.typing_speed = 0
        #self.image = self.font.render(self.display_text, True, self.font_color, self.bg_color)
        #self.rect = self.image.get_rect(center=pos)
        
    def update_text(self):
        text_surface = self.font.render(self.display_text, True, self.font_color)
        padded_width = text_surface.get_width() + 2 * self.padding
        padded_height = text_surface.get_height() + 2 * self.padding
        self.image = pygame.Surface((padded_width, padded_height))
        self.image.fill(self.bg_color)
        self.image.blit(text_surface, (self.padding, self.padding))        
        self.rect = self.image.get_rect(center=self.pos)
    
    def key_event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:self.edit_pos-1] + self.text[self.edit_pos:]
                self.edit_pos = max(0, self.edit_pos-1)                
            elif event.key == pygame.K_RETURN:
                self.text = ""
                self.text_editing = ""
                self.text_editing_pos = 0
                self.edit_pos = 0

                if self.keydown_start_time is not None:
                    elapsed_time = (pygame.time.get_ticks() - self.keydown_start_time) / 1000                
                    typing_speed = round((self.keydown_cnt * 60) / elapsed_time, 2)
                    self.main.check_hit(self.display_text, typing_speed)
                    self.keydown_start_time = None
                    self.keydown_cnt = 0
                
        elif event.type == pygame.TEXTEDITING:            
            if self.keydown_start_time is None:
                self.keydown_start_time = pygame.time.get_ticks()

            self.text_editing = event.text
            self.text_editing_pos = event.start
            
            if event.text != "":
                self.keydown_cnt += 1
            
        elif event.type == pygame.TEXTINPUT:
            if self.keydown_start_time is None:
                self.keydown_start_time = pygame.time.get_ticks()

            if len(self.text + event.text) <= cfg.MAX_LENGTH:
                self.text_editing = ""
                self.text = self.text[:self.edit_pos] + event.text + self.text[self.edit_pos:]
                self.edit_pos = min(self.edit_pos + len(event.text), len(self.text + self.text_editing))
        
        self.display_text = self.text + self.text_editing
        self.update_text()
        

class Cartridge(pygame.sprite.Sprite):
    def __init__(self, x, y, delay_time=0, dir=1):
        super().__init__()
        self.delay_time_ms = delay_time * 1000  # 밀리초 단위로 변환
        self.spawn_time = pygame.time.get_ticks()
        self.visible = False

        self.image = pygame.Surface((cfg.CARTRIDGE_RADIUS * 2, cfg.CARTRIDGE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, cfg.CARTRIDGE_COLOR, (cfg.CARTRIDGE_RADIUS, cfg.CARTRIDGE_RADIUS), cfg.CARTRIDGE_RADIUS)
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(self.rect.center)        
        angle = random.uniform(-math.pi / 6, -math.pi / 8) * dir
        speed = random.uniform(5, 7) * dir
        self.velocity = pygame.math.Vector2(math.cos(angle) * speed,
                                            math.sin(angle) * speed)
        self.life = 60
        self.visible = False

    def update(self):
        current_time = pygame.time.get_ticks()
        if not self.visible and (current_time - self.spawn_time >= self.delay_time_ms):
            self.visible = True

        if self.visible:
            self.velocity.y += cfg.GRAVITY
            self.pos += self.velocity
            self.rect.center = (int(self.pos.x), int(self.pos.y))
            self.life -= 1
            if self.life <= 0:
                self.kill()

    def draw(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect)