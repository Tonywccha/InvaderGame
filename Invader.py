'''A classic invader shooting game'''


import random
import time
import pygame

# --- Global constants ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 780

HEART_POSITION_X = 10
HEART_POSITION_Y = 10
NUMBER_OF_HEART = 5

NUMBER_OF_BLOCKS_COL = 11
NUMBER_OF_BLOCKS_ROW = 5
SPACE_BETWEEN_BLOCKS = 15

INVADERBULLETCHANCE = 5
HIT_DELAY=0.05

global VX
global VXX
VXX = False
VX = 1

# --- Classes ---


class Block(pygame.sprite.Sprite):
    """ This class represents a simple block the player collects. """

    def __init__(self):
        """ Constructor, create the image of the block. """
        super().__init__()
        #self.image = pygame.Surface([20, 20])
        #self.image.fill(WHITE)
        #self.rect = self.image.get_rect()
        self.image1 = pygame.image.load("goose1-45px.png")
        self.image2 = pygame.image.load("goose2-45px.png")
        self.image3 = pygame.image.load("goose3-45px.png")
        self.imagehit = pygame.image.load("explode.png")
        self.image=self.image1
        self.imageindex=1
        self.imagedirection='R'
        self.rect = self.image.get_rect()

    def hit(self):
        '''change the sprite image to an explode image'''
        self.image=self.imagehit

    def swapimage(self):
        '''animated sprite image'''
        if self.imageindex==1:
            self.image=self.image2
            self.imageindex=2
        elif self.imageindex==2:
            self.image=self.image3
            self.imageindex=3
        else:
            self.image=self.image1
            self.imageindex=1

    def flipimage(self):
        '''flip sprite image to keep the face consistent to moving direction'''
        if self.imagedirection=='R':
            self.imagedirection='L'
        else:
            self.imagedirection='R'
        self.image1=pygame.transform.flip(self.image1,True,False)
        self.image2=pygame.transform.flip(self.image2,True,False)
        self.image3=pygame.transform.flip(self.image3,True,False)


    def update(self):
        """ Automatically called when we need to move the block. """
        global VX
        global VXX
        if self.rect.x+VX >= SCREEN_WIDTH - self.rect.w:
            VXX = True
            #self.rect.x += VX
            #VX *= -1
        elif self.rect.x+VX <= 0:
            VXX = True
            #self.rect.x += VX
        #else:
        self.rect.x += VX
        if self.rect.x % 7 == 3:
            self.swapimage()



class Player(pygame.sprite.Sprite):
    """ This class represents the player. """

    def __init__(self):
        super().__init__()
        #self.image = pygame.Surface([20, 20])
        #self.image.fill(GREEN)
        self.image = pygame.image.load("hunter.png")
        self.rect = self.image.get_rect()
        self.rect.y = SCREEN_HEIGHT-self.rect.h

    def update(self):
        """ Update the player location. """
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]


class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
        #self.image = pygame.Surface([4, 10])
        #self.image.fill(GREEN)
        self.image = pygame.image.load("greenbolt.png")
        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        self.rect.y -= 3

class InvaderBullet(Bullet):
    """ This class represents the bullets from the invaders and it is a sub-class of Bullet"""
    def __init__(self):
        super().__init__()
        #self.image.fill(RED)
        self.image = pygame.image.load("pooemoji.png")
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += 3

class Heart(pygame.sprite.Sprite):
    """ This class represents the life left . """

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.image = pygame.image.load("heart.png")
        self.rect = self.image.get_rect()


