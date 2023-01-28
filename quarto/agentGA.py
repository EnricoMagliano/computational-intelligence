import logging
import argparse
import copy
import random
import quarto
import numpy as np
import operator as op
import utilities
import main

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

    def set_genome(self, genome):
        '''set the genome for the current GA agent'''
        self.genome = genome 

    def choose_piece(self) -> int:
        return random.randint(0, 15)

    def place_piece(self) -> tuple[int, int]:
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
        genome = (random.random(), random.random(), random.random())
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
                    
    logging.warning(f"main: Winner ratio of GA evaluation training: {win_count/n}")

def training():
    '''
    training the GA agent and evaluete it
    ''' 
    best_genome = GA()
    game = quarto.Quarto()
    agentGen = GeneticAlgorithm(game)
    agentGen.set_genome(best_genome) 
    play_n_game(game, agentGen, main.RandomPlayer(game), NUM_EVAL_MATCH) 


if __name__ == '__main__':
    training()