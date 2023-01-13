import logging
import argparse
import random
import quarto
import numpy as np
import operator as op

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