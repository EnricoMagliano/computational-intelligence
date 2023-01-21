import logging
import argparse
import copy
import random
import quarto
import numpy as np
import operator as op
import utilities
import main
import myMinMax

NUM_TRAINING_MATCH = 1000
NUM_EVAL_MATCH = 100

class ReinforcementLearning(quarto.Player):
    '''Reinforcement Learning Agent'''

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)
        self.learning = False
        self.knowledge = dict() #dict with board status as key and two list as value one for the score of all place and one for the piece
        self.current = dict() #dict for saving place and piece of the current game 
        self.random_factor = 1 #close to 1 -> more exploration, close to 0 more exploitation
        self.num_match = 0
        self.tot_num_matches = NUM_TRAINING_MATCH

    def set_learning(self, value: bool):
        '''set RF agent in learning mode if value equal true, otherwise set it on evaluation mode.'''
        self.learning = value

    def save_knowledge(self, win):
        '''save the move made in this game scoring accordinng with the outcome (win)'''
        
        #value is a dict that contains choosen piece or place piece
        for board, value in self.current.items(): #loop over all the board status in current dict
            
            if board in self.knowledge: #check if board already exist in the dict
                
                if "choose_piece" in value: #check if value is choose_piece type
                    not_in = True 
                    for element in self.knowledge[board]["choose_piece"]:
                        if element[0] == value["choose_piece"]: #if piece already exists for board status in knowledge dict
                            not_in = False
                            element[1]+= 1 if win else -1 #update it 
                    if not_in: #otherwise add it and initialize
                        self.knowledge[board]["choose_piece"].append([value["choose_piece"], 1 if win else -1])
                
                else: #check if value is place_piece type
                    not_in = True 
                    for element in self.knowledge[board]["place_piece"]: 
                        if element[0] == value["place_piece"]: #if place already exists for board status in knowledge dict
                            not_in = False
                            element[1]+= 1 if win else -1 #update it
                    if not_in: #otherwise add it and initialize
                        self.knowledge[board]["place_piece"].append([value["place_piece"], 1 if win else -1])        
            
            else: #if board status isn't already in the knowledge dict add it creating the 2 list, one for piece scoring the other for place scoring
                self.knowledge[board] = {"choose_piece": list(), "place_piece": list()}
                if "choose_piece" in value: #and add piece or place in the right list, with score according to the outcomes
                    self.knowledge[board]["choose_piece"].append([value["choose_piece"], 1 if win else -1])
                else:
                    self.knowledge[board]["place_piece"].append([value["place_piece"], 1 if win else -1])
        
        self.num_match +=1 #update number of played matches
        self.random_factor = 1- 2*(self.num_match/self.tot_num_matches) #update random factor for encrease the exploitation with match prograssion
        self.current = dict() #reset the current dict

    def choose_piece(self) -> int:
        board = self.get_game().get_board_status()
        free_pieces = list(utilities.free_pieces(self).keys())           
        choose = random.choice(free_pieces)

        #if random_factor > random(0,1) -> exploration otherwise exploitation
        if self.learning and random.random() < self.random_factor: #if agent is set in learning return a random piece from the free ones
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

        #if random_factor > random(0,1) -> exploration otherwise exploitation
        if self.learning and random.random() < self.random_factor:   #if agent is set in learning and exploration return a random place from the free ones 
            self.current[np.array2string(board)] = {"place_piece": choose} #and save the choose in the current dict
            return choose[1], choose[0]
        
        else:   #if agent is in eval (or exploitation) mode select the place with the highest score (>0)  if it exists
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
    play_n_game_train(game, agentReinLear, myMinMax.MyMinMax(game), NUM_TRAINING_MATCH)
    agentReinLear.set_learning(False) 
    play_n_game(game, agentReinLear, myMinMax.MyMinMax(game), NUM_EVAL_MATCH) 


if __name__ == '__main__':
    training()