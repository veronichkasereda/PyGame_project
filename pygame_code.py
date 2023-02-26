from game_over import *
from widget_run import *
import pygame

# from datetime import datetime

pygame.init()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Красная шапочка')
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

FPS = 60


def terminate():
    pygame.quit()
    sys.exit()


# запуск стартового окна
def start_screen():
    intro_text = ["", "", "",
                  "ЦЕЛЬ ИГРЫ -", "Дойти до домика бабушки",
                  "Правила игры:",
                  "На пути вашего персонажа могут всстретиться преграды.",
                  "Ваша задача - не провалиться в ямы, обойти",
                  "деревья и добраться до бабушки максимально быстро",
                  "Для начала игры нажмите на любую клавишу. Удачи!"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


# запуск финального окна
def finish_screen():
    intro_text = ["", "", "", "", "",
                  "Вы дошли до конца!", "",
                  "Ваш рекорд:", "",
                  "Текущий результат:"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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


title_images = {
    'wall': load_image('tree.png'),
    'grass': load_image('grass.png'),
    'hero': load_image('masha.png'),
    'empty': load_image('fon.jpg'),
    'home': load_image('home.png'),
    'pit': load_image('pit.png')
}


# загрузка уровня
def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_width = tile_height = 50
tile_images = {
    'wall': load_image('tree.png'),
    'grass': load_image('grass.png'),
    'home': load_image('home.png'),
    'pit': load_image('pit.png')
}
player_image = load_image('masha.png')


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0] + 15, tile_height * self.pos[1] + 5)


player = None


# 'распаковка' уровня
def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('grass', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '-':
                Tile('pit', x, y)
            elif level[y][x] == '|':
                Tile('home', x, y)
            elif level[y][x] == '@':
                Tile('grass', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


level_map = load_level('Карта')
hero, max_x, max_y = generate_level(level_map)


def move(hero, moves):
    x, y = hero.pos
    if moves == 'up':
        if y > 0 and level_map[y - 1][x] == '.':
            hero.move(x, y - 1)
            return True
        if level_map[y - 1][x] == '-':
            # проигрышь при попадании в яму
            hero.move(x, y - 1)
            game_over()
            return False
        if level_map[y - 1][x] == '|':
            # победа при попадании домой
            hero.move(x, y - 1)
            #            time(datetime.now().time())
            game_win()
    if moves == 'down':
        if y < max_y and level_map[y + 1][x] == '.':
            hero.move(x, y + 1)
            return True
        if level_map[y + 1][x] == '-':
            hero.move(x, y + 1)
            game_over()
            return False
        if level_map[y + 1][x] == '|':
            hero.move(x, y + 1)
            #            time(datetime.now().time())
            game_win()
    if moves == 'left':
        if y > 0 and level_map[y][x - 1] == '.':
            hero.move(x - 1, y)
            return True
        if level_map[y][x - 1] == '-':
            hero.move(x - 1, y)
            game_over()
            return False
        if level_map[y][x - 1] == '|':
            hero.move(x - 1, y)
            #            time(datetime.now().time())
            game_win()
    if moves == 'right':
        if y < max_y and level_map[y][x + 1] == '.':
            hero.move(x + 1, y)
            return True
        if level_map[y][x + 1] == '-':
            hero.move(x + 1, y)
            game_over()
            return False
        if level_map[y][x + 1] == '|':
            hero.move(x + 1, y)
            #            time(datetime.now().time())
            game_win()


# вызов заставки проигрыша
def game_over():
    game_over_main()


# вызов заставки выигрыша
def game_win():
    finish_screen()


# def time(times):
#    values = []
#    values.append(times)


def main():
    start_screen()
    level_map = load_level('Карта')
    hero, max_x, max_y = generate_level(level_map)
    running = True
    pygame.init()
    size = wight, height = 600, 600
    screen = pygame.display.set_mode(size)
    #    time(datetime.now().time())
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #                time(datetime.now().time())
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    running = move(hero, 'up')
                elif event.key == pygame.K_DOWN:
                    running = move(hero, 'down')
                elif event.key == pygame.K_LEFT:
                    running = move(hero, 'left')
                elif event.key == pygame.K_RIGHT:
                    running = move(hero, 'right')

        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(15)
    pygame.quit()


if __name__ == '__main__':
    main()
