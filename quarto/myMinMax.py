import logging
import argparse
import random
import quarto
import numpy as np
import operator as op

class MyMinMax(quarto.Player):
    '''My MinMax strategy'''

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)
        self.opportunity = {}       #dict key=opportunity level, value= list of tuple of a list of position tuple and int that is charachteristics

    def choose_piece(self) -> int:
        self.check_opportunity() 
        print(self.opportunity)

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
        print("pos ", positive_char)
        print("neg ", negative_char)

        positive_char = [x for x in positive_char if x not in negative_char] #take only positive char that are not in negative char
        
        piece_index = self.find_piece(positive_char, negative_char) 
        if piece_index != -1:
                print("selected piece ", piece_index)
                return piece_index  
        else:   
            for e4 in self.opportunity[4]: #add level 4 in positive char
                positive_char.append(e4[1])

            positive_char = [x for x in positive_char if x not in negative_char]        
                
            piece_index = self.find_piece(positive_char, negative_char)
            if piece_index != -1:
                print("selected piece ", piece_index)
                return piece_index
            else:
                positive_char = range(8) #take all char
                negative_char = [] #reset negative for taking only level 1
                for e1 in self.opportunity[1]:  #take opportunity level 1 (worse for me)
                    if e1[1] not in negative_char:
                        negative_char.append(e1[1])
                positive_char = [x for x in positive_char if x not in negative_char]        
                
                piece_index = self.find_piece(positive_char, negative_char)
                if piece_index != -1:
                    print("selected piece ", piece_index)
                    return piece_index        


        
        return random.randint(0, 15)

    def place_piece(self) -> tuple[int, int]: #index are inverted
        #compute opportunity
        self.check_opportunity() 
        print(self.opportunity)

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
        print(positive_op)
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
        