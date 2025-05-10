import pygame
from config import Config as cfg
from collider import Collider

class Barrier(pygame.sprite.Sprite):
    def __init__(self, main, fence, pos, crash):
        super().__init__()
        self.id = "barrier"
        self.main = main
        self.images = fence
        self.idx = 6
        self.image = self.images[6]
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)        
        self.collider = Collider(self.rect.x
                               , self.rect.y
                               , self.rect.width
                               , self.rect.height / 10
                               , 0
                               , self.rect.height * (9/10))
        self.damaged = 0
        self.sound_delay_time = 1000
        self.last_sound_time = pygame.time.get_ticks()
        self.crash = crash
    
    def update(self):
        if self.damaged > len(self.images):
            self.collider.clear()
        else:
            self.image = self.images[int(self.damaged)]            
            #self.collider.draw(self.main.screen)
            
    def play_crash_sound(self):
        if pygame.time.get_ticks() - self.last_sound_time >= self.sound_delay_time:
            self.crash.play()
            self.last_sound_time = pygame.time.get_ticks()
        
    def damage(self, power):
        self.damaged += power    
        self.play_crash_sound()
        if self.damaged >= len(self.images):
            return False
        else:
            return True