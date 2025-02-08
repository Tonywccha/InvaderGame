import pygame
import random

# --- Global constants ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500

NUMBER_OF_BLOCKS_COL = 11
NUMBER_OF_BLOCKS_ROW = 5
SPACE_BETWEEN_BLOCKS = 15

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
        self.image = pygame.Surface([20, 20])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()


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

class Player(pygame.sprite.Sprite):
    """ This class represents the player. """

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.y = 480

    def update(self):
        """ Update the player location. """
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]


class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([4, 10])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        self.rect.y -= 3


class Game(object):
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """

    def __init__(self):
        """ Constructor. Create all our attributes and initialize
        the game. """

        self.score = 0
        self.game_over = False

        # Create sprite lists
        self.block_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()

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
                    bullet.rect.x = self.player.rect.x
                    bullet.rect.y = self.player.rect.y
                    # Add the bullet to the lists
                    self.all_sprites_list.add(bullet)
                    self.bullet_list.add(bullet)

        return False

    def run_logic(self):
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

            # See if the player block has collided with anything.
            # blocks_hit_list = pygame.sprite.spritecollide(self.player, self.block_list, True)

            for bullet in self.bullet_list:
                # See if it hit a block
                block_hit_list = pygame.sprite.spritecollide(bullet, self.block_list, True)

                # For each block hit, remove the bullet and add to the score
                for block in block_hit_list:
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

    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.fill(BLACK)

        if self.game_over:
            # font = pygame.font.Font("Serif", 25)
            font = pygame.font.SysFont("serif", 25)
            text = font.render("Game Over, click to restart", True, WHITE)
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
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("My Game")
    pygame.mouse.set_visible(False)

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
        game.run_logic()

        # Draw the current frame
        game.display_frame(screen)

        # Pause for the next frame
        clock.tick(60)

    # Close window and exit
    pygame.quit()


# Call the main function, start up the game
if __name__ == "__main__":
    main()
