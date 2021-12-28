import pygame
import os



# Import sprites
SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]

LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

SCREEN_WIDTH = 1100

class Obstacle:
    def __init__(self, img, number_of_cactus):
        self._image = img
        self._type = number_of_cactus
        self._rect = self._image[self._type].get_rect()
        self._rect.x = SCREEN_WIDTH

    def update(self, speed):
        self._rect.x -= speed
        if self._rect.x < -self._rect.width:
            return True
        return False

    def draw(self, screen):
        screen.blit(self._image[self._type], self._rect)

    def get_rect(self):
        return self._rect


class SmallCactus(Obstacle):
    def __init__(self, image, number_of_cactus):
        super().__init__(image, number_of_cactus)
        self._rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image, number_of_cactus):
        super().__init__(image, number_of_cactus)
        self._rect.y = 300
