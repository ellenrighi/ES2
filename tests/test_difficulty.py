import unittest

from src.ai.difficulty import Difficulty, get_depth


class DifficultyTests(unittest.TestCase):

    def test_difficulty_levels_exist(self):
        # Confere se os tres niveis de dificuldade foram definidos.
        self.assertEqual(Difficulty.EASY.value, "easy")
        self.assertEqual(Difficulty.MEDIUM.value, "medium")
        self.assertEqual(Difficulty.HARD.value, "hard")

    def test_medium_depth(self):
        # O nivel medio usa uma busca menor.
        self.assertEqual(get_depth(Difficulty.MEDIUM), 2)

    def test_hard_depth(self):
        # O nivel dificil usa uma busca mais profunda.
        self.assertEqual(get_depth(Difficulty.HARD), 4)

    def test_easy_has_no_depth(self):
        # O nivel facil usa movimentos aleatorios.
        self.assertIsNone(get_depth(Difficulty.EASY))


if __name__ == "__main__":
    unittest.main()