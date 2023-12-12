import pygame
from pygame.locals import *
from global_variables import *

vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.activate()

    def activate(self):
            self.surf = pygame.Surface((30, 30))
            self.surf.fill((255, 255, 255))
            self.rect = self.surf.get_rect(center = (10, 420))

            self.pos = vec((30, 385))
            self.vel = vec(0, 0)

            self.pos_in_matrix = (0, 0)


    def move(self):
        self.vel = vec(0, 0)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_a]:
            self.vel.x = -VEL
        if pressed_keys[K_d]:
            self.vel.x = VEL
        if pressed_keys[K_w]:
            self.vel.y = -VEL
        if pressed_keys[K_s]:
            self.vel.y = VEL
        

        self.pos += self.vel

    def get_pos(self):
        return self.pos

    def set_pos(self, pos):
        self.pos = pos

    def get_rect(self):
        return self.rect

    def set_rect_midbottom(self, pos):
        self.rect.midbottom = pos

    def get_pos_in_matrix(self):
        return self.pos_in_matrix

    def set_pos_in_matrix(self, pos):
        self.pos_in_matrix = pos_in_matrix
