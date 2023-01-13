import logging
import argparse
import random
import quarto
import numpy as np
import operator as op
import utilities

class MyPastimes(quarto.Player):
    '''Generalization of ourpastimes.com strategy'''
    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)
        self.opportunity = {} #dict key=opportunity level, value= list of tuple of a list of position tuple and int that is charachteristics

    def choose_piece(self) -> int:
        utilities.check_opportunity(self)
        print(self.opportunity)
        return random.randint(0, 15)

    def place_piece(self) -> tuple[int, int]:
        return random.randint(0, 3), random.randint(0, 3)    