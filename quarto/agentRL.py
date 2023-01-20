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
        self.knowledge = dict() #dict with board status as key and two list as value one for the score of all place and one for the piece
        self.current = dict() #dict for saving place and piece of the current game 

    def set_learning(self, value: bool):
        '''set RF agent in learning mode if value equal true, otherwise set it on evaluation mode.'''
        self.learning = value

    def save_knowledge(self, win):
        '''save the move made in this game scoring accordinng with the outcome (win)'''
        
        for board, value in self.current.items(): #loop over all the board status
            if board in self.knowledge: #check if already exist in the dict
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
        
        self.current = dict() #reset the current dict

    def choose_piece(self) -> int:
        board = self.get_game().get_board_status()
        free_pieces = list(utilities.free_pieces(self).keys())           
        choose = random.choice(free_pieces)

        if self.learning: #if agent is set in learning return a random piece from the free ones
            self.current[np.array2string(board)] = {"choose_piece": choose} #and save the choose in the current dict
            return choose

        else: #if agent is in eval mode select the piece with the highest score (>0) if it exists
            best = None
            if np.array2string(board) in self.knowledge:
                #piece_score is a tuple (piece_index, score)
                for piece_score in self.knowledge[np.array2string(board)]["choose_piece"]:
                    if best == None or best[1] < piece_score[1]:
                        best = piece_score
                if best != None and best[1] > 0: #check if exists a piece with score greater than 0
                    return best[0]
            return choose #if not exist return a random piece

    def place_piece(self) -> tuple[int, int]:
        
        board = self.get_game().get_board_status()
        free_place = utilities.free_place(self)
        choose = random.choice(free_place)

        if self.learning:   #if agent is set in learning return a random place from the free ones
            self.current[np.array2string(board)] = {"place_piece": choose} #and save the choose in the current dict
            return choose[1], choose[0]
        
        else:   #if agent is in eval mode select the place with the highest score (>0)  if it exists
            best = None
            if np.array2string(board) in self.knowledge:
                #place_score is a tuple (place_tuple, score)
                for place_score in self.knowledge[np.array2string(board)]["place_piece"]:
                    if best == None or best[1] < place_score[1]:
                        best = place_score
                if best != None and best[1] > 0: #check if exists a place with score greater than 0
                    return best[0][1], best[0][0]
            return choose[1], choose[0] #if not exist return a random place from the free ones
                     



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
    '''
    training the RF agent and evaluete it
    '''
    game = quarto.Quarto()
    agentReinLear = ReinforcementLearning(game)
    agentReinLear.set_learning(True) 
    play_n_game_train(game, agentReinLear, main.RandomPlayer(game), 10000)
    agentReinLear.set_learning(False) 
    play_n_game(game, agentReinLear, main.RandomPlayer(game), 1000) 


if __name__ == '__main__':
    training()