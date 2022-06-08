from csv import reader
from os import walk
import pygame

def import_csv_layout(path):
    terrain = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter = ',') # delimiter is what seperates each entry in the file
        
        for row in layout:
            terrain.append(list(row))
        return terrain

def import_folder(path):
    surface_list = []
    
    for _,__,image_files in walk(path):
        for i in image_files:
            full_path = path + '/' + i
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)
            
    return surface_list