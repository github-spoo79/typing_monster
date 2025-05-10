import pygame
import random
from config import Config as cfg
from util import Util as util
from collider import Collider
from ability import Ability

class Monster(pygame.sprite.Sprite):
    def __init__(self, uuid, main, pos, walk, die, attack, scream, speed):
        super().__init__()
        self.uuid = uuid
        self.images = []
        self.walk_images = walk
        self.die_images = die
        self.attack_images = attack   
        self.scream = scream     
        self.images = self.walk_images
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        self.speed = pygame.math.Vector2(0, speed)

        self.monster_status = cfg.WALK                
        self.animation_index = 0
        self.animation_interval = 10
        self.animation_interval_count = 0
        self.animation_interval_increment = 1
        
        self.opacity = 255
        self.monster_text = None
        self.collider = Collider(self.rect.x
                                 , self.rect.y + (self.rect.height * (3/4))
                                 , self.rect.width
                                 , self.rect.height / 4
                                 , 0
                                 , self.rect.height * (3/4))
        self.id = "monster"
        self.stop = False
        self.attack_target = None
        self.main = main
        self.target = False
        
    def set_status(self, status):
        if status == "DIE":
            self.monster_status = cfg.DIE
            self.images = self.die_images
            self.speed = pygame.math.Vector2(0, 0)
            self.scream.play()
            self.collider.clear()    

        if self.monster_status != cfg.DIE and self.monster_status != cfg.DISAPPEAR:
            if status == "ATTACK":
                self.monster_status = cfg.ATTACK
                self.images = self.attack_images
                self.speed = pygame.math.Vector2(0, 0)
                
            elif status == "WALK":
                self.monster_status = cfg.WALK
                self.images = self.walk_images
                self.speed = pygame.math.Vector2(0, 0.3)
                
            elif status == "WAIT":
                if self.monster_status not in (cfg.ATTACK, cfg.DIE):
                    self.monster_status = cfg.WAIT
                    self.images = self.walk_images
                    self.speed = pygame.math.Vector2(0, 0)
            
        self.animation_index = 0
        self.animation_interval_count = 0        
        self.image = self.images[self.animation_index]        
    
    def update(self):
        self.move()
        self.animation()
        self.dispose()    

    def move(self):
        self.pos += self.speed
        self.rect.center = self.pos
        self.collider.update(self.rect.x, self.rect.y)
        
        if not(self.target) and self.rect.y >= cfg.FENCE_POSITION_Y:
            self.speed = (pygame.math.Vector2(cfg.START_POS) - pygame.math.Vector2(self.rect.center)).normalize()
            self.target = True
        
    def animation(self):
        self.animation_interval_count += self.animation_interval_increment
        if self.monster_status == cfg.DIE:
            if self.animation_interval_count >= self.animation_interval:
                self.animation_interval_count = 0
                self.animation_index = (self.animation_index + 1) % len(self.images)
                self.image = self.images[self.animation_index]
                if self.animation_index == len(self.images) - 1:
                    self.monster_status = cfg.DISAPPEAR

        elif self.monster_status == cfg.DISAPPEAR:
            self.disappear()
            
        else:
            if self.animation_interval_count >= self.animation_interval:
                self.animation_interval_count = 0
                self.animation_index = (self.animation_index + 1) % len(self.images)
                self.image = self.images[self.animation_index]
                
            if self.monster_status == cfg.ATTACK:
                self.attack()
            
    def disappear(self):
        self.opacity -= 3
        self.image.set_alpha(self.opacity)
        if self.opacity < 0:
            self.kill()
            
    def dispose(self):
        if self.rect.y > cfg.SCREEN_HEIGHT:
            self.kill()        
            
    def attack(self):
        if self.attack_target:
            if not(self.attack_target.damage(0.0167)):
                self.stop = False
                self.set_status("WALK")
            
class MonsterText(pygame.sprite.Sprite):
    def __init__(self, uuid, main, monster, text, probability):
        super().__init__()
        self.uuid = uuid
        self.monster = monster
        self.font = pygame.font.Font(cfg.GAME_FONT_DIR + "HBIOS-SYS.ttf", 24)
        self.text = text
        self.display_text = text
        self.font_color = cfg.BLACK
        self.bg_color = cfg.WHITE
        self.padding = 5
        self.render_text()
        pos = (self.monster.rect.x + self.monster.rect.width / 2, -(self.monster.rect.height/2 + 20))
        self.rect = self.image.get_rect(center=pos)        
        self.pos = pygame.math.Vector2(pos)
        self.speed = pygame.math.Vector2(0, 0.3)
        self.skill = False        
        self.ability = Ability(self)
        self.probability = probability
        
    def update(self):
        self.move()
        self.active_skill()
        self.dispose()
        
    def move(self):
        if not(self.monster.stop):
            self.pos += self.monster.speed
        self.rect.center = self.pos
        
    def render_text(self):
        text_surface = self.font.render(self.display_text, True, self.font_color)
        padded_width = text_surface.get_width() + 2 * self.padding
        padded_height = text_surface.get_height() + 2 * self.padding        
        self.image = pygame.Surface((padded_width, padded_height))
        self.image.fill(self.bg_color)
        self.image.blit(text_surface, (self.padding, self.padding))
        
    def align_text(self):
        self.rect = self.image.get_rect(center=self.pos)
        
    def active_skill(self):
        if self.rect.y > 0:
            if not(self.skill):
                if random.random() < self.probability:
                    self.skill = self.ability.action()                
                    self.rect = self.image.get_rect(center=self.pos)
            else:
                self.ability.check_next()
        
    def destroy(self):
        self.monster.set_status("DIE")
        self.kill()
        
    def dispose(self):
        if self.rect.y > cfg.SCREEN_HEIGHT:
            self.kill()