# Documentacao

Esta pasta concentra documentos de planejamento, organizacao e apoio ao desenvolvimento do jogo **Cobralia: Snake Ascension.**

## Sobre o Projeto

Cobralia: Snake Ascension e uma releitura moderna do classico *Snake Game*, desenvolvida em Python utilizando a biblioteca Pygame.

O jogador controla uma cobra que deve coletar macas para crescer, cumprir objetivos de cada fase e avancar por uma campanha composta por diferentes desafios, inimigos e mecanicas especiais.

Entre os principais recursos previstos estao:

* Sistema de fases com metas progressivas;
* Paredes fixas e paredes moveis;
* Habilidade de **Dash**, consumindo recursos do jogador;
* Itens especiais com efeitos temporarios;
* Inimigos com inteligencia artificial;
* Batalha contra um Chefao Final com pontos fracos e padroes de ataque.

---

## Arquivos

* `proposta.MD`

  Documento contendo a proposta inicial do jogo, escopo, mecanicas previstas, organizacao do projeto e desafios esperados.

---

## Estrutura Planejada do Projeto

```text
Projeto/
│
├── main.py
├── config.py
├── requirements.txt
│
├── assets/
│   ├── images/
│   ├── sounds/
│   └── fonts/
│
├── core/
│   ├── game.py
│   ├── state_manager.py
│   └── level_manager.py
│
├── entities/
│   ├── snake.py
│   ├── items.py
│   ├── obstacles.py
│   ├── predator.py
│   └── boss.py
│
├── systems/
│   ├── collision.py
│   ├── pathfinding.py
│   └── effects.py
│
├── ui/
│   ├── hud.py
│   └── menus.py
│
└── docs/
    ├── proposta.MD
    └── README.md
```

---

## Escopo Minimo da Entrega

A versao minima do jogo devera possuir:

* Cobra funcional com crescimento ao coletar macas;
* Colisao com paredes e com o proprio corpo;
* Pelo menos **3 fases jogaveis**;
* Paredes moveis;
* Sistema de transicao entre fases;
* Implementacao de no minimo **2 itens especiais**, como:

  * Pimenta (aumento de velocidade);
  * Tesoura (reduz a cauda da cobra).

---

## Melhorias Planejadas

Funcionalidades previstas para expansao do projeto:

* Movimentacao em 360° baseada em vetores;
* Sistema de vida para o jogador;
* Efeitos visuais e particulas;
* Trilha sonora dinamica;
* Modo Fantasma;
* Inversao de controles;
* Inteligencia Artificial avancada para o Chefao Final;
* Sistema de pontuacao e ranking local.

---

## Sugestoes de Uso

* Registrar decisoes importantes do grupo;
* Documentar alteracoes de mecanicas e regras;
* Registrar mudancas de escopo;
* Manter historico de ideias e melhorias futuras;
* Anotar problemas encontrados e respectivas solucoes durante o desenvolvimento.
