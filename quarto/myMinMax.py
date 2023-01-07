import logging
import argparse
import random
import quarto
import numpy as np
import operator as op

class myMinMax(quarto.Player):
    '''My MinMax strategy'''

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)
        self.opportunity = []       # list of tuple of a list of position tuple and int that is charachteristics

    def choose_piece(self) -> int:
        self.check_opportunity()
        return random.randint(0, 15)

    def place_piece(self) -> tuple[int, int]:
        return random.randint(0, 3), random.randint(0, 3)

    def save_opportunity(self, vet, i, verticale, char) -> None:
        free_places = []
        for j in range(4):
            if vet[j] == -1: #check free place
                if verticale == 0: #vet is horiz
                    free_places.append((i, j))
                else:
                    free_places.append((j,i))
        self.opportunity.append((free_places, char))
        print("save ", (free_places, char))                   

    def check_opportunity(self) -> None:
        self.opportunity = [] #reset opportunity vector
        mat = self.get_game().get_board_status() #get board
        print("mat in check ")
        print(mat)


        for i in range(4):
            horiz = mat[i]
            vert = mat[:,i]
            
            #check if in horiz there are not element without char HIGH
            if sum(1 for x in horiz if not self.get_game().get_piece_charachteristics(x).HIGH and x != -1) == 0:
                print("horiz high ", horiz)
                self.save_opportunity(horiz, i, 0, 0)

            #check if in horiz there are not element without char COLOURED 
            if sum(1 for x in horiz if not self.get_game().get_piece_charachteristics(x).COLOURED and x != -1) == 0:
                print("horiz col ", horiz)
                self.save_opportunity(horiz, i, 0, 1)

            #check if in horiz there are not element without char SOLID 
            if sum(1 for x in horiz if not self.get_game().get_piece_charachteristics(x).SOLID and x != -1) == 0:
                print("horiz solid ", horiz)
                self.save_opportunity(horiz, i, 0, 2)

            #check if in horiz there are not element without char SQUARE 
            if sum(1 for x in horiz if not self.get_game().get_piece_charachteristics(x).SQUARE and x != -1) == 0:
                print("horiz square ", horiz)
                self.save_opportunity(horiz, i, 0, 3)

            #check if in horiz there are not element with char HIGH -> are all low
            if sum(1 for x in horiz if self.get_game().get_piece_charachteristics(x).HIGH and x != -1) == 0:
                print("horiz low ", horiz)
                self.save_opportunity(horiz, i, 0, 4)

            #check if in horiz there are not element with char COLOURED -> are all WHITE 
            if sum(1 for x in horiz if self.get_game().get_piece_charachteristics(x).COLOURED and x != -1) == 0:
                print("horiz white ", horiz)
                self.save_opportunity(horiz, i, 0, 5)

            #check if in horiz there are not element with char SOLID -> are all holled 
            if sum(1 for x in horiz if self.get_game().get_piece_charachteristics(x).SOLID and x != -1) == 0:
                print("horiz holled ", horiz)
                self.save_opportunity(horiz, i, 0, 6)

            #check if in horiz there are not element with char SQUARE -> are all CIRCUL 
            if sum(1 for x in horiz if self.get_game().get_piece_charachteristics(x).SQUARE and x != -1) == 0:
                print("horiz circul ", horiz)
                self.save_opportunity(horiz, i, 0, 7)                   


            
        '''
        HighMat = np.zeros((4,4)) 
        ColMat = np.zeros((4,4))
        SquMat = np.zeros((4,4)) 
        SolMat = np.zeros((4,4))
        for i in range(4):      #loop for mark free place(-1), place used by other char(0), place of the right char(1) 
            for j in range(4): #loop over element -> make it more pythonic
                if mat[i, j] == -1:
                    HighMat[i, j] = -1
                    ColMat[i,j] = -1
                    SquMat[i,j] = -1
                    SolMat[i,j] = -1
                elif self.get_game().get_piece_charachteristics(mat[i,j]).HIGH:
                    HighMat[i,j] = 1
                elif self.get_game().get_piece_charachteristics(mat[i,j]).COLOURED:
                    ColMat[i,j] = 1
                elif self.get_game().get_piece_charachteristics(mat[i,j]).SQUARE:
                    SquMat[i,j] = 1 
                elif self.get_game().get_piece_charachteristics(mat[i,j]).SOLID:
                    SolMat[i,j] = 1       
        '''
       







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