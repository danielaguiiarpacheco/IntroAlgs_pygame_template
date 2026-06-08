import random
from config import LARGURA, ALTURA, TAMANHO

class Maca:
    def __init__(self):
        self.nova()

    def nova(self):
        self.pos = [
            random.randrange(0, LARGURA, TAMANHO),
            random.randrange(0, ALTURA, TAMANHO)
        ]