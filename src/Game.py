import pygame 
import sys
import os
from Entities import PhysicsEntity, Player
from Tilemap import Tilemap
from Clouds import Clouds
import utils

# CONSTANTS
BLACK = (0,0,0)
SKY_BLUE = (14, 219, 248)
SCREEN_HORIZONTAL = 640
SCREEN_VERTICAL = 480

# Classes
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Learning Pygame')

        self.screen = pygame.display.set_mode((SCREEN_HORIZONTAL, SCREEN_VERTICAL))
        self.display = pygame.Surface((SCREEN_HORIZONTAL //2, SCREEN_VERTICAL // 2)) # we use a display and render it onto the screen object in order to scale up the size of everything in the game

        self.clock = pygame.time.Clock()
        self.run = True 

        self.movement_right = 0
        self.movement_left = 0

     
        self.scroll = [0, 0] # camera - all we need to do is apply this scroll the positions of everything

        self.assets = {

                'decor': utils.load_images(os.path.join('tiles', 'decor')),
                'grass': utils.load_images(os.path.join('tiles', 'grass')), 
                'large_decor': utils.load_images(os.path.join('tiles', 'large_decor')),
                'stone': utils.load_images(os.path.join('tiles', 'stone')),
                'player': utils.load_image(os.path.join('entities', 'player.png')),
                'background': utils.load_image(os.path.join('background.png')),
                'clouds': utils.load_images(os.path.join('clouds')),
                'player/idle' : utils.Animation(utils.load_images(os.path.join('entities', 'player', 'idle')), img_duration=6 ),
                'player/run' : utils.Animation(utils.load_images(os.path.join('entities', 'player', 'run')), img_duration=4 ),

                'player/jump' : utils.Animation(utils.load_images(os.path.join('entities', 'player', 'jump')) ),

                'player/slide' : utils.Animation(utils.load_images(os.path.join('entities', 'player', 'slide')) ),

                'player/wall_slide' : utils.Animation(utils.load_images(os.path.join('entities', 'player', 'wall_slide')) ),


                }


        self.player = Player(self,[50,50], [8,15])

        self.tilemap = Tilemap(self)

        self.clouds = Clouds(self.assets['clouds'])
        

    def run_game(self):
        while self.run: 
            self.display.blit(self.assets['background'], (0,0)) 
            
            # we subtract self.scroll to see how far we are away from the player - we divide by 30 so the camera moves slower as it approaches the player
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30 # subtract width / 2 because we want the player in the middle
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30 # subtract width / 2 because we want the player in the middle

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            self.clouds.update()
            self.clouds.render(surf=self.display, offset=render_scroll)

            self.tilemap.render(surf=self.display, offset=render_scroll) #offset handles the camera position

            self.player.update(tilemap=self.tilemap, movement=(self.movement_right - self.movement_left, 0))
            self.player.render(surf=self.display, offset=render_scroll) 
            
            #print(self.tilemap.physics_rects_around(self.player.pos))


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.quit()
                    sys.exit()
                # user input
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement_left = 1
                    if event.key == pygame.K_RIGHT:
                        self.movement_right = 1
                    if event.key == pygame.K_SPACE:
                        self.player.velocity[1] = -3 # this is so much better than that other video ...
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement_left = 0
                    if event.key == pygame.K_RIGHT:
                        self.movement_right = 0
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))

            pygame.display.flip()    
            self.clock.tick(60)

if __name__ == "__main__":
    g = Game()
    g.run_game()


