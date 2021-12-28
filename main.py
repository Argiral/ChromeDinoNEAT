import math

import neat
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
    ge.pop(index)
    nets.pop(index)


def distance(pos_a, pos_b):
    dx = pos_a[0] - pos_b[0]
    dy = pos_a[1] - pos_b[1]
    return math.sqrt(dx ** 2 + dy ** 2)


def eval_genomes(genomes, config):
    global game_speed, x_pos_bg, y_pos_bg, points, dinosaurs, obstacles, ge, nets, points
    clock = pygame.time.Clock()
    points = 0

    obstacles = []
    dinosaurs = []
    ge = []
    nets = []

    x_pos_bg = 0
    y_pos_bg = 380
    game_speed = 20

    # Init genomes
    for genome_id, genome in genomes:
        dinosaurs.append(Dinosaur())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

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

        # If no dinosaurs remains, stop
        if len(dinosaurs) == 0:
            break

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
            if obstacle.update(game_speed):
                obstacles.remove(obstacle)
            # Check collision
            for i, dinosaur in enumerate(dinosaurs):
                if dinosaur.rect.colliderect(obstacle.get_rect()):
                    # decrease fitness of dinosaur colliding with object
                    ge[i].fitness -= 1
                    remove(i)

        # Set jump when pressing spacebar
        for i, dinosaur in enumerate(dinosaurs):
            # Activare nn using position and distance to next obstacle
            output = nets[i].activate((dinosaur.rect.y,
                                       distance((dinosaur.rect.x, dinosaur.rect.y),
                                                obstacles[0].get_rect().midtop)))
            if output[0] > 0.5 and dinosaur.rect.y == dinosaur.Y_POS:
                dinosaur.dino_jump = True
                dinosaur.dino_run = False


        score()
        background()
        clock.tick(30)
        pygame.display.update()

# Setup NEAT
def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)
    pop.run(eval_genomes, 50)


if __name__ == '__main__':
    global game_speed
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)

# main()
# pygame.quit()
# sys.exit()
