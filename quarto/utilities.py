import logging
import argparse
import random
import quarto
import numpy as np
import operator as op

def get_pieces_char(agent, index):
    '''
    Return array of the characteristic of the index piece
    '''
    piece = agent.get_game().get_piece_charachteristics(index)
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
    return piece_char


def char_l1(self):
    '''
    return a list of l1 char
    '''
    array = list()
    for l1 in self.opportunity[1]:
        if l1[1] not in array:
            array.append(l1[1])
    return array      

def free_pieces(agent):
    '''
    Return a dict of free piece indexes as value and array of charateristic as value
    '''
    board = agent.get_game().get_board_status()
    pieces = dict()
    for p in range(16):
        if p not in board:
            pieces[p] = get_pieces_char(agent, p)

    return pieces    

def free_place(agent):
    '''
    Return a list tuple of free place in the board
    '''    
    board = agent.get_game().get_board_status()
    free_place = []
    for i in range(4):
        for j in range(4):
            if board[i][j] == -1:
                free_place.append((i, j))
    return free_place            

def block_next(self, sel_piece_index) -> tuple[int, int]:
        '''
        Check if next turn, I have to choose a piece that let my opponent win.
        In this case return a position when place piece to block the winning.
        Otherwise return None
        ''' 
        sel_piece = self.get_game().get_piece_charachteristics(sel_piece_index)

        positive_char_opponent = {} #dict where key is l1 char and value the number of place 
        for e1 in self.opportunity[1]:
            if e1[1] not in positive_char_opponent:
                positive_char_opponent[e1[1]] = 1
            else:
                 positive_char_opponent[e1[1]] += 1 

        #print("in block", positive_char_opponent)

        #take all piece indexes not already placed in the board
        free_pieces = list(range(16))
        free_pieces.remove(sel_piece_index) #remove selected piece
        for r in self.get_game().get_board_status():
            for p in r:
                if p != -1:
                    free_pieces.remove(p)    
        
        for p in free_pieces:
            match = False 
            for c in positive_char_opponent:
                if c == 0:
                    if self.get_game().get_piece_charachteristics(p).HIGH == True:
                        match = True
                elif c == 1:    
                    if self.get_game().get_piece_charachteristics(p).COLOURED == True:
                        match = True
                elif c == 2:
                    if self.get_game().get_piece_charachteristics(p).SOLID == True:
                        match = True   
                elif c == 3:
                    if self.get_game().get_piece_charachteristics(p).SQUARE == True:
                        match = True   
                elif c == 4:
                    if self.get_game().get_piece_charachteristics(p).HIGH == False:
                        match = True  
                elif c == 5:
                    if self.get_game().get_piece_charachteristics(p).COLOURED == False:
                        match = True   
                elif c == 6:
                    if self.get_game().get_piece_charachteristics(p).SOLID == False:
                        match = True  
                elif c == 7:
                    if self.get_game().get_piece_charachteristics(p).SQUARE == False:
                        match = True 
                
            if match == False: #find a piece that doesn't match
                #print("find piece not match ", p)
                return None   #no need block, find a piece without char in l1

        #search char with one place
        blockable_char = []
        for c in positive_char_opponent:
            if positive_char_opponent[c] == 1: #try to block char c if have one place
                blockable_char.append(c)
        #print("blockable char ", blockable_char)



        for b_c in blockable_char:
            for l1 in self.opportunity[1]:
                if l1[1] == b_c:
                    place = l1[0][0]
                    if simulation(self, place, sel_piece_index, free_pieces):
                         return place[1], place[0]
        return None  #if there aren't any single place for one char -> unblockable -> return None

        '''
        for c in blockable_char:
            place = None
            not_in_l2 = True
            for e1 in self.opportunity[1]:
                if e1[1] == c:
                    place = e1[0][0]
            for e2 in self.opportunity[2]:
                for place_2 in e2[0]:
                    if place_2 == place:
                        not_in_l2 = False
            if not_in_l2:
                #print("not il l2, ", place)   
                return place[1], place[0]    
        
        if len(blockable_char) > 0: 
            place = None
            random_choose = random.choice(blockable_char)
            for e1 in self.opportunity[1]:
                if e1[1] == random_choose:
                    place = e1[0][0]
            #print("place in l2, ", place)        
            return place[1], place[0]   
        return None  #if there aren't any single place for one char -> unblockable -> return None        
        '''

