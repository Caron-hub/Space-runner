"""Graphics from:
https://opengameart.org/content/space-parallax-background
https://opengameart.org/content/space-ship-construction-kit
https://www.fontspace.com/heaven-castro/pixel-miners"""

import random
import pygame
# Global colors
WHITE = (255, 255, 255)


def pre_spawn_enemies():
    global enemy_list
    enemy_list = pygame.sprite.Group()
    for i in range(8):
        # Create objects
        enemy1 = Enemy()
        # Add sprites to lists
        enemy_list.add(enemy1)
        all_sprites_list.add(enemy1)


def spawn_player():
    global player
    player = Player()
    all_sprites_list.add(player)


def load_images():
    """Load images and return them as a dictionary."""
    image_dict = {
        "player": pygame.image.load("graphics/player.png").convert_alpha(),
        "background": pygame.image.load("graphics/Parallax.png").convert(),
        "enemy1": pygame.image.load("graphics/enemy1.png").convert_alpha(),
        }
    return image_dict


class Player(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.image = image_dict["player"]
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 400
        self.life = 3


class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.image = image_dict["enemy1"]
        # 50x54 pixels
        self.rect = self.image.get_rect()
        self.spawn()

    def spawn(self):
            self.rect.y = random.randrange(-904, -54, 100)
            self.rect.x = random.randrange(0, screen_width - 99, 100)

    def update(self):
        self.rect.y += game_speed
        if self.rect.y > screen_height:
            self.spawn()


class Background:
    def __init__(self):
        self.bg_image = image_dict["background"]
        self.bg1_y = 0
        self.bg2_y = -500
        self.moving_speed = 2

    def render(self):

        screen.blit(self.bg_image, [0, self.bg1_y])
        screen.blit(self.bg_image, [0, self.bg2_y])

    def move(self):
        self.bg1_y += self.moving_speed
        self.bg2_y += self.moving_speed

        if self.bg1_y == 500:
            self.bg1_y = -500
        if self.bg2_y == 500:
            self.bg2_y = -500


def main():
    global screen, image_dict, game_speed, screen_width, screen_height, all_sprites_list
    # --------------- Initialize game engine -----------------
    pygame.init()
    # WINDOW size and other
    screen_height = 500
    screen_width = 500
    screen = pygame.display.set_mode([screen_width, screen_height])
    pygame.display.set_caption("Space Runner")
    score = 0
    clock_counter = 0
    game_speed = 5

    # Text

    # Select the font to use, size, bold, italics
    font = pygame.font.Font('graphics/PixelMiners.otf', 15)

    # Loading all needed images once
    image_dict = load_images()

    background = Background()
    clock = pygame.time.Clock()

    all_sprites_list = pygame.sprite.Group()
    pre_spawn_enemies()
    spawn_player()
    # Main game loop
    done = False
    while not done:
        # ------------- Main event loop --------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # Player movement
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.rect.x -= 100
                    if player.rect.x < 0:
                        player.rect.x = 0
                elif event.key == pygame.K_RIGHT:
                    player.rect.x += 100
                    if player.rect.x > 400:
                        player.rect.x = 400
                elif event.key == pygame.K_UP:
                    player.rect.y -= 100
                    if player.rect.y < 0:
                        player.rect.y = 0
                elif event.key == pygame.K_DOWN:
                    player.rect.y += 100
                    if player.rect.y > 400:
                        player.rect.y = 400
        # ------------ LOGIC -------------
        enemy_list.update()

        # See if the player has collided with anything.
        enemies_hit_list = pygame.sprite.spritecollide(player, enemy_list, False)

        # Decrease life
        for enemy in enemies_hit_list:
            player.life -= 1
            enemy.spawn()
        if player.life == 0:
            done = True

        if clock_counter % 30 == 0:
            score += 1
        # Speed up game every 10 seconds
        if clock_counter % 300 == 0:
                game_speed += 1
        clock_counter += 1
        # ------------- DRAWING --------------
        # Background
        background.render()
        background.move()

        # Player and enemies
        all_sprites_list.draw(screen)

        # Score display
        # Create image of the letters
        score_text = font.render("Score:    " + str(score), True, WHITE)
        screen.blit(score_text, [390, 480])
        life_text = font.render("Lives:    " + str(player.life), True, WHITE)
        screen.blit(life_text, [10, 480])
        # flipping the screen
        pygame.display.flip()
        clock.tick(30)
    # Close the window.
    pygame.quit()


# Call the main function if file is run.
if __name__ == "__main__":
    main()
