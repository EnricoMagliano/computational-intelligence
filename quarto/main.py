# Free for personal or classroom use; see 'LICENSE.md' for details.
# https://github.com/squillero/computational-intelligence

import logging
import argparse
import random
import quarto
import myMinMax
import pastimesStrategy
import myPastimes


class RandomPlayer(quarto.Player):
    """Random player"""

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)

    def choose_piece(self) -> int:
        return random.randint(0, 15)

    def place_piece(self) -> tuple[int, int]:
        return random.randint(0, 3), random.randint(0, 3)

def play_one_game(game: quarto.Quarto, player1: quarto.Player, player2: quarto.Player):
    '''
    Play one game player1 against player2, print the winner
    '''
    game.set_players((player1, player2))
    winner = game.run()
    logging.warning(f"main: Winner: player {winner}")

def play_n_game(game: quarto.Quarto, player1: quarto.Player, player2: quarto.Player, n: int):
    '''
    Play n games player1 against player2, print the winner ratio of player1 over player2, switching the starter at each game
    '''

    win_count = 0
    last_start = 1
    for i in range(n):
        game.reset()

        if last_start == 1:
            game.set_players((player1, player2))
            last_start = 0
        else:
            game.set_players((player2, player1))
            last_start = 1

        winner = game.run()
        
        if (winner == 0 and last_start == 0) or (winner == 1 and last_start == 1): #player1 win
            win_count+=1
                    
    logging.warning(f"main: Winner ratio of player1: {win_count/n}")        

def main():
    game = quarto.Quarto()
    #play_one_game(game, RandomPlayer(game), RandomPlayer(game))
    play_n_game(game, myMinMax.MyMinMax(game), RandomPlayer(game), 10000)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count', default=0, help='increase log verbosity')
    parser.add_argument('-d',
                        '--debug',
                        action='store_const',
                        dest='verbose',
                        const=2,
                        help='log debug messages (same as -vv)')
    args = parser.parse_args()

    if args.verbose == 0:
        logging.getLogger().setLevel(level=logging.WARNING)
    elif args.verbose == 1:
        logging.getLogger().setLevel(level=logging.INFO)
    elif args.verbose == 2:
        logging.getLogger().setLevel(level=logging.DEBUG)

    main()