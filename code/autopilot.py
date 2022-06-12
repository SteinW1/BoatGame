import pygame
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
from settings import *

class Autopilot:
    def __init__(self, master_object):
        self.master_object = master_object
        self.map_matrix = self.create_matrix()
        self.pathing_matrix = self.update_pathing_matrix()
        
        ####################################################
        #TODO: master object needs to be able to change this
        self.current_target = (14, 25)
        self.autopilot_status = False
        ####################################################
        
        self.current_path_matrix = self.calculate_path()
        self.current_path = self.convert_path()

        print(self.current_path)
        
    def update_pathing_matrix(self):
        '''
        Creates a new matrix of points where the master sprite can move without colliding into other collidable objects.        
        '''
        new_matrix = []
        for row_index, row in enumerate(self.map_matrix):
            row_list = []
            for column_index, column in enumerate(row):
                node = '1'
                if self._check_collision(column_index, row_index):
                #if self.map_matrix[row_index][column_index] == '0':
                    node = '0'
                row_list.append(node)
            new_matrix.append(row_list)
        return new_matrix
                    
    def _check_collision(self, column, row):
        test_rect = self.master_object.hitbox
        test_rect.center = (column*16) + (self.master_object.hitbox_width//2), (row*16) + (self.master_object.hitbox_height//2)
        print(test_rect.center, test_rect)
        for sprite in self.master_object.collidable_sprites:
            if sprite.hitbox.colliderect(test_rect):
                return True       
            
    def create_matrix(self):
        matrix = []
        for row in range(MAP_TILE_HEIGHT):
            row_list = []
            for column in range(MAP_TILE_WIDTH):
                node = '1'
                for sprite in self.master_object.collidable_sprites:
                    if sprite.hitbox.collidepoint((column*16) + (TILESIZE//2),(row*16) + (TILESIZE//2)):
                        node = '0'
                        break
                row_list.append(node)
            matrix.append(row_list)            
        return matrix
    
    def calculate_path(self):
        '''
        Returns a path as a list that was created using the A* star pathing algorithm.
        '''
        # 1. create a grid
        grid = Grid(matrix = self.pathing_matrix)
        # 2. create start and end cell
        start_node = grid.node(self.master_object.position[0] // 16, self.master_object.position[1] // 16)
        end_node = grid.node(self.current_target[0],self.current_target[1])
        # 3. create a finder with movement style
        finder = AStarFinder(diagonal_movement = DiagonalMovement.always)
        # 4. use the finder to find the path
        path, runs = finder.find_path(start_node, end_node, grid)
        return path
    
    def convert_path(self):
        matrix = self.current_path_matrix
        for row in matrix:
            for column in row:
                
        return path