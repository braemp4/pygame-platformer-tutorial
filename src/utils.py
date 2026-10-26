import pygame 
from pathlib import Path
import os 

# CONSTANTS
ASSETS_DIR = Path(Path(__file__).resolve().parents[1], 'data')
IMG_DIR = os.path.join(ASSETS_DIR, 'images')
print(IMG_DIR)

BLACK = (0,0,0)

def load_image(path):
    img = pygame.image.load(os.path.join(IMG_DIR, path)).convert()
    img.set_colorkey(BLACK)
    return img

def load_images(path):
    images = []

    for img_name in os.listdir(os.path.join(IMG_DIR, path)):
        images.append(load_image(os.path.join(path, img_name)))
    
    return images

class Animation:
    def __init__(self, images, img_duration=5, loop=True):
        '''
        image duration is how many frames a single image of the animation should show for
        '''
        self.images = images 
        self.img_duration = img_duration
        self.loop = loop 
        self.done = False
        self.frame = 0 

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):

        # we want to do frame +=1 but carefully
        if self.loop:
            self.frame = (self.frame+1) % (self.img_duration * len(self.images)) # modulo forces the frame to loop, once it reaches the max it will go back to zero

        else: 
            # we do +=1 with a minumum statement - no need to go back to zero
            self.frame = min(self.frame + 1, self.img_duration* len(self.images) - 1) # we need to subtract 1 here - in the othercase modulo takes care of this by going back to zero

            # why multiply by len(images) to image duration 
            # if we have a 5 image animation, and the image duration is 20, we should have a 5x20 = 100 frame long animation

            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True 

        print(self.frame)

    def img(self):
        '''
        get current image of the animation
        '''
        
        return self.images[int(self.frame / self.img_duration)] # we divide by image duration because we only show the next image after the duration has passed - for example if img dur = 5 and we are on frame 0, every query will return image[0] until we reach 5 frames, then we get image[1]
