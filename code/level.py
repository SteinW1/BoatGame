import pygame
from settings import *
from support import import_csv_layout, import_folder
from debug import debug
from camera import PlayerBoxCamera
from player import Player
from tileobject import TileObject
from dock import Dock

class Level:
    def __init__(self, clock) -> None:
        
        self.game_clock = clock
        self.active = True
        self.display_surface = pygame.display.get_surface()

        # set map size
        self.level_width = MAP_TILE_WIDTH * TILESIZE
        self.level_height = MAP_TILE_HEIGHT * TILESIZE
        
        # setup sprites
        self.visible_sprites = CameraGroup(self)
        self.collidable_sprites = pygame.sprite.Group()
        
        # setup map
        self.create_map()
        
    def create_map(self) -> None:
        """
        Creates the current level map. Reads the tile maps and initializes necessary game objects.
        """
        # import layout files for the map
        tilemaps= {
            'map_boundary': import_csv_layout('../map/pippen_test_map_Boundary.csv'),
            'map_docks': import_csv_layout('../map/pippen_test_map_Docks.csv')
        }
        
        # create map floor
        self.background_surface = pygame.image.load('../graphics/tilemap/pippen_test_map.png').convert_alpha()
        self.background_rect = self.background_surface.get_rect(topleft = (0,0))
        self.background = (self.background_surface, self.background_rect)
        
        self.player = Player((30,30), [self.visible_sprites], self.collidable_sprites) 
        self.docks = []
        
        for map_set, map_set_data in tilemaps.items():
            for row_index, row in enumerate(map_set_data):
                for column_index, column in enumerate(row):
                    if column != '-1': 
                        x = column_index * TILESIZE
                        y = row_index * TILESIZE
                                        
                        if map_set == 'map_boundary':
                            TileObject((x,y), [self.collidable_sprites], 'boundary')

                        if map_set == 'map_docks':
                            self.docks.append(Dock(len(self.docks)+1, (x,y)))
                            print('Place Object Created')

        # create the player
        self.player = Player((30,30), [self.visible_sprites], self.collidable_sprites)
        
        print('Main World Map Created')
        
    def run(self, game_states) -> None: # called once per iteration of the game loop
        """
        Called once per iteration of the game loop.
        
        Parameters:
            game_states:
        """
        # update dock objects
        for dock in self.docks:
            if self.player.current_port == None:
                dock.player_proximity_check(self.player)
            else:
                self.docks[self.player.current_port - 1].player_proximity_check(self.player)
        
        self.visible_sprites.update()
        
        self.draw()

        if self.player.request_to_dock:            
            self.switch_state(game_states['town'])

        if self.player.debug_mode == True:
            debug(f'XY: {round(self.player.position[0])}/{round(self.player.position[1])} FPS:{round(self.game_clock.get_fps())}')
            
    def draw(self):
        self.visible_sprites.custom_draw(self.player, self.background)
        
    def switch_state(self, new_state):        
        self.active = False
        new_state.active = True

class CameraGroup(pygame.sprite.Group):
    def __init__(self, level) -> None:
        super().__init__()
        self.camera = PlayerBoxCamera(level) # edit this line to change camera types
  
    def custom_draw(self, player, background) -> None:
        """
        Calls on the camera object to draw sprite groups.
        
        Parameters:
            player:
            
            background:
        """
        self.camera.draw(self, player, background)