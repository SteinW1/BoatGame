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
        
        #####################################################
        #TODO: master object needs to be able to change these
        self.current_target = (301, 297)
        self.autopilot_status = False
        #####################################################
        
        self.current_path_points = self.calculate_path()
        self.current_path = self.convert_path_nodes_to_xylocation()
    
    def update_pathing_matrix(self):
        '''Creates a new matrix of points where the master sprite can move without colliding into other collidable objects.'''
        new_matrix = []
        for row_index, row in enumerate(self.map_matrix):
            row_list = []
            for column_index, column in enumerate(row):
                node = '0' if self._check_collision(column_index, row_index) else '1'
                row_list.append(node)
            new_matrix.append(row_list)
        return new_matrix    
            
    def create_matrix(self):
        '''Returns a matrix of points based on the size of the tilemap and the size of the map tiles'''
        matrix = []
        for row in range(MAP_TILE_HEIGHT):
            row_list = []
            for column in range(MAP_TILE_WIDTH):
                node = '1'
                for sprite in self.master_object.collidable_sprites:
                    if sprite.hitbox.collidepoint((column*TILESIZE) + (TILESIZE//2),(row*TILESIZE) + (TILESIZE//2)):
                        node = '0'
                        break
                row_list.append(node)
            matrix.append(row_list)
        return matrix
        
    def convert_path_nodes_to_xylocation(self):
        '''Multiplies the x,y of a node by the game tilesize to get the display location of the node.'''
        path = []
        for point in self.current_path_points:
            path.append((point[0]*TILESIZE, point[1]*TILESIZE))
        return path
    
    def calculate_path(self):
        '''Returns a path as a list that was created using the A* star pathing algorithm.'''
        # 1. create a grid
        grid = Grid(matrix = self.pathing_matrix)

        # 2. create start and end cell
        start_node = grid.node(self.master_object.hitbox.x // 16, self.master_object.hitbox.y // 16)
        end_node = grid.node(self.current_target[0]//16,self.current_target[1]//16)

        # 3. create a hitboxfinder with movement style
        finder = AStarFinder(diagonal_movement = DiagonalMovement.always)

        # 4. use the finder to find the path
        path, runs = finder.find_path(start_node, end_node, grid)

        return path

    def _check_collision(self, column, row):
        test_rect = pygame.Rect(self.master_object.hitbox.x, self.master_object.hitbox.y, self.master_object.hitbox.w, self.master_object.hitbox.h)
        test_rect.topleft = (column*16), (row*16)
        for sprite in self.master_object.collidable_sprites:
            if sprite.hitbox.colliderect(test_rect):
                return True
