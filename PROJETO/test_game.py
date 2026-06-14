# test_game.py
import unittest
import pygame
from entities import Snake
from config import GRID_W, GRID_H, INITIAL_SPEED, DASH_CD

class TestSnakeMechanics(unittest.TestCase):

    def setUp(self):
        """Inicializa as variáveis antes de cada teste."""
        pygame.init()
        self.snake = Snake()

    def test_initial_state(self):
        """Testa se a cobra inicia com os valores corretos de vida, pontos e tamanho."""
        self.assertEqual(self.snake.lives, 3, "A cobra deve começar com 3 vidas.")
        self.assertEqual(self.snake.score, 0, "A pontuação inicial deve ser 0.")
        self.assertEqual(len(self.snake.body), 3, "O corpo inicial deve ter 3 segmentos.")
        self.assertEqual(self.snake.speed, INITIAL_SPEED, "A velocidade deve ser a inicial.")

    def test_dash_mechanic(self):
        """Testa se o dash consome um segmento do corpo e aplica cooldown."""
        initial_length = len(self.snake.body)
        
        # Simulando que a cobra cresceu para poder dar dash (precisa de > 3 segmentos)
        self.snake.body.append(pygame.Vector2(0,0))
        self.snake.body.append(pygame.Vector2(0,0))
        
        self.snake.dash()
        
        self.assertEqual(self.snake.dash_cd, DASH_CD, "O cooldown do dash deve ser ativado.")
        self.assertTrue(self.snake.dash_active > 0, "O estado ativo do dash deve ser maior que 0.")
        self.assertEqual(len(self.snake.body), initial_length + 1, "O dash deve consumir 1 segmento do corpo.")

    def test_powerup_scissors(self):
        """Testa se o power-up da tesoura corta 30% da cobra."""
        # Força a cobra a ter 10 pedaços
        self.snake.body = [pygame.Vector2(0,0) for _ in range(10)]
        self.snake.apply_powerup('SCISSORS')
        
        # 30% de 10 é 3. Sobram 7.
        self.assertEqual(len(self.snake.body), 7, "A tesoura deve remover 30% dos segmentos.")

if __name__ == '__main__':
    unittest.main()