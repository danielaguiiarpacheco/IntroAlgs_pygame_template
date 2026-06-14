# entities.py
import pygame
import random
from typing import List, Dict
from config import *

class Snake:
    def __init__(self) -> None:
        self.body: List[pygame.Vector2] = [pygame.Vector2(GRID_W // 2, GRID_H // 2 + i) for i in range(3)]
        self.direction: pygame.Vector2 = pygame.Vector2(0, -1)
        self.speed: int = INITIAL_SPEED
        self.move_timer: int = 0
        self.grow_pending: int = 0
        
        # Sistemas de Dash e Status
        self.dash_active: int = 0
        self.dash_cd: int = 0
        self.lives: int = 3
        self.effects: Dict[str, int] = {}
        self.score: int = 0

    def update(self, dt: int) -> None:
        # Gerenciamento de Cooldowns
        if self.dash_cd > 0: self.dash_cd -= dt
        if self.dash_active > 0: self.dash_active -= dt

        # Gerenciamento de Efeitos (Power-ups)
        to_remove = []
        for e, time in self.effects.items():
            self.effects[e] -= dt
            if self.effects[e] <= 0: to_remove.append(e)
        for e in to_remove: del self.effects[e]

        # Modificadores de Velocidade
        current_speed = self.speed
        if self.dash_active > 0: current_speed = int(self.speed / DASH_MULT)
        if 'PEPPER' in self.effects: current_speed = int(self.speed * 0.5)
        if 'ICE' in self.effects: current_speed = int(self.speed * 1.4)

        # Movimentação em Grade
        self.move_timer += dt
        if self.move_timer >= current_speed:
            self.move_timer = 0
            head = self.body[0] + self.direction
            self.body.insert(0, head)
            
            if self.grow_pending > 0:
                self.grow_pending -= 1
            else:
                self.body.pop()

    def dash(self) -> None:
        if self.dash_cd <= 0 and len(self.body) > 3:
            self.dash_active = DASH_DUR
            self.dash_cd = DASH_CD
            self.body.pop() # Custo de 1 segmento

    def apply_powerup(self, p_type: str) -> None:
        if p_type == 'SCISSORS':
            cut = max(1, int(len(self.body) * 0.3))
            self.body = self.body[:-cut]
        else:
            self.effects[p_type] = 8000 # 8 segundos de duração

class Enemy:
    def __init__(self, pos: Tuple[int, int]) -> None:
        self.pos: pygame.Vector2 = pygame.Vector2(pos)
        self.timer: int = 0
        
    def update(self, dt: int, target: pygame.Vector2) -> None:
        self.timer += dt
        if self.timer > 300: # IA Simples: move a cada 300ms
            self.timer = 0
            dx = target.x - self.pos.x
            dy = target.y - self.pos.y
            if abs(dx) > abs(dy):
                self.pos.x += 1 if dx > 0 else -1
            else:
                self.pos.y += 1 if dy > 0 else -1

class Boss:
    def __init__(self) -> None:
        self.rect: pygame.Rect = pygame.Rect(GRID_W // 2 - 5, 2, 10, 4)
        self.weak_points: List[pygame.Vector2] = [
            pygame.Vector2(self.rect.left + 2, self.rect.bottom),
            pygame.Vector2(self.rect.centerx, self.rect.bottom),
            pygame.Vector2(self.rect.right - 2, self.rect.bottom)
        ]
        self.hp: int = 3
        self.timer: int = 0
        self.projectiles: List[pygame.Vector2] = []
        self.dir: int = 1

    def update(self, dt: int) -> None:
        self.timer += dt
        if self.timer > 500:
            self.rect.x += self.dir
            for wp in self.weak_points: wp.x += self.dir
            
            # Rebater nas bordas
            if self.rect.right >= GRID_W - 2 or self.rect.left <= 2:
                self.dir *= -1
            self.timer = 0
            
            # Padrão de Disparo
            if random.random() > 0.4:
                self.projectiles.append(pygame.Vector2(self.rect.centerx, self.rect.bottom))

        # Atualizar Projéteis
        for p in self.projectiles:
            p.y += 0.5