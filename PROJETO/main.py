# main.py
import pygame
import sys
import random
from config import *
from entities import Snake, Enemy, Boss
from systems import LevelManager, UIManager

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("COBRALIA: SNAKE ASCENSION")
    clock = pygame.time.Clock()
    
    lm = LevelManager()
    ui = UIManager()
    
    # Estados: MENU, PLAY, GAME_OVER, VICTORY
    state = "MENU"
    snake = Snake()
    
    apple = pygame.Vector2(random.randint(5, GRID_W-5), random.randint(5, GRID_H-5))
    powerup = None
    apples_collected = 0
    
    enemy = None
    boss = None

    def load_level(num: int) -> None:
        nonlocal apples_collected, enemy, boss, snake, powerup
        lvl = lm.levels[num]
        apples_collected = 0
        powerup = None
        
        # Mantém score e vidas entre fases, reseta posição
        old_lives, old_score = snake.lives, snake.score
        snake = Snake()
        snake.lives, snake.score = old_lives, old_score
        
        if lvl.get("enemy"): enemy = Enemy((10, 10))
        if lvl.get("boss"): boss = Boss()

    load_level(1)

    while True:
        dt = clock.tick(FPS)
        
        # 1. Processamento de Eventos
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if e.type == pygame.KEYDOWN:
                if state in ["MENU", "GAME_OVER", "VICTORY"] and e.key == pygame.K_RETURN:
                    if state in ["GAME_OVER", "VICTORY"]:
                        lm.current = 1
                        snake = Snake() # Hard reset
                        load_level(1)
                    state = "PLAY"
                    
                if state == "PLAY":
                    if e.key == pygame.K_SPACE: snake.dash()
                    if e.key == pygame.K_ESCAPE: state = "MENU" # Pause simples
                    
                    # Controles (com suporte a inversão de PowerDown)
                    dir_map = {
                        pygame.K_w: (0, -1), pygame.K_s: (0, 1),
                        pygame.K_a: (-1, 0), pygame.K_d: (1, 0)
                    }
                    if e.key in dir_map:
                        new_dir = pygame.Vector2(dir_map[e.key])
                        if 'POISON' in snake.effects: new_dir *= -1
                        # Evita movimento reverso instantâneo
                        if new_dir + snake.direction != pygame.Vector2(0, 0):
                            snake.direction = new_dir

        # 2. Lógica do Jogo
        if state == "PLAY":
            snake.update(dt)
            head = snake.body[0]

            # Coleta de Maçã
            if head == apple:
                snake.grow_pending += 1
                apples_collected += 1
                snake.score += 10
                apple = pygame.Vector2(random.randint(2, GRID_W-2), random.randint(2, GRID_H-2))
                
                # Chance de spawnar PowerUp
                if random.random() > 0.7 and not powerup:
                    p_types = ['PEPPER', 'ICE', 'GHOST', 'SCISSORS', 'POISON']
                    powerup = {"pos": pygame.Vector2(random.randint(2, GRID_W-2), random.randint(2, GRID_H-2)), 
                               "type": random.choice(p_types)}

                # Progressão de Fase
                if apples_collected >= lm.levels[lm.current]["goal"]:
                    lm.current += 1
                    if lm.current > 4: state = "VICTORY"
                    else: load_level(lm.current)

            # Coleta de PowerUp
            if powerup and head == powerup["pos"]:
                snake.apply_powerup(powerup["type"])
                powerup = None

            # Inimigo
            if enemy:
                enemy.update(dt, head)
                if head == enemy.pos and 'GHOST' not in snake.effects:
                    snake.lives -= 1
                    enemy.pos = pygame.Vector2(10, 10) # Reposiciona

            # Chefão
            if boss:
                boss.update(dt)
                # Colisão com Pontos Fracos
                for wp in boss.weak_points[:]:
                    if head == wp:
                        boss.weak_points.remove(wp)
                        boss.hp -= 1
                        snake.score += 500
                        # Muda padrão de velocidade após hit
                        boss.timer -= 100 
                
                # Colisão com Projéteis do Chefe
                for p in boss.projectiles:
                    if int(p.x) == int(head.x) and int(p.y) == int(head.y) and 'GHOST' not in snake.effects:
                        snake.lives -= 1
                        boss.projectiles.remove(p)

                if boss.hp <= 0: state = "VICTORY"

            # Colisão consigo mesma
            if head in snake.body[1:] and 'GHOST' not in snake.effects:
                snake.lives -= 1
                snake.body = snake.body[:snake.body.index(head)] # Corta a cobra

            # Colisão com Paredes (Limites da Grade)
            if head.x < 0 or head.x >= GRID_W or head.y < 0 or head.y >= GRID_H:
                if 'GHOST' not in snake.effects:
                    snake.lives -= 1
                    # Reposiciona cabeça p/ evitar morte infinita
                    snake.body[0] = pygame.Vector2(GRID_W//2, GRID_H//2) 
                else:
                    snake.body[0].x = head.x % GRID_W
                    snake.body[0].y = head.y % GRID_H

            if snake.lives <= 0:
                state = "GAME_OVER"

        # 3. Renderização
        screen.fill(BG_COLOR)
        
        if state == "MENU":
            ui.draw_menu(screen, "COBRALIA: ASCENSION", "Pressione ENTER para Jogar")
        elif state == "GAME_OVER":
            ui.draw_menu(screen, "GAME OVER", f"Pontuação Final: {snake.score} | ENTER para Reiniciar")
        elif state == "VICTORY":
            ui.draw_menu(screen, "VITÓRIA!", f"O Guardião Corrompido caiu! Pontos: {snake.score}")
        elif state == "PLAY":
            # Maçã e PowerUps
            pygame.draw.rect(screen, APPLE_COLOR, (apple.x*TILE_SIZE, apple.y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if powerup:
                pygame.draw.circle(screen, POWERUP_COLOR, 
                                 (int(powerup["pos"].x*TILE_SIZE + TILE_SIZE/2), int(powerup["pos"].y*TILE_SIZE + TILE_SIZE/2)), 
                                 TILE_SIZE//2)

            # Cobra
            for i, part in enumerate(snake.body):
                color = SNAKE_COLOR if i == 0 else (SNAKE_COLOR[0]-20, SNAKE_COLOR[1]-20, SNAKE_COLOR[2]-20)
                if 'GHOST' in snake.effects: color = (255, 255, 255)
                pygame.draw.rect(screen, color, (part.x*TILE_SIZE, part.y*TILE_SIZE, TILE_SIZE-1, TILE_SIZE-1), border_radius=4)

            # Inimigo
            if enemy:
                pygame.draw.rect(screen, ENEMY_COLOR, (enemy.pos.x*TILE_SIZE, enemy.pos.y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            
            # Chefão
            if boss:
                pygame.draw.rect(screen, BOSS_COLOR, 
                               (boss.rect.x*TILE_SIZE, boss.rect.y*TILE_SIZE, boss.rect.width*TILE_SIZE, boss.rect.height*TILE_SIZE))
                for wp in boss.weak_points:
                    pygame.draw.rect(screen, WEAK_POINT_COLOR, (wp.x*TILE_SIZE, wp.y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
                for p in boss.projectiles:
                    pygame.draw.circle(screen, APPLE_COLOR, (int(p.x*TILE_SIZE), int(p.y*TILE_SIZE)), TILE_SIZE//3)

            ui.draw_hud(screen, snake, lm.levels[lm.current].get("goal", 1), apples_collected)

        pygame.display.flip()

if __name__ == "__main__":
    main()