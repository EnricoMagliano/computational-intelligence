import logging
import argparse
import copy
import random
import quarto
import numpy as np
import operator as op
import utilities
import main
import math

NUM_TRAINING_MATCH = 100
NUM_EVAL_MATCH = 10
NUM_GENERATION = 10
POPULATION_SIZE = 100
OFFSPRING_SIZE = 10

class GeneticAlgorithm(quarto.Player):
    '''Genetic Algorithm agent'''
    
    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)
        self.best_genome = None
        self.opportunity = {}   #dict key=opportunity level, value= list of tuple of a list of position tuple and int that is charachteristics

    def set_genome(self, genome):
        '''set the genome for the current GA agent'''
        self.genome = genome 

    def choose_piece(self) -> int:
        utilities.check_opportunity(self)

        level = math.ceil(self.genome[0]*4)
        chars = {}
        for _, char in self.opportunity[level]:
            if char not in chars:
                chars[char] = 1
            else:
                chars[char] += 1    

        free_piece = utilities.free_pieces(self)
        best_fit = None
        worse_fit = None
        for p_index, p_char in free_piece.items():
            score = 0
            for char in p_char:
                score += chars[char] if char in chars else 0
            if worse_fit == None or worse_fit[1] > score:
                worse_fit = (p_index, score)
            if best_fit == None or best_fit[1] < score:
                best_fit = (p_index, score)        
        if self.genome[1] < 0.5:
            if best_fit != None:
                return best_fit[0]
        else:
            if worse_fit != None:
                return worse_fit[0]        

        return random.randint(0, 15)

    def place_piece(self) -> tuple[int, int]:
        utilities.check_opportunity(self)
        piece_index = self.get_game().get_selected_piece()
        piece_char = utilities.get_pieces_char(self, piece_index)
        level = math.ceil(self.genome[2]*4)

        position_pos = []
        position_neg = utilities.free_place(self)
        for pos, char in self.opportunity[level]:
            for p in pos:
                if char in piece_char:
                    position_pos.append(p)
                    if p in position_neg:
                        position_neg.remove(p)
        if self.genome[3] < 0.5:
            if len(position_pos) > 0:
                choice = random.choice(position_pos)
                return choice[1], choice[0]
        else:
            if len(position_neg) > 0:
                choice = random.choice(position_neg)
                return choice[1], choice[0]        

        return random.randint(0, 3), random.randint(0, 3)




#
# GA STUFF
#

def fitness(genome): # calcolate the fisness
    game = quarto.Quarto()
    agent = GeneticAlgorithm(game)
    agent.set_genome(genome)
    opponent = main.RandomPlayer(game)
    return play_n_game(game, agent, opponent, NUM_EVAL_MATCH)

def generatePopulation(): #return population, one individual is a tuple of a mask array of the list taken and his fitness
    population = list()
    for genome in range(POPULATION_SIZE):
        genome = (random.random(), random.random(), random.random(), random.random())
        population.append((genome, fitness(genome)))
    return population    

def mutation(g):
    point = random.randint(0,len(g)-1)
    return g[:point] + (random.random(),) + g[point+1:]  

def select_parent(population, tornament_size=10):
    return max(random.choices(population, k=tornament_size), key=lambda i: i[1])      

def GA():
    best_sol = None 
    best_sol_fit = None
    
    population = generatePopulation()
    for generation in range(10):
        print("init gen: ", generation)
        offsprings = list()
        for i in range(OFFSPRING_SIZE):
            o = ()
            p = select_parent(population)
            o = mutation(p[0])
            offsprings.append((o, fitness(o)))
        population = population + offsprings   
        population = sorted(population, key=lambda i:i[1], reverse=True)[:POPULATION_SIZE]
            
    best_sol = population[0][0]
    best_sol_fit = population[0][1]
    print("after 100 generations")
    print("best solution:")
    print(best_sol)
    return best_sol

 
def play_n_game(game: quarto.Quarto, GA: GeneticAlgorithm, player2: quarto.Player, n: int):
    '''
    Play n games player1 (Genetic Algorithm) against player2, print the winner ratio of player1 over player2, switching the starter at each game
    '''

    win_count = 0
    last_start = 1
    for i in range(n):
        game.reset()

        if last_start == 1:
            game.set_players((GA, player2))
            last_start = 0
        else:
            game.set_players((player2, GA))
            last_start = 1

        winner = game.run()
        
        if (winner == 0 and last_start == 0) or (winner == 1 and last_start == 1): #player1 win
            win_count+=1
                    
    #logging.warning(f"main: Winner ratio of GA evaluation training: {win_count/n}")
    return win_count/n
def training():
    '''
    training the GA agent and evaluete it
    ''' 
    best_genome = GA()
    game = quarto.Quarto()
    agentGen = GeneticAlgorithm(game)
    agentGen.set_genome(best_genome) 
    result = play_n_game(game, agentGen, main.RandomPlayer(game), NUM_EVAL_MATCH) 
    print(f"main: Winner ratio of GA: {result}, with genome: {best_genome}")

if __name__ == '__main__':
    training()