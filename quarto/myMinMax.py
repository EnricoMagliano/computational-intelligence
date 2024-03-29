import logging
import argparse
import random
import quarto
import numpy as np
import operator as op
import utilities

class MyMinMax(quarto.Player):
    '''My MinMax strategy'''

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)
        self.opportunity = {}       #dict key=opportunity level, value= list of tuple of a list of position tuple and int that is charachteristics

    def choose_piece(self) -> int:
        utilities.check_opportunity(self) 
        #print(self.opportunity)

        negative_char = []
        positive_char = []
        for e1 in self.opportunity[1]:  #take opportunity level 1 (worse for me)
            if e1[1] not in negative_char:
                negative_char.append(e1[1])
        for e3 in self.opportunity[3]: #take opportunity level 3
            if e3[1] not  in negative_char:
                negative_char.append(e3[1])         
        for e2 in self.opportunity[2]:  #take opportunity level 2 (best for me)
            if e2[1] not in positive_char:
                positive_char.append(e2[1])  
        #print("pos ", positive_char)
        #print("neg ", negative_char)

        positive_char = [x for x in positive_char if x not in negative_char] #take only positive char that are not in negative char
        
        piece_index = utilities.find_piece(self, positive_char, negative_char) 
        if piece_index != -1:
                #print("selected piece ", piece_index)
                return piece_index  
        else:   
            for e4 in self.opportunity[4]: #add level 4 in positive char
                positive_char.append(e4[1])

            positive_char = [x for x in positive_char if x not in negative_char]        
                
            piece_index = utilities.find_piece(self, positive_char, negative_char)
            if piece_index != -1:
                #print("selected piece ", piece_index)
                return piece_index
            else:
                positive_char = range(8) #take all char
                negative_char = [] #reset negative for taking only level 1
                for e1 in self.opportunity[1]:  #take opportunity level 1 (worse for me)
                    if e1[1] not in negative_char:
                        negative_char.append(e1[1])
                positive_char = [x for x in positive_char if x not in negative_char]        
                
                piece_index = utilities.find_piece(self, positive_char, negative_char)
                if piece_index != -1:
                    #print("selected piece ", piece_index)
                    return piece_index        


        
        return random.randint(0, 15)

    def place_piece(self) -> tuple[int, int]: #index are inverted
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

    
   