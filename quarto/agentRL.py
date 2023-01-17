import logging
import argparse
import copy
import random
import quarto
import numpy as np
import operator as op
import utilities

class ReinforcementLearning(quarto.Player):
    '''Reinforcement Learning Agent'''

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)
        self.learning = False
        self.knowledge = dict()
        self.current

    def set_learning(self, value: bool):
        self.learning = value

    def choose_piece(self) -> int:
        return random.randint(0, 15)

    def place_piece(self) -> tuple[int, int]:
        return random.randint(0, 3), random.randint(0, 3)