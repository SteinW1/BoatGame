import pygame
from support import import_folder
from entity import Entity

class Player(Entity):
    def __init__(self, position, sprite_group, collidable_sprites) -> None:
        super().__init__(sprite_group)
        self.position = position
        self.collidable_sprites = collidable_sprites

        # player stats
        self.speed = 2    
        self.boat = 'schooner'
        self.animation = 'right'
        self.request_to_dock = False
        self.can_dock = False
        self.current_port = None
        
        # graphics setup
        self.import_assets()
        self.image = pygame.image.load(f'../graphics/player/{self.boat}/{self.animation}/{self.animation}_{self.animation_frame_index}.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = position)
        
        # player hitbox setup
        self.hitbox_xoffset = 0
        self.hitbox_yoffset = 55
        self.hitbox_width = 64
        self.hitbox_height = 9
        self.hitbox_position = (self.rect.x + self.hitbox_xoffset, self.rect.y + self.hitbox_yoffset)
        self.hitbox = pygame.Rect(self.hitbox_position,(self.hitbox_width, self.hitbox_height))
        
        # debug mode
        self.debug_mode = False
        self.debug_switchable = True
        self.debug_switch_time = None
        self.debug_mode_cooldown = 200
    
    def import_assets(self) -> None:
        sprite_path = f'../graphics/player/{self.boat}/'
        
        #import player animations
        self.animations = {
            'left':[], 'right':[],
        }
        
        for animation in self.animations.keys():
            full_path = sprite_path + animation
            self.animations[animation] = import_folder(full_path)
        
    def input(self) -> None:
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP ] or keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0    
            
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x =-1
            self.animation = 'left'
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.animation = 'right'
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.can_dock:
            self.request_to_dock = True
        else:
            self.request_to_dock = False

        # debug mode
        if keys[pygame.K_F3] and self.debug_switchable:
            if not self.debug_mode:
                self.debug_mode = True
                self.debug_switchable = False
                self.debug_switch_time = pygame.time.get_ticks()
            else:
                self.debug_mode = False
                self.debug_switchable = False
                self.debug_switch_time = pygame.time.get_ticks()
    
    def animate(self) -> None:
        
        animation = self.animations[self.animation]

        self.animation_frame_index += self.animation_speed
        if self.animation_frame_index >= len(animation):
            self.animation_frame_index = 0
            
        self.image = animation[int(self.animation_frame_index)]
    
    def update(self) -> None:
        self.input()
        self.animate()
        self.move(self.speed)