import pygame 
import sys
import os
from Entities import PhysicsEntity, Player
from Tilemap import Tilemap, Tile
from Clouds import Clouds
import utils
from Game import Game

# CONSTANTS
BLACK = (0,0,0)
SKY_BLUE = (14, 219, 248)
SCREEN_HORIZONTAL = 1920
SCREEN_VERTICAL = 1080

# Classes
class LevelEditor(Game):
    def __init__(self):
        
        super().__init__()
        pygame.init()
        pygame.display.set_caption('Level Editor')


        self.player=None
        self.tilemap = Tilemap(self)

        self.tile_size = 16
        self.camera_rect = pygame.Rect([50,50], (self.tile_size,self.tile_size))

        self.camera_velocity = [0,0]
        self.movement_left = 0
        self.movement_right = 0
        self.movement_up = 0
        self.movement_down = 0 
         
        self.level_size = [int((SCREEN_HORIZONTAL) * 4) , int((SCREEN_VERTICAL) * 4)]
        self.mouse_pos = pygame.mouse.get_pos()
        self.current_block = 'grass'
        self.erase_block = False
        # we can just add a tile directly to self.tilemap 
        # we need to get the users mouse pixel positon and convert it into a grid position
        # then go tilemap[grid_position] = new_tile

    def get_mouse_grid_pos(self):
        
        #return (int(self.mouse_pos[0] // self.tile_size - offset[0]), int(self.mouse_pos[1] // self.tile_size - offset[1])) # not sure what to do with the offset


        return (int(self.mouse_pos[0] // self.tile_size), int(self.mouse_pos[1] // self.tile_size)) # not sure what to do with the offset
    
    def update_camera(self,movement=(0,0)): 
        
        frame_movement = (movement[0] + self.camera_velocity[0], movement[1] + self.camera_velocity[1])

        self.camera_rect.x += frame_movement[0] 
        self.camera_rect.y += frame_movement[1]

        if self.camera_rect.x >= self.level_size[0]:
            self.camera_rect.x -=frame_movement[0]
    
    def change_level_size(self, multiplier):

        self.level_size = [(SCREEN_HORIZONTAL) * multiplier , (SCREEN_VERTICAL) * multiplier]


    def run_game(self):
        pygame.mouse.set_visible(False)
        while self.run: 
            self.display.blit(self.assets['background'], (0,0)) 

            self.mouse_pos = pygame.mouse.get_pos()
            
            # we subtract self.scroll to see how far we are away from the player - we divide by 30 so the camera moves slower as it approaches the player
            self.scroll[0] += (self.camera_rect.centerx - self.display.get_width() / 2 - self.scroll[0]) / 60 # subtract width / 2 because we want the player in the middle
            self.scroll[1] += (self.camera_rect.centery - self.display.get_height() / 2 - self.scroll[1]) / 60 # subtract width / 2 because we want the player in the middle

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            #self.clouds.update()
            #self.clouds.render(surf=self.display, offset=render_scroll)

            self.tilemap.render(surf=self.display, offset=render_scroll) #offset handles the camera position


            self.update_camera(movement=(self.movement_right - self.movement_left, self.movement_down - self.movement_up))
            

            self.camera_rect.x = pygame.mouse.get_pos()[0] - render_scroll[0] 

            self.camera_rect.y = pygame.mouse.get_pos()[1] - render_scroll[1]

            pygame.draw.rect(self.display, (240, 240, 240), self.camera_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.quit()
                    sys.exit()
                # user input
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.erase_block:
                        self.tilemap.tilemap[str(self.get_mouse_grid_pos()[0]) + ";" + str(self.get_mouse_grid_pos()[1])] = Tile(self.current_block, 1, self.get_mouse_grid_pos())
                    else:

                        self.tilemap.tilemap.pop(str(self.get_mouse_grid_pos()[0]) + ";" + str(self.get_mouse_grid_pos()[1]), None) 

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        if self.erase_block == False:
                            self.erase_block = True                       
                        elif self.erase_block == True:
                            self.erase_block = False
                    if event.key == pygame.K_1:
                        self.current_block = 'stone'
                    elif event.key == pygame.K_2:
                        self.current_block = 'grass'
                    



 
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.flip()    
            self.clock.tick(60)

if __name__ == "__main__":
    le = LevelEditor()
    le.run_game()


