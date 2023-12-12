import pygame
import sys
from pygame.locals import *
import numpy as np

class Level:
    def __init__(self, display, x, y, color = None):
        self.display = display
        self.x = x
        self.y = y

        if color == None:
            self.color = list(np.random.choice(range(256), size=3))
        else:
            self.color = color


    def run(self):
        self.display.fill(self.color)

    def get_coordinates(self):
        return (self.x, self.y)


class Start:
    def __init__(self, display):
        self.display = display

    def run(self):
        self.display.fill('red')

class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState

    def get_state(self):
        return self.currentState

    def set_state(self, state):
        self.currentState = state