def simulation(self, place, piece_index, free_piece):
    '''
    Simulate placing the selected piece in the selected place.
    If this doesn't compromise nothing return true, otherwise return False.
    '''
    for l2 in self.opportunity[2]:
        if place in l2[0] and l2[1] in get_pieces_char(self, piece_index):
            piece_no_match = False
            for p in free_piece:
                if l2[1] not in get_pieces_char(self, p):
                    piece_no_match = True 
            if piece_no_match == False:   
                return False
    return True 

def check_l1(self, piece) -> bool:
    '''
    Return true if piece doesn't have charateristic in l1, otherwise return false
    '''
    #print("in check l1")
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

def find_piece(self, positive_char, negative_char) -> int:
    '''
    Return the index of a piece that satisfies positive char and doesn't have negative char
    Rturn -1 if there aren't pieces like that 
    '''
    
    # take all pieces not in board
    pieces_not_in_board = [x for x in range(16) if x not in self.get_game().get_board_status()]
    piesces_match_char = []
    for i in pieces_not_in_board:  #take pieces that have at least one positive char 
        for c in positive_char:
            if c == 0:
                if self.get_game().get_piece_charachteristics(i).HIGH == True and i not in piesces_match_char:
                    piesces_match_char.append(i)
            elif c == 1:    
                if self.get_game().get_piece_charachteristics(i).COLOURED == True and i not in piesces_match_char:
                    piesces_match_char.append(i)
            elif c == 2:
                if self.get_game().get_piece_charachteristics(i).SOLID == True and i not in piesces_match_char:
                    piesces_match_char.append(i)   
            elif c == 3:
                if self.get_game().get_piece_charachteristics(i).SQUARE == True and i not in piesces_match_char:
                    piesces_match_char.append(i)   
            elif c == 4:
                if self.get_game().get_piece_charachteristics(i).HIGH == False and i not in piesces_match_char:
                    piesces_match_char.append(i)  
            elif c == 5:
                if self.get_game().get_piece_charachteristics(i).COLOURED == False and i not in piesces_match_char:
                    piesces_match_char.append(i)   
            elif c == 6:
                if self.get_game().get_piece_charachteristics(i).SOLID == False and i not in piesces_match_char:
                    piesces_match_char.append(i)   
            elif c == 7:
                if self.get_game().get_piece_charachteristics(i).SQUARE == False and i not in piesces_match_char:
                    piesces_match_char.append(i)
        for c in negative_char:
            if c == 0:
                if self.get_game().get_piece_charachteristics(i).HIGH == True and i in piesces_match_char:
                    piesces_match_char.remove(i)
            elif c == 1:    
                if self.get_game().get_piece_charachteristics(i).COLOURED == True and i in piesces_match_char:
                    piesces_match_char.remove(i)
            elif c == 2:
                if self.get_game().get_piece_charachteristics(i).SOLID == True and i in piesces_match_char:
                    piesces_match_char.remove(i)   
            elif c == 3:
                if self.get_game().get_piece_charachteristics(i).SQUARE == True and i in piesces_match_char:
                    piesces_match_char.remove(i)   
            elif c == 4:
                if self.get_game().get_piece_charachteristics(i).HIGH == False and i in piesces_match_char:
                    piesces_match_char.remove(i)  
            elif c == 5:
                if self.get_game().get_piece_charachteristics(i).COLOURED == False and i in piesces_match_char:
                    piesces_match_char.remove(i)   
            elif c == 6:
                if self.get_game().get_piece_charachteristics(i).SOLID == False and i in piesces_match_char:
                    piesces_match_char.remove(i)   
            elif c == 7:
                if self.get_game().get_piece_charachteristics(i).SQUARE == False and i in piesces_match_char:
                    piesces_match_char.remove(i)            
            
    if len(piesces_match_char) > 0: #if there are at least one matched element return it
        return piesces_match_char[0]  
    return -1 #return -1 if thera isn't any piece that match the char and isn't already place                                                        
             

def save_opportunity(agent, vet, i, verticale, char) -> None:
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
        agent.opportunity[len(free_places)].append((free_places, char)) #append tupla in the correct dict list 
        #print("save ", (free_places, char)) 

