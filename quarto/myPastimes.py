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
        self.pieces = utilities.pieces(self) #dict: key= piece index, value = list of char

    def choose_piece(self) -> int:
        #compute opportunity
        utilities.check_opportunity(self)
        print(self.opportunity)

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
        
        #try to return an element
        for c, n in cont_senza_char.items():
            #if even give at the opponent a piece of the char c
            if n%2 == 0:
                for p, p_char in returnable_piece.items():
                    if c in p_char:
                        return p
            else: #if odd give at the opponeny a piece without char c
                for p, p_char in returnable_piece.items():
                    if c not in p_char:
                        return p



        #return from returnable list if it's not empty or choose from free piece
        if len(returnable_piece) > 0:
            choose = random.choice(list(returnable_piece.keys()))
            print("choose from returnable :) index: ", choose)
            self.pieces.pop(choose)
            return choose #return a good piece 
        else:
            choose = random.choice(list(self.pieces.keys()))
            print("choose from free piece :( index: ", choose)
            self.pieces.pop(choose)
            return choose  #return not a good piece

     
    def place_piece(self) -> tuple[int, int]:
        piece_index = self.get_game().get_selected_piece()
        if piece_index in self.pieces.keys():
            self.pieces.pop(piece_index)
        return random.randint(0, 3), random.randint(0, 3)    

    def char_l1(self):
        '''
        return a list of l1 char
        '''
        array = list()
        for l1 in self.opportunity[1]:
            if l1[1] not in array:
                array.append(l1[1])
        return array            