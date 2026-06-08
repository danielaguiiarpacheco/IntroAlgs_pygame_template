import pygame

from docs.cobrinha.config import *
from docs.cobrinha.jogo import Cobra
from docs.cobrinha.maca import Maca


pygame.init()

tela = pygame.display.set_mode(
    (LARGURA, ALTURA)
)

pygame.display.set_caption(TITULO)

clock = pygame.time.Clock()
fonte = pygame.font.SysFont(None, 36)

cobra = Cobra()
maca = Maca()

pontos = 0
rodando = True

while rodando:

    clock.tick(FPS)

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:
            cobra.mudar_direcao(evento.key)

    cobra.mover()

    if cobra.corpo[0] == maca.posicao:
        pontos += 1
        cobra.crescer()
        maca.reposicionar()

    x, y = cobra.corpo[0]

    if (
        x < 0
        or x >= LARGURA
        or y < 0
        or y >= ALTURA
    ):
        rodando = False

    tela.fill(PRETO)

    for parte in cobra.corpo:
        pygame.draw.rect(
            tela,
            VERDE,
            (parte[0], parte[1], TAMANHO, TAMANHO)
        )

    pygame.draw.rect(
        tela,
        VERMELHO,
        (
            maca.posicao[0],
            maca.posicao[1],
            TAMANHO,
            TAMANHO
        )
    )

    texto = fonte.render(
        f"Pontos: {pontos}",
        True,
        BRANCO
    )

    tela.blit(texto, (10, 10))

    pygame.display.flip()

pygame.quit()