import random
import pygame
from config import Config as cfg
from util import Util as util

class Background():
    def __init__(self):
        self.noline_maptile = util.render_sheet("aspalt.png", 100, 100, 9, 1)
        self.fence_top = pygame.image.load(cfg.GAME_IMG_DIR + "fence_top.png")
        self.fence_middle = pygame.image.load(cfg.GAME_IMG_DIR + "fence_middle.png")
        self.matrix = [[random.randint(0, 6) for _ in range(9)] for _ in range(9)]
        
    def draw_tile(self, surface):
         for y in range(0, 9):
             for x in range(0, 9):
                 tile = self.matrix[y][x]
                 surface.blit(self.noline_maptile[tile], (x * 100, y * 100))
                 
    def draw_fence(self, surface):
        for x in range(0, 9):
            surface.blit(self.fence_top, (x * 100, 450))
            