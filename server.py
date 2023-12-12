import pygame
from pygame.locals import *

from player import *
from global_variables import *
from game_manager import *

import errno
import select
import socket
import json
import time

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
        self.start = Start(self.displaySurface)


        # Perguntar pro servidor qual coordenadas ainda nao foram criadas antes disso
        self.currentLevelIdx = 0
        self.currentLevelIdy = 0
        
        self.level = Level(self.displaySurface, self.currentLevelIdx, self.currentLevelIdy)
        self.known_levels = [self.level]

        self.states = {'start':self.start, 'level':self.level}

        for i in range(11):
            for j in range(11):
                self.known_levels.append(Level(self.displaySurface, i - 10, j - 10))

        # Create Player
        self.P1 = Player() 

        # Add sprites
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.P1)

    def levelChange(self):
        levelExistsInServer = False # For now, client creates every level
        levelExistsInClient = [level for level in self.known_levels if level.get_coordinates() == (self.currentLevelIdx, self.currentLevelIdy)]
        if levelExistsInClient != []:
            self.states['level'] = levelExistsInClient[0]
        else:
            self.states['level'] = Level(self.displaySurface, self.currentLevelIdx, self.currentLevelIdy)
            self.known_levels.append(self.states['level'])

    def run(self):
        HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
        PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            # Comunicacao estabelecida
            self.P2 = Player()
            self.all_sprites.add(self.P2)
            with conn:
                conn.sendall(bytes(str([str((e.color, e.get_coordinates())) for e in self.known_levels]), encoding='utf-8'))
                print(f"Connected by {addr}")
                while True:

                    #break
                    ## Inicio do jogo de fato

                    for event in pygame.event.get():
                        if event.type == QUIT:
                            print('Fechando o jogo')
                            pygame.quit()
                            break
                    
                    #self.displaySurface.fill((0, 0, 0)) # Black background
                    self.states[self.gameStateManager.get_state()].run()

                    for entity in self.all_sprites: # Draw all sprites
                        self.displaySurface.blit(entity.surf, entity.rect)


                    self.P1.move()

                    # The game loop has the responsibility to garantee the player is in the screen
                    p1_pos = self.P1.get_pos()

                    #For every one of these if`s, ask the server if the level already exists
                    if p1_pos.x > WIDTH:
                        self.P1.set_pos(vec(0, p1_pos.y))

                        self.currentLevelIdx += 1

                        self.levelChange()
                    elif p1_pos.x < 0:
                        self.P1.set_pos(vec(WIDTH, p1_pos.y))
                        
                        self.currentLevelIdx -= 1

                        self.levelChange()
                    elif p1_pos.y < 0:
                        self.P1.set_pos(vec(p1_pos.x, HEIGHT))

                        self.currentLevelIdy += 1

                        self.levelChange()
                    elif p1_pos.y > HEIGHT:
                        self.P1.set_pos(vec(p1_pos.x, 0))

                        self.currentLevelIdy -= 1

                        self.levelChange()

                    self.P1.set_rect_midbottom(self.P1.get_pos()) # Updates the rect object of Player with the new position

                    # Recebe posicao global do outro jogador
                    p2_global = list(conn.recv(1024))
                    p2_global = [x - 100 for x in p2_global]
                    print(p2_global)
                    if not p2_global:
                        print('Erro na comunicacao entre jogadores')
                        pygame.quit()
                        break

                    time.sleep(0.003)

                    # Envia posicao global ao outro jogador
                    data = bytearray([self.currentLevelIdx + 100, self.currentLevelIdy + 100])
                    conn.sendall(data)

                    time.sleep(0.003)

                    # Envia posicao local ao outro jogador
                    data = f"{p1_pos.x},{p1_pos.y}"
                    pos = bytearray(data, encoding='utf-8')
                    conn.sendall(pos)
                    time.sleep(0.003)

                    # Recebe posicao local do outro jogador
                    data = [float(x) for x in tuple(conn.recv(1024).decode('utf-8').split(','))]
                    if not data:
                        print('Erro na comunicacao entre jogadores')
                        pygame.quit()
                        break
                    p2_pos = vec(data)
                    time.sleep(0.003)

                    # Se o outro jogador esta na mesma posicao global, desenhar ele
                    if p2_global == [self.currentLevelIdx, self.currentLevelIdy]:
                        print('True')
                        self.all_sprites.add(self.P2)
                        self.P2.set_pos(p2_pos)
                        self.P2.set_rect_midbottom(p2_pos)
                    else:
                        self.all_sprites.remove(self.P2)
                    

                    pygame.display.update()
                    self.FramePerSec.tick(FPS)
                print('Fechando o jogo')
                pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
