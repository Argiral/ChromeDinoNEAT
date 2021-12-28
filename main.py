import pygame
import os
import random
import sys

from dinosaur import Dinosaur
from obstacle import SmallCactus, LargeCactus, SMALL_CACTUS, LARGE_CACTUS

# Init pygame
pygame.init()

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


BG = pygame.image.load((os.path.join("Assets/Other", "Track.png")))

FONT = pygame.font.Font("freesansbold.ttf", 20)


global game_speed, obstacles, dinosaurs


def remove(index):
    dinosaurs.pop(index)


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, dinosaurs, obstacles
    clock = pygame.time.Clock()
    points = 0

    obstacles = []
    dinosaurs = [Dinosaur()]

    x_pos_bg = 0
    y_pos_bg = 380
    game_speed = 20

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        text = FONT.render(f'Points: {str(points)}', True, (0, 0, 0))
        SCREEN.blit(text, (950, 50))

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        # Plot 2 bg
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed

    # Main game loop
    run = True
    while run:
        # Check exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Paint screen
        SCREEN.fill((255, 255, 255))

        # Update game
        for dinosaur in dinosaurs:
            dinosaur.update()
            dinosaur.draw(SCREEN)

        # Randomly generate obstacles
        if len(obstacles) == 0:
            new_ob_type = random.randint(0, 1)
            if new_ob_type == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS, random.randint(0, 2)))
            elif new_ob_type == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS, random.randint(0, 2)))

        # Update and draw obstacles
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            # Check collision
            for i, dinosaur in enumerate(dinosaurs):
                if dinosaur.rect.colliderect(obstacle.get_rect()):
                    remove(i)

        # Get user input
        user_input = pygame.key.get_pressed()

        # Set jump when pressing spacebar
        for i, dinosaur in enumerate(dinosaurs):
            if user_input[pygame.K_SPACE]:
                dinosaur.dino_jump = True
                dinosaur.dino_run = False

        # If no dinosaurs remains, stop
        if len(dinosaurs) == 0:
            break

        score()
        background()
        clock.tick(30)
        pygame.display.update()


main()
pygame.quit()
sys.exit()
