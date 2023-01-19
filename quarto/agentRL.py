import logging
import argparse
import copy
import random
import quarto
import numpy as np
import operator as op
import utilities
import main

class ReinforcementLearning(quarto.Player):
    '''Reinforcement Learning Agent'''

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)
        self.learning = False
        self.knowledge = dict() 
        self.current = dict()

    def set_learning(self, value: bool):
        '''set RF agent in learning mode if value equal true, otherwise set it on evaluation mode.'''
        self.learning = value

    def save_knowledge(self, win):
        '''save the move made in this game scoring accordinng with the outcome (win)'''
        for board, value in self.current.items():
            if board in self.knowledge:
                if "choose_piece" in value:
                    not_in = True 
                    for element in self.knowledge[board]["choose_piece"]:
                        if element[0] == value["choose_piece"]:
                            not_in = False
                            element[1]+= 1 if win else -1
                    if not_in:
                        self.knowledge[board]["choose_piece"].append([value["choose_piece"], 1 if win else -1])
                else:
                    not_in = True 
                    for element in self.knowledge[board]["place_piece"]:
                        if element[0] == value["place_piece"]:
                            not_in = False
                            element[1]+= 1 if win else -1
                    if not_in:
                        self.knowledge[board]["place_piece"].append([value["place_piece"], 1 if win else -1])        
            else:
                self.knowledge[board] = {"choose_piece": list(), "place_piece": list()}
                if "choose_piece" in value:
                    self.knowledge[board]["choose_piece"].append([value["choose_piece"], 1 if win else -1])
                else:
                    self.knowledge[board]["place_piece"].append([value["place_piece"], 1 if win else -1])
        
        self.current = dict()

    def choose_piece(self) -> int:
        board = self.get_game().get_board_status()
        free_pieces = list(utilities.free_pieces(self).keys())           
        choose = random.choice(free_pieces)
        if self.learning:
            self.current[np.array2string(board)] = {"choose_piece": choose}
            return choose
        else:
            best = None
            if np.array2string(board) in self.knowledge:
                for piece_score in self.knowledge[np.array2string(board)]["choose_piece"]:
                    if best == None or best[1] < piece_score[1]:
                        best = piece_score
                if best != None:
                    return best[0]
            else:
                return choose

    def place_piece(self) -> tuple[int, int]:
        board = self.get_game().get_board_status()
        free_place = utilities.free_place(self)
        choose = random.choice(free_place)
        if self.learning:
            
            self.current[np.array2string(board)] = {"place_piece": choose}
            return choose[1], choose[0]
        else:
            best = None
            if np.array2string(board) in self.knowledge:
                for place_score in self.knowledge[np.array2string(board)]["place_piece"]:
                    if best == None or best[1] < place_score[1]:
                        best = place_score
                if best != None:
                    return best[0][1], best[0][1]
            else:
                return choose[1], choose[0]
                     



#
# TRAINING STUFF
#

def play_n_game_train(game: quarto.Quarto, RF: ReinforcementLearning, player2: quarto.Player, n: int):
    '''
    Play n games  for training player1 (Reinforcement Learning) against player2, print the winner ratio of player1 over player2, switching the starter at each game
    '''

    win_count = 0
    last_start = 1
    for i in range(n):
        game.reset()

        if last_start == 1:
            game.set_players((RF, player2))
            last_start = 0
        else:
            game.set_players((player2, RF))
            last_start = 1

        winner = game.run()
        
        if (winner == 0 and last_start == 0) or (winner == 1 and last_start == 1): #player1 win
            win_count+=1
            RF.save_knowledge(True)
        else: 
            RF.save_knowledge(False)
                    
    logging.warning(f"main: Winner ratio of RF during training: {win_count/n}")  

def play_n_game(game: quarto.Quarto, RF: ReinforcementLearning, player2: quarto.Player, n: int):
    '''
    Play n games player1 (Reinforcement Learning) against player2, print the winner ratio of player1 over player2, switching the starter at each game
    '''

    win_count = 0
    last_start = 1
    for i in range(n):
        game.reset()

        if last_start == 1:
            game.set_players((RF, player2))
            last_start = 0
        else:
            game.set_players((player2, RF))
            last_start = 1

        winner = game.run()
        
        if (winner == 0 and last_start == 0) or (winner == 1 and last_start == 1): #player1 win
            win_count+=1
                    
    logging.warning(f"main: Winner ratio of RF evaluation training: {win_count/n}")

def training():
    game = quarto.Quarto()
    #play_one_game(game, RandomPlayer(game), RandomPlayer(game))
    agentReinLear = ReinforcementLearning(game)
    agentReinLear.set_learning(True)
    play_n_game_train(game, agentReinLear, main.RandomPlayer(game), 100) 
    agentReinLear.set_learning(False) 
    play_n_game(game, agentReinLear, main.RandomPlayer(game), 100) 


if __name__ == '__main__':
    training()