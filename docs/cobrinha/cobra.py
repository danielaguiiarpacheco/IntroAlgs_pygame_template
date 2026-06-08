import pygame
from config import TAMANHO

class Cobra:
    def __init__(self):
        self.reset()

    def reset(self):
        self.corpo = [(100, 100)]
        self.dx = TAMANHO
        self.dy = 0

    def mover(self):
        x, y = self.corpo[0]
        nova_cabeca = (x + self.dx, y + self.dy)

        self.corpo.insert(0, nova_cabeca)
        self.corpo.pop()

    def crescer(self):
        # crescimento simples: adiciona um bloco extra
        self.corpo.append(self.corpo[-1])

    def mudar_direcao(self, tecla):

        if tecla == pygame.K_UP and self.dy == 0:
            self.dx = 0
            self.dy = -TAMANHO

        elif tecla == pygame.K_DOWN and self.dy == 0:
            self.dx = 0
            self.dy = TAMANHO

        elif tecla == pygame.K_LEFT and self.dx == 0:
            self.dx = -TAMANHO
            self.dy = 0

        elif tecla == pygame.K_RIGHT and self.dx == 0:
            self.dx = TAMANHO
            self.dy = 0