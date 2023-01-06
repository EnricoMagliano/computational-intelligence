import logging
import argparse
import random
import quarto
import numpy as np

class myMinMax(quarto.Player):
    '''My MinMax strategy'''

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)
        self.opportunity = []

    def choose_piece(self) -> int:
        self.check_opportunity()
        return random.randint(0, 15)

    def place_piece(self) -> tuple[int, int]:
        return random.randint(0, 3), random.randint(0, 3)

    def check_opportunity(self) -> None:
        mat = self.get_game().get_board_status()
        print("mat in check ")
        print(mat)
        for att in range(4):    #loop over attribute
            ausMat = np.zeros((4,4)) 
            for i in range(4): 
                for j in range(4): #loop over element -> make it more pythonic
                    if mat[i, j] == -1:
                        ausMat[i, j] = -1
                    elif self.get_game().get_piece_charachteristics(mat[i,j]).HIGH:
                        ausMat[i,j] = 1
            print("mat for high")
            print(ausMat)                    




#to be deleted
def play_one_game(game: quarto.Quarto, player1: quarto.Player, player2: quarto.Player):
    '''
    Play one game player1 against player2, print the winner
    '''
    game.set_players((player1, player2))
    winner = game.run()
    logging.warning(f"main: Winner: player {winner}")

class RandomPlayer(quarto.Player):
    """Random player"""

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)

    def choose_piece(self) -> int:
        return random.randint(0, 15)

    def place_piece(self) -> tuple[int, int]:
        return random.randint(0, 3), random.randint(0, 3)



def main():
    game = quarto.Quarto()
    #play_one_game(game, RandomPlayer(game), RandomPlayer(game))
    play_one_game(game, myMinMax(game), RandomPlayer(game))

if __name__ == '__main__':
    main()