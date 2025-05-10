import random
import pygame
from util import Util as util

class Ability:
    def __init__(self, main):
        self.main = main
        self.action_start_time = None
        self.action = random.choice([self.shuffle_text, self.hide_text])
        
    def shuffle_text(self):
        new_text = list(self.main.display_text) 
        random.shuffle(new_text)
        self.main.text = ''.join(new_text)
        self.main.display_text = ''.join(new_text)
        self.main.render_text()
        return True
    
    def hide_text(self):
        display_text = util.mask_text(self.main.display_text)
        self.main.display_text = display_text
        self.main.render_text()        
        self.action_start_time = pygame.time.get_ticks()
        return True
    
    def check_next(self):
        if self.action_start_time and pygame.time.get_ticks() - self.action_start_time > 2000:
            self.reveal_text()
            self.action_start_time = None
        
    def reveal_text(self):
        display_text = self.main.text
        self.main.display_text = display_text
        self.main.render_text()
        self.main.align_text()
        return True
