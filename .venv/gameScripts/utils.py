import os
import pygame

BASE_IMG_PATH = ".venv/images/"

def load_image(path) -> pygame.Surface:
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path) -> list:
    images = []
    for imgName in os.listdir(BASE_IMG_PATH + path):
        images.append(load_image(path + '/' + imgName))
    return images

class Animation:
    def __init__(self, images, img_duration = 5, loop = True) -> None:
        self.images = images
        self.image_duration = img_duration
        self.loop = loop
        self.done = False
        self.frame = 0
    
    def copy(self):
        return Animation(self.images, self.image_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.image_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.image_duration * len(self.images) - 1)
            if self.frame >= self.image_duration * len(self.images) - 1:
                self.done = True

    def image(self):
        return self.images[int(self.frame / self.image_duration)]
