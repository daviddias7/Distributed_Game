import pygame
from global_variables import *

vec = pygame.math.Vector2


class Object(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center = (240, 240))
