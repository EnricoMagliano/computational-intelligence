import logging
import argparse
import random
import quarto
import numpy as np
import operator as op

class pastimes(quarto.Player):
    '''ourpastimes.com strategy'''

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)
        self.opportunity = {} #dict key=opportunity level, value= list of tuple of a list of position tuple and int that is charachteristics
        self.selected_char = random.randint(0,7) #select a char randomny

    def choose_piece(self) -> int:
        #print("sel char ", self.selected_char)
        opposite_char = self.selected_char-4 if self.selected_char > 3 else self.selected_char+4
        self.check_opportunity()
        #print(self.opportunity)
        
        selected_char_l1 = False
        for e1 in self.opportunity[1]:
            if e1[1] == self.selected_char:
                selected_char_l1 = True
                break
        selected_char_l2 = False
        for e2 in self.opportunity[2]:
            if e2[1] == self.selected_char:
                selected_char_l2 = True
                break

        #print("si in l1") if selected_char_l1 else print("no in l1")
        #print("si in l2") if selected_char_l2 else print("no in l2")   

        #if there aren't pair (l2) or tripletes (l1) of selected char, return a piece with selected char if doesn't match other l1 char        
        if selected_char_l1 == False and selected_char_l2 == False: 
            pieces_with_selected_char = self.select_pieces(self.selected_char)
            #print("piece with selected char ", pieces_with_selected_char)
            for p in pieces_with_selected_char:
                 if p not in self.get_game().get_board_status() and self.check_l1(p) == True:
                    #print("return ", p)
                    return p
            #gestire pezzi finiti
            print("allert1 pezzi finiti")     
        
        #if there are pair(l2) but there aren't tripletes(l1)
        #check number of element without selected char if even(pari)
        #return a piece with selected char, otherwise a piece without it
        if selected_char_l1 == False and selected_char_l2 == True:
            pieces_with_selected_char = self.select_pieces(self.selected_char)
            #print("opposite char ",opposite_char)

            pieces_without_selected_char_tot = self.select_pieces(opposite_char)
            pieces_without_selected_char = []
            for p in pieces_without_selected_char_tot: #filter pieces, take only the ones not already in the board
                if p not in self.get_game().get_board_status():
                    pieces_without_selected_char.append(p)
            #print("piece without sel char: ", pieces_without_selected_char)

            if len(pieces_without_selected_char)%2 == 0: #even check
                for p in pieces_with_selected_char:
                    if p not in self.get_game().get_board_status() and self.check_l1(p) == True:
                        #print("return ", p)
                        return p
                #gestire pezzi finiti
                print("allert2 pezzi finiti")
            else:
                for p in pieces_without_selected_char:
                    if p not in self.get_game().get_board_status() and self.check_l1(p) == True:
                        print("return ", p)
                        return p
                #gestire pezzi finiti
                print("allert3 pezzi finiti")        

        #if there are tripletes of selected char return a piece without selected char
        pieces_without_selected_char = self.select_pieces(opposite_char)
        for p in pieces_without_selected_char:
            if p not in self.get_game().get_board_status() and self.check_l1(p) == True:
                    return p                        

        #if there aren't any other posibilities return random
        return random.randint(0, 15)

    

    def place_piece(self) -> tuple[int, int]:
        #compute opportunity
        self.check_opportunity() 
        #print(self.opportunity)

        #take selected piece
        piece_index = self.get_game().get_selected_piece()
        piece = self.get_game().get_piece_charachteristics(piece_index)
        #print("index piece ", piece_index)
        piece_char = []
        
        #take piece char
        if piece.HIGH == True:
            piece_char.append(0)
        else:
            piece_char.append(4)
        if piece.COLOURED == True:
            piece_char.append(1)
        else:
            piece_char.append(5)
        if piece.SOLID == True:
            piece_char.append(2)
        else:
            piece_char.append(6)
        if piece.SQUARE == True:
            piece_char.append(3)
        else:
            piece_char.append(7)
        #print("piece char ", piece_char)


        positive_op = []
        for e1 in self.opportunity[1]:  #take opportunity level 1 (best for me)
            if e1 not in positive_op:
                positive_op.append(e1)
        #print(positive_op)
        #loop over level 1 opportunity until found one with char of selected piece
        for op in positive_op:  
            if op[1] in piece_char: 
                return op[0][0][1], op[0][0][0]


        positive_op = []
        for e3 in self.opportunity[3]:  #take opportunity level 3 (good for me)
            if e3 not in positive_op:
                positive_op.append(e3)
        negative_op_place = []
        for e2 in self.opportunity[2]:  #take opportunity level 2 (good for my opponent)
            for e2_place in e2[0]:    #take only the places not the tuple (list_of_place, char)
                if e2_place not in negative_op_place:
                    negative_op_place.append(e2_place) 
        #loop over positive opportunity (l3) checking if match with piece char 
        for op in positive_op:
            if op[1] in piece_char:
                for place in op[0]: #loop over opportunity places
                    if place not in negative_op_place: #check if place isn't also a place of opportunity of l2
                        return place[1], place[0]        

        #loop over free place
        board = self.get_game().get_board_status()
        for i in range(4):
            for j in range(4):
                if board[i][j] == -1 and (i,j) not in negative_op_place: #check if free place isn't a negative opportunity l2
                    return j, i

        #loop over free place 
        for i in range(4):
            for j in range(4):
                if board[i][j] == -1:
                    return j, i      #return first free place found  

    def check_l1(self, piece) -> bool:
        '''
        Return true if piece doesn't have charateristic in l1, otherwise return false
        '''
        l1 = []
        for e1 in self.opportunity[1]:
            if e1[1] not in l1:
                l1.append(e1[1])
        if self.get_game().get_piece_charachteristics(piece).HIGH == True:
            if 0 in l1:
                return False
        else: 
            if 4 in l1:
                return False
        if self.get_game().get_piece_charachteristics(piece).COLOURED == True:
            if 1 in l1:
                return False
        else: 
            if 5 in l1:
                return False
        if self.get_game().get_piece_charachteristics(piece).SOLID == True:
            if 2 in l1:
                return False
        else: 
            if 6 in l1:
                return False  
        if self.get_game().get_piece_charachteristics(piece).SQUARE == True:
            if 3 in l1:
                return False
        else: 
            if 7 in l1:
                return False              
        return True            

    def select_pieces(self, char):
        '''
        return a list of all index of piece with char
        '''
        select_pieces = []
        for i in range(16):
            if char == 0:
                if self.get_game().get_piece_charachteristics(i).HIGH == True:
                    select_pieces.append(i)
            elif char == 1:
                if self.get_game().get_piece_charachteristics(i).COLOURED == True:
                    select_pieces.append(i)
            elif char == 2:
                if self.get_game().get_piece_charachteristics(i).SOLID == True:
                    select_pieces.append(i)
            elif char == 3:
                if self.get_game().get_piece_charachteristics(i).SQUARE == True:
                    select_pieces.append(i)
            elif char == 4:
                if self.get_game().get_piece_charachteristics(i).HIGH == False:
                    select_pieces.append(i)
            elif char == 5:
                if self.get_game().get_piece_charachteristics(i).COLOURED == False:
                    select_pieces.append(i)
            elif char == 6:
                if self.get_game().get_piece_charachteristics(i).SOLID == False:
                    select_pieces.append(i)
            elif char == 7:
                if self.get_game().get_piece_charachteristics(i).SQUARE == False:
                    select_pieces.append(i)   

        return select_pieces                           

    def save_opportunity(self, vet, i, verticale, char) -> None:
        free_places = []
        ind_diag = 0
        ind_diag_rev = 3
        for j in range(4):
            if vet[j] == -1: #check free place
                if verticale == 0: #vet is horiz
                    if i == -1: #check if is main diag
                        free_places.append((ind_diag,ind_diag))
                    else:
                        free_places.append((i, j))
                else:
                    if i == -1: #check if is antidiag
                        free_places.append((ind_diag,ind_diag_rev))
                    else:   
                        free_places.append((j,i))
            ind_diag+=1 
            ind_diag_rev-=1          
        self.opportunity[len(free_places)].append((free_places, char)) #append tupla in the correct dict list 
        #print("save ", (free_places, char))                   

    def check_opportunity(self) -> None:
        self.opportunity = {1: [], 2: [], 3: [], 4: []} #reset opportunity vector
        mat = self.get_game().get_board_status() #get board
        #print("mat in check ")
        #print(mat)

        
        for i in range(4):
            horiz = mat[i]
            vert = mat[:,i]
            
            
            #HORIZ
            #check if in horiz there are not element without char HIGH
            if sum(1 for x in horiz if not self.get_game().get_piece_charachteristics(x).HIGH and x != -1) == 0:
                
                self.save_opportunity(horiz, i, 0, 0)

            #check if in horiz there are not element without char COLOURED 
            if sum(1 for x in horiz if not self.get_game().get_piece_charachteristics(x).COLOURED and x != -1) == 0:
                
                self.save_opportunity(horiz, i, 0, 1)

            #check if in horiz there are not element without char SOLID 
            if sum(1 for x in horiz if not self.get_game().get_piece_charachteristics(x).SOLID and x != -1) == 0:
                
                self.save_opportunity(horiz, i, 0, 2)

            #check if in horiz there are not element without char SQUARE 
            if sum(1 for x in horiz if not self.get_game().get_piece_charachteristics(x).SQUARE and x != -1) == 0:
                
                self.save_opportunity(horiz, i, 0, 3)

            #check if in horiz there are not element with char HIGH -> are all low
            if sum(1 for x in horiz if self.get_game().get_piece_charachteristics(x).HIGH and x != -1) == 0:
                
                self.save_opportunity(horiz, i, 0, 4)

            #check if in horiz there are not element with char COLOURED -> are all WHITE 
            if sum(1 for x in horiz if self.get_game().get_piece_charachteristics(x).COLOURED and x != -1) == 0:
                
                self.save_opportunity(horiz, i, 0, 5)

            #check if in horiz there are not element with char SOLID -> are all holled 
            if sum(1 for x in horiz if self.get_game().get_piece_charachteristics(x).SOLID and x != -1) == 0:
                
                self.save_opportunity(horiz, i, 0, 6)

            #check if in horiz there are not element with char SQUARE -> are all CIRCUL 
            if sum(1 for x in horiz if self.get_game().get_piece_charachteristics(x).SQUARE and x != -1) == 0:
                
                self.save_opportunity(horiz, i, 0, 7)
            
            
            #VERT    
            #check if in vert there are not element without char HIGH
            if sum(1 for x in vert if not self.get_game().get_piece_charachteristics(x).HIGH and x != -1) == 0:
                
                self.save_opportunity(vert, i, 1, 0)

            #check if in vert there are not element without char COLOURED 
            if sum(1 for x in vert if not self.get_game().get_piece_charachteristics(x).COLOURED and x != -1) == 0:
                
                self.save_opportunity(vert, i, 1, 1)

            #check if in vert there are not element without char SOLID 
            if sum(1 for x in vert if not self.get_game().get_piece_charachteristics(x).SOLID and x != -1) == 0:
                
                self.save_opportunity(vert, i, 1, 2)

            #check if in vert there are not element without char SQUARE 
            if sum(1 for x in vert if not self.get_game().get_piece_charachteristics(x).SQUARE and x != -1) == 0:
                
                self.save_opportunity(vert, i, 1, 3)

            #check if in vert there are not element with char HIGH -> are all low
            if sum(1 for x in vert if self.get_game().get_piece_charachteristics(x).HIGH and x != -1) == 0:
                
                self.save_opportunity(vert, i, 1, 4)

            #check if in vert there are not element with char COLOURED -> are all WHITE 
            if sum(1 for x in vert if self.get_game().get_piece_charachteristics(x).COLOURED and x != -1) == 0:
                
                self.save_opportunity(vert, i, 1, 5)

            #check if in vert there are not element with char SOLID -> are all holled 
            if sum(1 for x in vert if self.get_game().get_piece_charachteristics(x).SOLID and x != -1) == 0:
                
                self.save_opportunity(vert, i, 1, 6)

            #check if in vert there are not element with char SQUARE -> are all CIRCUL 
            if sum(1 for x in vert if self.get_game().get_piece_charachteristics(x).SQUARE and x != -1) == 0:
                
                self.save_opportunity(vert, i, 1, 7)                       

        
        diag = mat.diagonal() #take main diagonal
        #Diag
        #check if in diag there are not element without char HIGH
        if sum(1 for x in diag if not self.get_game().get_piece_charachteristics(x).HIGH and x != -1) == 0:
            
            self.save_opportunity(diag, -1, 0, 0)

        #check if in diag there are not element without char COLOURED 
        if sum(1 for x in diag if not self.get_game().get_piece_charachteristics(x).COLOURED and x != -1) == 0:
        
            self.save_opportunity(diag, -1, 0, 1)

        #check if in diag there are not element without char SOLID 
        if sum(1 for x in diag if not self.get_game().get_piece_charachteristics(x).SOLID and x != -1) == 0:
            
            self.save_opportunity(diag, -1, 0, 2)

        #check if in diag there are not element without char SQUARE 
        if sum(1 for x in diag if not self.get_game().get_piece_charachteristics(x).SQUARE and x != -1) == 0:
           
            self.save_opportunity(diag, -1, 0, 3)

        #check if in diag there are not element with char HIGH -> are all low
        if sum(1 for x in diag if self.get_game().get_piece_charachteristics(x).HIGH and x != -1) == 0:
           
            self.save_opportunity(diag, -1, 0, 4)

        #check if in diag there are not element with char COLOURED -> are all WHITE 
        if sum(1 for x in diag if self.get_game().get_piece_charachteristics(x).COLOURED and x != -1) == 0:
            
            self.save_opportunity(diag, -1, 0, 5)

        #check if in diag there are not element with char SOLID -> are all holled 
        if sum(1 for x in diag if self.get_game().get_piece_charachteristics(x).SOLID and x != -1) == 0:
            
            self.save_opportunity(diag, -1, 0, 6)

        #check if in diag there are not element with char SQUARE -> are all CIRCUL 
        if sum(1 for x in diag if self.get_game().get_piece_charachteristics(x).SQUARE and x != -1) == 0:
            
            self.save_opportunity(diag, -1, 0, 7)

        diag = np.fliplr(mat).diagonal() #take anti diagonal
        if sum(1 for x in diag if not self.get_game().get_piece_charachteristics(x).HIGH and x != -1) == 0:
            
            self.save_opportunity(diag, -1, 1, 0)

        #check if in diag there are not element without char COLOURED 
        if sum(1 for x in diag if not self.get_game().get_piece_charachteristics(x).COLOURED and x != -1) == 0:
            
            self.save_opportunity(diag, -1, 1, 1)

        #check if in diag there are not element without char SOLID 
        if sum(1 for x in diag if not self.get_game().get_piece_charachteristics(x).SOLID and x != -1) == 0:
            
            self.save_opportunity(diag, -1, 1, 2)

        #check if in diag there are not element without char SQUARE 
        if sum(1 for x in diag if not self.get_game().get_piece_charachteristics(x).SQUARE and x != -1) == 0:
            
            self.save_opportunity(diag, -1, 1, 3)

        #check if in diag there are not element with char HIGH -> are all low
        if sum(1 for x in diag if self.get_game().get_piece_charachteristics(x).HIGH and x != -1) == 0:
            
            self.save_opportunity(diag, -1, 1, 4)

        #check if in diag there are not element with char COLOURED -> are all WHITE 
        if sum(1 for x in diag if self.get_game().get_piece_charachteristics(x).COLOURED and x != -1) == 0:
            
            self.save_opportunity(diag, -1, 1, 5)

        #check if in diag there are not element with char SOLID -> are all holled 
        if sum(1 for x in diag if self.get_game().get_piece_charachteristics(x).SOLID and x != -1) == 0:
            
            self.save_opportunity(diag, -1, 1, 6)

        #check if in diag there are not element with char SQUARE -> are all CIRCUL 
        if sum(1 for x in diag if self.get_game().get_piece_charachteristics(x).SQUARE and x != -1) == 0:
            
            self.save_opportunity(diag, -1, 1, 7)        


#to be deleted




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
    play_n_game(game, pastimes(game), RandomPlayer(game), 1000)

if __name__ == '__main__':
    main()