class Game(object):
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """

    def __init__(self):
        """ Constructor. Create all our attributes and initialize
        the game. """

        self.score = 0
        self.game_over = False
        self.game_over_msg ='Game Over!'
        self.life=NUMBER_OF_HEART
        global VX, VXX
        VXX = False
        VX = 1

        # Create sprite lists
        self.block_list = pygame.sprite.Group()
        self.block_hit_group = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()
        self.invaderbullet_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        self.heart_list=[]

        for i in range(self.life):
            heart=Heart()
            heart.rect.x = HEART_POSITION_X + i * heart.rect.w + 10
            heart.rect.y = HEART_POSITION_Y
            self.heart_list.append(heart)
            self.all_sprites_list.add(heart)



        # Create the block sprites`
        for col in range(NUMBER_OF_BLOCKS_COL):
            for row in range(NUMBER_OF_BLOCKS_ROW):
                block = Block()

                block.rect.x = (SCREEN_WIDTH / 2) - (NUMBER_OF_BLOCKS_COL * block.rect.w / 2 + NUMBER_OF_BLOCKS_COL / 2 * SPACE_BETWEEN_BLOCKS) + col * (block.rect.width + SPACE_BETWEEN_BLOCKS)

                block.rect.y = (SCREEN_HEIGHT / 2) - (NUMBER_OF_BLOCKS_ROW * block.rect.h / 2 + NUMBER_OF_BLOCKS_ROW / 2 * SPACE_BETWEEN_BLOCKS) + row * (block.rect.height + SPACE_BETWEEN_BLOCKS)

                self.block_list.add(block)
                self.all_sprites_list.add(block)

        # Create the player
        self.player = Player()
        self.all_sprites_list.add(self.player)

    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over:
                    self.__init__()
                else:
                    # Fire a bullet if the user clicks the mouse button
                    bullet = Bullet()
                    # Set the bullet so it is where the player is
                    bullet.rect.centerx=self.player.rect.centerx
                    bullet.rect.y = self.player.rect.y-bullet.rect.h
                    # Add the bullet to the lists
                    self.all_sprites_list.add(bullet)
                    self.bullet_list.add(bullet)

        return False

    def run_logic(self,screen):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        global  VX, VXX

        if not self.game_over:
            # Move all the sprites
            self.all_sprites_list.update()
            if VXX == True:
                VX *= -1
                VXX = False
                for block in self.block_list:
                    block.flipimage()

            # See if the player block has collided with anything.
            # blocks_hit_list = pygame.sprite.spritecollide(self.player, self.block_list, True)

            for bullet in self.bullet_list:
                # See if it hit a block
                block_hit_list = pygame.sprite.spritecollide(bullet, self.block_list, True)

                # For each block hit, remove the bullet and add to the score
                if len(block_hit_list)>0:
                    for block in block_hit_list:
                        block.hit()
                        self.block_hit_group.add(block)
                    self.block_hit_group.draw(screen)
                    pygame.display.flip()
                    time.sleep(HIT_DELAY)


                    for block in block_hit_list:
                        self.block_hit_group.remove(block)
                        self.bullet_list.remove(bullet)
                        self.all_sprites_list.remove(bullet)
                        self.score += 1
                        print(self.score)

                # Remove the bullet if it flies up off the screen
                if bullet.rect.y < -10:
                    self.bullet_list.remove(bullet)
                    self.all_sprites_list.remove(bullet)

            if len(self.block_list) == 0:
                self.game_over = True
                self.game_over_msg = 'Wow! You won!'
            else:
                #One random invader shoots a bullet if a random number > INVADERBULLETCHANCE
                if random.randrange(100)>(100-INVADERBULLETCHANCE):
                    invaderbullet=InvaderBullet()
                    randomblockindex = random.randrange(0, len(self.block_list))
                    randomblock:Block=None
                    i=0
                    for block in self.block_list:
                        i += 1
                        if i > randomblockindex:
                            randomblock=block
                            break
                    invaderbullet.rect.centerx=randomblock.rect.centerx
                    invaderbullet.rect.y=randomblock.rect.y+randomblock.rect.h
                    self.all_sprites_list.add(invaderbullet)
                    self.invaderbullet_list.add(invaderbullet)


                for invaderbullet in self.invaderbullet_list:
                    #Checks if any invader bullets hit the player
                    #block_hit_list = pygame.sprite.spritecollide(bullet, self.block_list, True)

                    #if hit the player, gameover

                    #Remove the invader bullet if it flies down off the screen
                    if invaderbullet.rect.y > SCREEN_HEIGHT:
                        self.invaderbullet_list.remove(invaderbullet)
                        self.all_sprites_list.remove(invaderbullet)

                invaderbullet_hit_list = pygame.sprite.spritecollide(self.player, self.invaderbullet_list, True)
                if len(invaderbullet_hit_list) > 0:
                    self.life -= 1
                    self.all_sprites_list.remove(self.heart_list[self.life])
                    #self.heart_list.remove(self.life)
                    if self.life ==0:
                        self.game_over = True



    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.fill(BLACK)

        if self.game_over:
            # font = pygame.font.Font("Serif", 25)
            font = pygame.font.SysFont("serif", 25)
            text = font.render(self.game_over_msg+" Click to restart", True, WHITE)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])

        if not self.game_over:
            self.all_sprites_list.draw(screen)

        pygame.display.flip()


def main():
    """ Main program function. """
    # Initialize Pygame and set up the window
    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)


    pygame.display.set_caption("My Game")
    pygame.mouse.set_visible(True)

    # Create our objects and set the data
    done = False
    clock = pygame.time.Clock()

    # Create an instance of the Game class
    game = Game()

    # Main game loop
    while not done:
        # Process events (keystrokes, mouse clicks, etc)
        done = game.process_events()

        # Update object positions, check for collisions
        game.run_logic(screen)

        # Draw the current frame
        game.display_frame(screen)

        # Pause for the next frame
        clock.tick(60)

    # Close window and exit
    pygame.quit()


# Call the main function, start up the game
if __name__ == "__main__":
    main()