def check_opportunity(agent) -> None:
        '''
        return a dict with all the opportunity on the board.
        Key is the level of the opportunity
        Value is an arrey of tuple (array of free position of the opp, char of opp)
        '''
        agent.opportunity = {1: [], 2: [], 3: [], 4: []} #reset opportunity vector
        mat = agent.get_game().get_board_status() #get board
        #print("mat in check ")
        #print(mat)

        
        for i in range(4):
            horiz = mat[i]
            vert = mat[:,i]
            
            
            #HORIZ
            #check if in horiz there are not element without char HIGH
            if sum(1 for x in horiz if not agent.get_game().get_piece_charachteristics(x).HIGH and x != -1) == 0:
                
                save_opportunity(agent, horiz, i, 0, 0)

            #check if in horiz there are not element without char COLOURED 
            if sum(1 for x in horiz if not agent.get_game().get_piece_charachteristics(x).COLOURED and x != -1) == 0:
                
                save_opportunity(agent, horiz, i, 0, 1)

            #check if in horiz there are not element without char SOLID 
            if sum(1 for x in horiz if not agent.get_game().get_piece_charachteristics(x).SOLID and x != -1) == 0:
                
                save_opportunity(agent, horiz, i, 0, 2)

            #check if in horiz there are not element without char SQUARE 
            if sum(1 for x in horiz if not agent.get_game().get_piece_charachteristics(x).SQUARE and x != -1) == 0:
                
                save_opportunity(agent, horiz, i, 0, 3)

            #check if in horiz there are not element with char HIGH -> are all low
            if sum(1 for x in horiz if agent.get_game().get_piece_charachteristics(x).HIGH and x != -1) == 0:
                
                save_opportunity(agent, horiz, i, 0, 4)

            #check if in horiz there are not element with char COLOURED -> are all WHITE 
            if sum(1 for x in horiz if agent.get_game().get_piece_charachteristics(x).COLOURED and x != -1) == 0:
                
                save_opportunity(agent, horiz, i, 0, 5)

            #check if in horiz there are not element with char SOLID -> are all holled 
            if sum(1 for x in horiz if agent.get_game().get_piece_charachteristics(x).SOLID and x != -1) == 0:
                
                save_opportunity(agent, horiz, i, 0, 6)

            #check if in horiz there are not element with char SQUARE -> are all CIRCUL 
            if sum(1 for x in horiz if agent.get_game().get_piece_charachteristics(x).SQUARE and x != -1) == 0:
                
                save_opportunity(agent, horiz, i, 0, 7)
            
            
            #VERT    
            #check if in vert there are not element without char HIGH
            if sum(1 for x in vert if not agent.get_game().get_piece_charachteristics(x).HIGH and x != -1) == 0:
                
                save_opportunity(agent, vert, i, 1, 0)

            #check if in vert there are not element without char COLOURED 
            if sum(1 for x in vert if not agent.get_game().get_piece_charachteristics(x).COLOURED and x != -1) == 0:
                
                save_opportunity(agent, vert, i, 1, 1)

            #check if in vert there are not element without char SOLID 
            if sum(1 for x in vert if not agent.get_game().get_piece_charachteristics(x).SOLID and x != -1) == 0:
                
                save_opportunity(agent, vert, i, 1, 2)

            #check if in vert there are not element without char SQUARE 
            if sum(1 for x in vert if not agent.get_game().get_piece_charachteristics(x).SQUARE and x != -1) == 0:
                
                save_opportunity(agent, vert, i, 1, 3)

            #check if in vert there are not element with char HIGH -> are all low
            if sum(1 for x in vert if agent.get_game().get_piece_charachteristics(x).HIGH and x != -1) == 0:
                
                save_opportunity(agent, vert, i, 1, 4)

            #check if in vert there are not element with char COLOURED -> are all WHITE 
            if sum(1 for x in vert if agent.get_game().get_piece_charachteristics(x).COLOURED and x != -1) == 0:
                
                save_opportunity(agent, vert, i, 1, 5) 

            #check if in vert there are not element with char SOLID -> are all holled 
            if sum(1 for x in vert if agent.get_game().get_piece_charachteristics(x).SOLID and x != -1) == 0:
                
                save_opportunity(agent, vert, i, 1, 6)

            #check if in vert there are not element with char SQUARE -> are all CIRCUL 
            if sum(1 for x in vert if agent.get_game().get_piece_charachteristics(x).SQUARE and x != -1) == 0:
                
                save_opportunity(agent, vert, i, 1, 7)                       

        
        diag = mat.diagonal() #take main diagonal
        #Diag
        #check if in diag there are not element without char HIGH
        if sum(1 for x in diag if not agent.get_game().get_piece_charachteristics(x).HIGH and x != -1) == 0:
            
            save_opportunity(agent, diag, -1, 0, 0)

        #check if in diag there are not element without char COLOURED 
        if sum(1 for x in diag if not agent.get_game().get_piece_charachteristics(x).COLOURED and x != -1) == 0:
        
            save_opportunity(agent, diag, -1, 0, 1)

        #check if in diag there are not element without char SOLID 
        if sum(1 for x in diag if not agent.get_game().get_piece_charachteristics(x).SOLID and x != -1) == 0:
            
            save_opportunity(agent, diag, -1, 0, 2)

        #check if in diag there are not element without char SQUARE 
        if sum(1 for x in diag if not agent.get_game().get_piece_charachteristics(x).SQUARE and x != -1) == 0:
           
            save_opportunity(agent, diag, -1, 0, 3)

        #check if in diag there are not element with char HIGH -> are all low
        if sum(1 for x in diag if agent.get_game().get_piece_charachteristics(x).HIGH and x != -1) == 0:
           
            save_opportunity(agent, diag, -1, 0, 4)

        #check if in diag there are not element with char COLOURED -> are all WHITE 
        if sum(1 for x in diag if agent.get_game().get_piece_charachteristics(x).COLOURED and x != -1) == 0:
            
            save_opportunity(agent, diag, -1, 0, 5)

        #check if in diag there are not element with char SOLID -> are all holled 
        if sum(1 for x in diag if agent.get_game().get_piece_charachteristics(x).SOLID and x != -1) == 0:
            
            save_opportunity(agent, diag, -1, 0, 6)

        #check if in diag there are not element with char SQUARE -> are all CIRCUL 
        if sum(1 for x in diag if agent.get_game().get_piece_charachteristics(x).SQUARE and x != -1) == 0:
            
            save_opportunity(agent, diag, -1, 0, 7)

        diag = np.fliplr(mat).diagonal() #take anti diagonal
        if sum(1 for x in diag if not agent.get_game().get_piece_charachteristics(x).HIGH and x != -1) == 0:
            
            save_opportunity(agent, diag, -1, 1, 0)

        #check if in diag there are not element without char COLOURED 
        if sum(1 for x in diag if not agent.get_game().get_piece_charachteristics(x).COLOURED and x != -1) == 0:
            
            save_opportunity(agent, diag, -1, 1, 1)

        #check if in diag there are not element without char SOLID 
        if sum(1 for x in diag if not agent.get_game().get_piece_charachteristics(x).SOLID and x != -1) == 0:
            
            save_opportunity(agent, diag, -1, 1, 2)

        #check if in diag there are not element without char SQUARE 
        if sum(1 for x in diag if not agent.get_game().get_piece_charachteristics(x).SQUARE and x != -1) == 0:
            
            save_opportunity(agent, diag, -1, 1, 3)

        #check if in diag there are not element with char HIGH -> are all low
        if sum(1 for x in diag if agent.get_game().get_piece_charachteristics(x).HIGH and x != -1) == 0:
            
            save_opportunity(agent, diag, -1, 1, 4)

        #check if in diag there are not element with char COLOURED -> are all WHITE 
        if sum(1 for x in diag if agent.get_game().get_piece_charachteristics(x).COLOURED and x != -1) == 0:
            
            save_opportunity(agent, diag, -1, 1, 5)

        #check if in diag there are not element with char SOLID -> are all holled 
        if sum(1 for x in diag if agent.get_game().get_piece_charachteristics(x).SOLID and x != -1) == 0:
            
            save_opportunity(agent, diag, -1, 1, 6)

        #check if in diag there are not element with char SQUARE -> are all CIRCUL 
        if sum(1 for x in diag if agent.get_game().get_piece_charachteristics(x).SQUARE and x != -1) == 0:
            
            save_opportunity(agent, diag, -1, 1, 7)