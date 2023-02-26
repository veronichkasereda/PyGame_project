import os
import sys

import pygame

# Изображение не получится загрузить
# без предварительной инициализации pygame
pygame.init()
size = width, height = 600, 700
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    try:
        image = pygame.image.load(fullname)
    except pygame.error as Message:
        print(Message)
        raise SystemExit(Message)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Car(pygame.sprite.Sprite):
    def __init__(self, group, x, screen, f):
        super().__init__(group)
        self.image = load_image('data\gameover.png')
        self.rect = self.image.get_rect()
        self.x = x
        self.f = f
        self.copy_image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        if not f:
            self.copy_image = pygame.transform.flip(self.copy_image, True, False)
        if x > 0:
            screen.blit(self.copy_image, (0, 0))
        else:
            screen.blit(self.copy_image, (x, 0))


def game_over_main():
    running = True
    pygame.init()
    size = wight, height = 700, 450
    screen = pygame.display.set_mode(size)
    x = -600
    f = True
    all_sprites = pygame.sprite.Group()
    car = Car(all_sprites, x, screen, f)
    all_sprites.add(car)
    start = True
    while running:
        if x < 0:
            f = True
        if f:
            x += 10
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pass
            if event.type == pygame.K_SPACE:
                start = not start
        screen.fill((0, 0, 0))
        car = Car(all_sprites, x, screen, f)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    game_over_main()
