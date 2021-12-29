import math
import numpy as np
from scipy.signal import convolve2d

import neat
import pygame
import os
import random
import sys

from dinosaur import Dinosaur
from obstacle import SmallCactus, LargeCactus, Bird, SMALL_CACTUS, LARGE_CACTUS, BIRD

# Init pygame
pygame.init()

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


BG = pygame.image.load((os.path.join("Assets/Other", "Track.png")))

FONT = pygame.font.Font("freesansbold.ttf", 20)


global game_speed, obstacles, dinosaurs, pop

max_score = 0


def remove(index):
    dinosaurs.pop(index)
    ge.pop(index)
    nets.pop(index)


def distance(pos_a, pos_b):
    dx = pos_a[0] - pos_b[0]
    dy = pos_a[1] - pos_b[1]
    return math.sqrt(dx ** 2 + dy ** 2)


# # kernel = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
# kernel = np.ones((5, 5))
#
#
# def prepare_img(img):
#     return convolve2d(img, kernel, mode='valid')[::5, ::5]

def eval_genomes(genomes, config):
    global game_speed, x_pos_bg, y_pos_bg, points, dinosaurs, obstacles, ge, nets, points, last_killed
    clock = pygame.time.Clock()
    points = 0
    max_score = 0
    last_killed = 0

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

    # Print stats
    def score():
        global points, game_speed, max_score, last_killed
        points += 1
        last_killed += 1
        max_score = max(points, max_score)
        if points % 100 == 0:
            game_speed += 1
        # Increase fitness of survived dinos
        if points % 50 == 0:
            for i in range(len(ge)):
                ge[i].fitness += 1
        # Points
        text = FONT.render(f'Points: {str(points)}', True, (0, 0, 0))
        SCREEN.blit(text, (950, 50))
        # Population number
        text_m_score =  FONT.render(f'Max score: {max_score}', True, (0, 0, 0))
        SCREEN.blit(text_m_score, (20, 50))
        # Nb. dinosaurs
        text_dino = FONT.render(f'Nb. dinosaurs: {len(dinosaurs)}', True, (0, 0, 0))
        SCREEN.blit(text_dino, (20, 450))
        # Population number
        text_popu = FONT.render(f'Generation: {pop.generation}', True, (0, 0, 0))
        SCREEN.blit(text_popu, (20, 475))

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
    running = True
    while running:
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
            dinosaur.draw(SCREEN, obstacles)

        # If no dinosaurs remains, stop
        if len(dinosaurs) == 0:
            break

        # Randomly generate obstacles
        if len(obstacles) == 0:
            new_ob_type = random.randint(0, 3)
            if new_ob_type == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS, random.randint(0, 2)))
            elif new_ob_type == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS, random.randint(0, 2)))
            elif new_ob_type == 2:
                obstacles.append(Bird(BIRD, random.randint(0, 1), height=0))
            elif new_ob_type == 2:
                obstacles.append(Bird(BIRD, random.randint(0, 1), height=1))

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

        # Activate dinosaurs
        for i, dinosaur in enumerate(dinosaurs):
            # Activate nn using position, distance to next obstacle, height of next obstacle, and speed
            dist = distance((dinosaur.rect.x, dinosaur.rect.y), obstacles[0].get_rect().midtop) if len(obstacles) > 0 else np.inf
            height =  obstacles[0].get_rect().y if len(obstacles) > 0 else np.inf
            output = nets[i].activate((dinosaur.rect.y, dist, height, game_speed))
            if output[0] > 0.5 and dinosaur.rect.y == dinosaur.Y_POS:
                dinosaur.dino_jump = True
                dinosaur.dino_run = False

        keyState = pygame.key.get_pressed()
        if last_killed > 5 and keyState[pygame.K_k]:
            # Kill a random dinosaur
            i = random.randint(0, len(dinosaurs) - 1)
            ge[i].fitness -= 1
            remove(i)
            last_killed = 0

        score()
        background()
        clock.tick(30)
        pygame.display.update()


# Setup NEAT
def run(config_path):
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)
    pop.run(eval_genomes, 50)

    print(pop.best_genome)


if __name__ == '__main__':
    global game_speed
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
