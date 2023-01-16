import logging
import argparse
import random
import quarto
import numpy as np
import operator as op
import utilities

class Pastimes(quarto.Player):
    '''ourpastimes.com strategy'''

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)
        self.opportunity = {} #dict key=opportunity level, value= list of tuple of a list of position tuple and int that is charachteristics
        self.selected_char = None #select a char

    def reset(self):
        '''
        Reset the agent for a new game
        '''
        
        self.selected_char = random.randint(0, 7)


    def choose_piece(self) -> int:
        #print("pastimes choose")
        #check if a new game is started
        if np.all(self.get_game().get_board_status() == -1):
            self.reset()

        
        #print("sel char ", self.selected_char)
        opposite_char = self.selected_char-4 if self.selected_char > 3 else self.selected_char+4
        utilities.check_opportunity(self)
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
            pieces_with_selected_char = utilities.select_pieces(self, self.selected_char)
            #print("piece with selected char ", pieces_with_selected_char)

            returnable = []
            for p in pieces_with_selected_char:
                 if p not in self.get_game().get_board_status() and utilities.check_l1(self, p) == True:
                    returnable.append(p)
            if len(returnable) > 0:
                return random.choice(returnable)       #return a random element from the returnable ones 
                 
        
        #if there are pair(l2) but there aren't tripletes(l1)
        #check number of element without selected char if even(pari)
        #return a piece with selected char, otherwise a piece without it
        if selected_char_l1 == False and selected_char_l2 == True:
            pieces_with_selected_char = utilities.select_pieces(self, self.selected_char)
            #print("opposite char ",opposite_char)

            pieces_without_selected_char_tot = utilities.select_pieces(self, opposite_char)
            pieces_without_selected_char = []
            for p in pieces_without_selected_char_tot: #filter pieces, take only the ones not already in the board
                if p not in self.get_game().get_board_status():
                    pieces_without_selected_char.append(p)
            #print("piece without sel char: ", pieces_without_selected_char)

            if len(pieces_without_selected_char)%2 == 0: #even check
                returnable = []
                for p in pieces_with_selected_char:
                    if p not in self.get_game().get_board_status() and utilities.check_l1(self, p) == True:
                        returnable.append(p)
                if len(returnable) > 0:        
                    return random.choice(returnable)        
                
            else:
                returnable = []
                for p in pieces_without_selected_char:
                    if p not in self.get_game().get_board_status() and utilities.check_l1(self, p) == True:
                        returnable.append(p)
                if len(returnable) > 0:
                    return random.choice(returnable)
                        

        #if there are tripletes of selected char return a piece without selected char and without l1 char
        returnable = []

        #pieces_without_selected_char = utlities.select_pieces(self, opposite_char) #this worsen the result
        #for p in pieces_without_selected_char:
        for p in range(16): 
            if p not in self.get_game().get_board_status() and utilities.check_l1(self, p) == True:
                returnable.append(p)
        if len(returnable) > 0:
            return random.choice(returnable)

        #if there aren't any other posibilities return random
        return random.randint(0, 15)

    

    def place_piece(self) -> tuple[int, int]:
        #print("pasttimes place")
        if np.all(self.get_game().get_board_status() == -1):
            self.reset()
        
        #compute opportunity
        utilities.check_opportunity(self) 
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

        #check if need a block and try to block
        if len(positive_op) > 0:
            move = utilities.block_next(self, piece_index)
            if move != None:
                return move
        
        
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
       

                               