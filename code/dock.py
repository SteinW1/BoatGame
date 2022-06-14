import pygame
from settings import *    
    
class Dock:
    def __init__(self, dock_id, position):
        self.dock_id = dock_id
        self.position = (position[0] + (TILESIZE // 2)), (position[1] + (TILESIZE // 2)) # set as center of tile
        self.dock_radius = 4 # number in tiles
        self.docking_distance_squared = (self.dock_radius * TILESIZE) ** 2
        
    def get_player_distance(self, player_rect):
        player_position = player_rect.center
        self.player_distance_squared = ((player_position[0]-self.position[0])**2) + ((player_position[1]-self.position[1])**2)
        
    def player_proximity_check(self, player):
        self.get_player_distance(player.hitbox)
        if self.player_distance_squared < self.docking_distance_squared:
            self.ready = True
            player.current_port = self.dock_id
            player.can_dock = True
        else:
            player.current_port = None
            player.can_dock = False
