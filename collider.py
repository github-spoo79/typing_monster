import pygame

class Collider():
    def __init__(self, x, y, width, height, padding_x=0, padding_y=0):
        self.padding_x = padding_x
        self.padding_y = padding_y
        self.rect = pygame.Rect(x + padding_x, y + padding_y, width, height)
        
    def update(self, x, y):
        self.rect.topleft = (x + self.padding_x, y + self.padding_y)        

    def draw(self, surface, color=(255, 0, 0)):
        pygame.draw.rect(surface, color, self.rect, 2)
        
    def clear(self):
        self.rect.x = self.rect.x
        self.rect.y = self.rect.y
        self.rect.width = 0
        self.rect.height = 0
        self.padding_x = 0
        self.padding_y = 0
        