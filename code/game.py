import sys
import pygame
from settings import *
from level import Level
from town import Town

class Game:
    def __init__(self) -> None:
        
        pygame.init()
        self.game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Pippen')
        self.game_states = {
            'level' : Level(self.clock),
            'town' : Town(self.clock),
        }
        
    def run(self) -> None:
        """ The main game loop."""
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            for state in self.game_states.keys():
                if self.game_states[state].active:
                    self.game_states[state].run(self.game_states)
                
            pygame.display.update()
            self.clock.tick(FPS)
         
if __name__ == '__main__':
    game = Game()
    game.run()