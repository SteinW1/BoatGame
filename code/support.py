from csv import reader, writer
from os import walk
import pygame

path = '../map/path_nodes.csv'
def create_csv_file(path, data):
    with open(path, 'w', newline='') as file:
        file_writer = writer(file)
        file_writer.writerows(data)

def import_csv_layout(path):
    csv_as_list = []
    with open(path) as csv:
        csv_layout = reader(csv, delimiter = ',')
        
        for row in csv_layout:
            csv_as_list.append(list(row))
        return csv_as_list

def import_folder(path):
    surface_list = []
    
    for _,__,image_files in walk(path):
        for file in image_files:
            full_path = path + '/' + file
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)
            
    return surface_list