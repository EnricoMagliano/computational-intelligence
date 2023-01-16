import logging
import argparse
import copy
import random
import quarto
import numpy as np
import operator as op
import utilities


class MyPastimes(quarto.Player):
    '''Generalization of ourpastimes.com strategy'''
    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)
        self.opportunity = {} #dict key=opportunity level, value= list of tuple of a list of position tuple and int that is charachteristics
        self.pieces = {} #dict: key= piece index, value = list of char

    def choose_piece(self) -> int:
        #compute opportunity
        utilities.check_opportunity(self)
        #print(self.opportunity)
        #take free pieces
        self.pieces = utilities.free_pieces(self)

        #save all free piece with l1 char
        returnable_piece = {} #piece withot char in l1
        for index, piece_char in self.pieces.items():
            not_in = True
            for l1 in self.opportunity[1]: #loop over l1 opp
                if l1[1] in piece_char:
                    not_in = False
            if not_in:        
                returnable_piece[index] = piece_char #add piece without l1 char       
        

        cont_senza_char = {} #dict where key = char and value are free piece without char
        for l2 in self.opportunity[2]:
            cont_senza_char[l2[1]] = sum(1 for p in self.pieces.values() if l2[1] not in p)
        #for each piece cont favor +1 and sfavor as -1
        score = {}
        for p_index, p_char in returnable_piece.items():
            score[p_index] = 0
            for c, n in cont_senza_char.items():
                if n%2 == 0: #if even char in piece is a favor
                    if c in p_char:
                        score[p_index] += 1
                    else:
                        score[p_index] -= 1
                else:      #if odd nor char in piece is a favor
                    if c not in p_char:
                        score[p_index] += 1
                    else:
                        score[p_index] -= 1 
        best_piece_index = None
        for p_index, value in score.items():
            if best_piece_index == None or best_piece_index < value:
                best_piece_index = p_index
        if best_piece_index != None:
            #print("choose from l2 char index: ", best_piece_index)  #return the best if exists           
            return best_piece_index
        '''
        #simple version
        #try to return an element
        for c, n in cont_senza_char.items():
            #if even give at the opponent a piece of the char c
            if n%2 == 0:
                for p, p_char in returnable_piece.items():
                    if c in p_char:
                        #print("choose from l2 char index: ", p)
                        return p
            else: #if odd give at the opponeny a piece without char c
                for p, p_char in returnable_piece.items():
                    if c not in p_char:
                        #print("choose from opposite l2 char index: ", p)
                        return p
        '''


        #return from returnable list if it's not empty or choose from free piece
        if len(returnable_piece) > 0:
            choose = random.choice(list(returnable_piece.keys()))
            #print("choose from returnable :) index: ", choose)
            return choose #return a good piece 
        else:
            choose = random.choice(list(self.pieces.keys()))
            #print("choose from free piece :( index: ", choose)
            return choose  #return not a good piece

     
    def place_piece(self) -> tuple[int, int]:
        #compute opportunity
        utilities.check_opportunity(self)
        #print(self.opportunity)
        #take free pieces
        self.pieces = utilities.free_pieces(self)

        #take selected piece
        piece_index = self.get_game().get_selected_piece()
        piece_char = utilities.get_pieces_char(self, piece_index)
        #print("piece char ", piece_char)

        #consider first l1 opportunities
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


        #consider l3 opportunity
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
        
        return random.randint(0, 3), random.randint(0, 3)              

    