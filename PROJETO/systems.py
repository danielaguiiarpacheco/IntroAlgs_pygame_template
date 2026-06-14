# systems.py
import json
import os
import pygame
from typing import Dict, Any
from config import *

class LevelManager:
    def __init__(self) -> None:
        self.levels: Dict[int, Any] = {}
        self.current: int = 1
        self.setup_directories()
        self.ensure_jsons()
        self.load_levels()

    def setup_directories(self) -> None:
        folders = ["assets/images", "assets/sounds", "assets/fonts", "assets/levels"]
        for folder in folders:
            os.makedirs(folder, exist_ok=True)

    def ensure_jsons(self) -> None:
        # Cria os JSONs automaticamente se não existirem
        data = {
            1: {"goal": 10, "enemy": False, "boss": False},
            2: {"goal": 15, "enemy": False, "boss": False},
            3: {"goal": 20, "enemy": True, "boss": False},
            4: {"goal": 1, "enemy": False, "boss": True}
        }
        for k, v in data.items():
            path = f"assets/levels/level_{k}.json"
            if not os.path.exists(path):
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(v, f, indent=4)

    def load_levels(self) -> None:
        for i in range(1, 5):
            with open(f"assets/levels/level_{i}.json", encoding="utf-8") as f:
                self.levels[i] = json.load(f)

class UIManager:
    def __init__(self) -> None:
        self.font = pygame.font.SysFont(None, 28)
        self.large_font = pygame.font.SysFont(None, 64)

    def draw_hud(self, screen: pygame.Surface, snake: Any, goal: int, apples: int) -> None:
        # Informações da Fase
        status = f"Fase: Maçãs {apples}/{goal} | Vidas: {snake.lives} | Pontos: {snake.score}"
        text = self.font.render(status, True, TEXT_COLOR)
        screen.blit(text, (10, 10))

        # Efeitos Ativos e Cooldown do Dash
        y_offset = 40
        if snake.dash_cd > 0:
            cd_text = self.font.render(f"Dash CD: {snake.dash_cd//1000}s", True, WEAK_POINT_COLOR)
            screen.blit(cd_text, (10, y_offset))
            y_offset += 25
            
        for effect, time in snake.effects.items():
            eff_text = self.font.render(f"{effect}: {time//1000}s", True, POWERUP_COLOR)
            screen.blit(eff_text, (10, y_offset))
            y_offset += 25

    def draw_menu(self, screen: pygame.Surface, title: str, subtitle: str) -> None:
        title_render = self.large_font.render(title, True, SNAKE_COLOR)
        sub_render = self.font.render(subtitle, True, TEXT_COLOR)
        screen.blit(title_render, (WIDTH//2 - title_render.get_width()//2, HEIGHT//2 - 50))
        screen.blit(sub_render, (WIDTH//2 - sub_render.get_width()//2, HEIGHT//2 + 20))