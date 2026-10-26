import pygame 

# CONSTANTS
GRAV_ACCELERATION = 0.1

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type 
        # pos = (x,y)
        self.pos = pos.copy() # why copy? lists are also objects, so if we spawn two things in the same place, their position will point to the same spot in memory. If we change this position, everything we placed at that spot will move.
        self.size = size
        self.velocity = [0, 0]

        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

        self.action = ''
        self.anim_offset = (-3, -3) # we need padding because different drawings will give frames different dimensions - deals with hitbox issues
        self.flip = False
        self.set_action('idle') # set action to idle by default - if we dont do this, we create a new animation object each time which always inits with frame = 0
    
    def rect(self):
        '''
        we want to create the rect dynamically because this physics entity will be moving
        '''
        return pygame.Rect(*self.pos, *self.size)

    def set_action(self, action):
        # only do this if the action has changed!
        if action != self.action:
            self.action = action 
            self.animation = self.game.assets[self.type + "/" + action].copy()

    def update(self, tilemap, movement=(0,0)):

        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False} # reset collisions every frame
        #frame_movement = (x,y)
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
       
        self.pos[0] += frame_movement[0] # update x coord
        entity_rect = self.rect()

        # handle horizontal collisions
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0: # if we are moving right
                    # make the right edge of the entity snap to the left edge of the tile
                    entity_rect.right = rect.left # WHAT headbuss I didnt know about this
                    self.collisions['right'] = True
                if frame_movement[0] < 0: # if moving left
                    # make the left edge of the entity snap to the right edge of the tile
                    entity_rect.left = rect.right 
                    self.collisions['left'] = True
                # we can't forget to update the players formal position attribute - otherwise the actual player will not move (I think)
                self.pos[0] = entity_rect.x 
            
        
        self.pos[1] += frame_movement[1] # update y coord
        # handle vertical collisions
        entity_rect = self.rect() # we need to make another rect - handle collisions 'twice' per frame

        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0: # if we are moving down
                    entity_rect.bottom = rect.top 
                    self.collisions['down'] = True
                    #self.velocity[1] = 0 # stop accelerating downwards
                if frame_movement[1] < 0: # if moving up
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y
        

        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0: # if we are moving right
                    # make the right edge of the entity snap to the left edge of the tile
                    entity_rect.right = rect.left # WHAT headbuss I didnt know about this
                if frame_movement[0] < 0: # if moving left
                    # make the left edge of the entity snap to the right edge of the tile
                    entity_rect.left = rect.right 
                # we can't forget to update the players formal position attribute - otherwise the actual player will not move (I think)
                self.pos[0] = entity_rect.x 
        
        # flip player if facing right or left
        if movement[0] <0:
            self.flip = True
        if movement[0] > 0:
            self.flip = False


        #add 0.1 to downward velocity until we reach 5 downward velocity
        self.velocity[1] = min(5,self.velocity[1] + GRAV_ACCELERATION) #type: ignore 

        if self.collisions['down'] or self.collisions['up']:
            # this will also prevent us from jumping through ceilings
            self.velocity[1] = 0


        # animations get updated within the update function
        self.animation.update()


    def render(self, surf, offset):
        # I feel like we don't need to pass surf to this function because screen is pretty much unchanging.
        #surf.blit(self.game.assets[self.type], (self.pos[0] - offset[0], self.pos[1] - offset[1]))
        surf.blit( pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]) )


class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0

    def update(self, tilemap, movement=(0,0)):
       super().update(tilemap, movement=movement)

       self.air_time +=1 

       if self.collisions['down']:
           self.air_time = 0

       if self.air_time > 4:
           self.set_action('jump') 
       elif movement[0] !=0:
           self.set_action('run')
       else:
           self.set_action('idle')
            

