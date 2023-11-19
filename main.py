import pygame
from pygame.locals import *
from player import *
from global_variables import *
from game_manager import *

vec = pygame.math.Vector2

class Game:
    def __init__(self):
        # Pre-game settings
        pygame.init()

        self.FramePerSec = pygame.time.Clock()

        self.displaySurface = pygame.display.set_mode((WIDTH, HEIGHT)) # Create window
        pygame.display.set_caption("Game")

        # Game Manager
        self.gameStateManager = GameStateManager('level')
        self.start = Start(self.displaySurface, self.gameStateManager)
        self.level = Level(self.displaySurface, self.gameStateManager)
        self.states = {'start':self.start, 'level':self.level}

        # Create Player
        self.P1 = Player() 

        # Add sprites
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.P1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
            
            #self.displaySurface.fill((0, 0, 0)) # Black background
            self.states[self.gameStateManager.get_state()].run()

            for entity in self.all_sprites: # Draw all sprites
                self.displaySurface.blit(entity.surf, entity.rect)


            self.P1.move()

            # The game loop has the responsibility to garantee the player is in the screen

            p1_pos = self.P1.get_pos()

            if p1_pos.x > WIDTH:
                self.P1.set_pos(vec(0, p1_pos.y))
                self.level.change_level()
            elif p1_pos.x < 0:
                self.P1.set_pos(vec(WIDTH, p1_pos.y))
                self.level.change_level()
            elif p1_pos.y < 0:
                self.P1.set_pos(vec(p1_pos.x, HEIGHT))
                self.level.change_level()
            elif p1_pos.y > HEIGHT:
                self.P1.set_pos(vec(p1_pos.x, 0))
                self.level.change_level()

            self.P1.set_rect_midbottom(self.P1.get_pos()) # Updates the rect object of Player with the new position



            pygame.display.update()
            self.FramePerSec.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
