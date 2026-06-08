import pygame
from cobra import Cobra
from maca import Maca
from config import *

pygame.init()

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Cobrinha")

clock = pygame.time.Clock()

cobra = Cobra()
maca = Maca()

pontos = 0
fonte = pygame.font.SysFont(None, 36)

rodando = True
game_over = False

while rodando:
    clock.tick(FPS)
    tela.fill(CINZA)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:
            if not game_over:
                cobra.mudar_direcao(evento.key)

    if not game_over:
        cobra.mover()

        # colisão com maçã (CORRETO)
        if cobra.corpo[0][0] == maca.pos[0] and cobra.corpo[0][1] == maca.pos[1]:
            cobra.crescer()
            pontos += 1
            maca.nova()

        # colisão com parede
        x, y = cobra.corpo[0]
        if x < 0 or x >= LARGURA or y < 0 or y >= ALTURA:
            game_over = True

    # desenhar maçã
    pygame.draw.rect(
        tela,
        VERMELHO,
        (maca.pos[0], maca.pos[1], TAMANHO, TAMANHO)
    )

    # desenhar cobra
    for parte in cobra.corpo:
        pygame.draw.rect(
            tela,
            VERDE,
            (parte[0], parte[1], TAMANHO, TAMANHO)
        )

    # placar
    texto = fonte.render(f"Pontos: {pontos}", True, PRETO)
    tela.blit(texto, (10, 10))

    # game over
    if game_over:
        texto2 = fonte.render("GAME OVER - pressione R", True, PRETO)
        tela.blit(texto2, (200, 250))

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_r]:
            cobra.reset()
            maca.nova()
            pontos = 0
            game_over = False

    pygame.display.flip()

pygame.quit()