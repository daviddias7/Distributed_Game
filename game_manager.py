import pygame
import sys
from pygame.locals import *
import numpy as np

class Level:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

        self.color = list(np.random.choice(range(256), size=3))


    def run(self):
        self.display.fill(self.color)

    def change_level(self):
        self.color = list(np.random.choice(range(256), size=3))


class Start:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def run(self):
        self.display.fill('red')

class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState

    def get_state(self):
        return self.currentState

    def set_state(self, state):
        self.currentState = state
