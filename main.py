import sys
import os

import pygame

filename = ''


def terminate():
    pygame.quit()
    sys.exit()


FPS = 50
WIDTH, HEIGHT = 1920, 1020
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Робинзон')
clock = pygame.time.Clock()
score = 0
victory = False
dead = False
game_over = False


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def game_over_screen(score):
    intro_text = ["SCORE: ",
                  str(score)]
    if game_over:
        fon = pygame.transform.scale(load_image('final.png'), (WIDTH, HEIGHT))
    if dead:
        fon = pygame.transform.scale(load_image('финал.png'), (WIDTH, HEIGHT))
    if victory:
        fon = pygame.transform.scale(load_image('win.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 10
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 20
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    global filename
    intro_text = ["ЗАСТАВКА",
                  "Правила игры:",
                  "Забрать сундук быстрее противника",
                  "Шипы вас убивают"]

    fon = pygame.transform.scale(load_image('photo_2025-02-15_16-50-49.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
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
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if 790 < event.pos[0] < 1095 and 400 < event.pos[1] < 475:
                    filename = 'map.txt'
                    return
                elif 780 < event.pos[0] < 1095 and 500 < event.pos[1] < 580:
                    filename = 'map2.txt'
                    return
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


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
        self.pos = pos_x, pos_y

    def move(self, x, y):
        self.pos = x, y
        self.rect = self.image.get_rect().move(tile_width * x + 15, tile_height * y + 5)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(enemy_group, all_sprites)
        self.image = enemy_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = pos_x, pos_y

    def move(self, x, y):
        self.pos = x, y
        self.rect = self.image.get_rect().move(tile_width * x + 15, tile_height * y + 5)


def generate_level(level):
    new_enemy, new_player, x, y = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == ';':
                Tile('water', x, y)
            elif level[y][x] == 'P':
                Tile('palka', x, y)
            elif level[y][x] == 'W':
                Tile('koster', x, y)
            elif level[y][x] == 'C':
                Tile('chest', x, y)
            elif level[y][x] == 'S':
                Tile('spikes', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == 'E':
                Tile('empty', x, y)
                new_enemy = Enemy(x, y)
    return new_enemy, new_player, x, y


def move(obj, direction):
    global score
    global dead
    global victory
    global game_over
    x, y = obj.pos
    if obj == player:
        score += 1

    if direction == 'left' and x > 0 and level[y][x - 1] == 'C':
        obj.move(x - 1, y)
        if obj == player:
            score += 1
            victory = True
        else:
            game_over = True
            score = 0
    if direction == 'right' and x < level_x and level[y][x + 1] == 'C':
        obj.move(x - 1, y)
        if obj == player:
            score += 1
            victory = True
        else:
            game_over = True
            score = 0
    if direction == 'up' and y > 0 and level[y - 1][x] == 'C':
        obj.move(x - 1, y)
        if obj == player:
            score += 1
            victory = True
        else:
            game_over = True
            score = 0
    if direction == 'down' and y < level_y and level[y + 1][x] == 'C':
        obj.move(x - 1, y)
        if obj == player:
            score += 1
            victory = True
        else:
            game_over = True
            score = 0

    if obj == player and direction == 'left' and x > 0 and level[y][x - 1] == 'S':
        obj.move(x - 1, y)
        dead = True
        score = 0
    if obj == player and direction == 'right' and x < level_x and level[y][x + 1] == 'S':
        obj.move(x - 1, y)
        dead = True
        score = 0
    if obj == player and direction == 'up' and y > 0 and level[y - 1][x] == 'S':
        obj.move(x - 1, y)
        dead = True
        score = 0
    if obj == player and direction == 'down' and y < level_y and level[y + 1][x] == 'S':
        obj.move(x - 1, y)
        dead = True
        score = 0

    if direction == 'left' and x > 0 and level[y][x - 1] != '#' and level[y][x - 1] != ';' and level[y][x - 1] != 'W':
        obj.move(x - 1, y)
    if direction == 'right' and x < level_x and level[y][x + 1] != '#' and level[y][x + 1] != ';' and level[y][
        x + 1] != 'W':
        obj.move(x + 1, y)
    if direction == 'up' and y > 0 and level[y - 1][x] != '#' and level[y - 1][x] != ';' and level[y - 1][x] != 'W':
        obj.move(x, y - 1)
    if direction == 'down' and y < level_y and level[y + 1][x] != '#' and level[y + 1][x] != ';' and level[y + 1][
        x] != 'W':
        obj.move(x, y + 1)


start_screen()
player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
tile_images = {
    'wall': load_image('камень2.png'),
    'empty': load_image('песок50.png'),
    'water': load_image('вода.png'),
    'palka': load_image('доска.png'),
    'koster': load_image('костер.png'),
    'chest': load_image('chest.png'),
    'spikes': load_image('spikes.png')
}
player_image = load_image('human.png', -1)
enemy_image = load_image('enemy.png', -1)

tile_width = tile_height = 50
level = load_level(filename)
enemy, player, level_x, level_y = generate_level(level)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move(player, 'left')
                if score <= 9 or (10 < score <= 14) or (15 < score <= 21):
                    move(enemy, 'left')
                elif score == 10 or score == 22:
                    move(enemy, 'down')
                elif score == 15:
                    move(enemy, 'up')
            if event.key == pygame.K_RIGHT:
                move(player, 'right')
                if score <= 9 or (10 < score <= 14) or (15 < score <= 21):
                    move(enemy, 'left')
                elif score == 10 or score == 22:
                    move(enemy, 'down')
                elif score == 15:
                    move(enemy, 'up')
            if event.key == pygame.K_UP:
                move(player, 'up')
                if score <= 9 or (10 < score <= 14) or (15 < score <= 21):
                    move(enemy, 'left')
                elif score == 10 or score == 22:
                    move(enemy, 'down')
                elif score == 15:
                    move(enemy, 'up')
            if event.key == pygame.K_DOWN:
                move(player, 'down')
                if score <= 9 or (10 < score <= 14) or (15 < score <= 21):
                    move(enemy, 'left')
                elif score == 10 or score == 22:
                    move(enemy, 'down')
                elif score == 15:
                    move(enemy, 'up')
            if event.key == pygame.K_ESCAPE:
                terminate()
    if game_over or victory or dead:
        game_over_screen(score)
    screen.fill('black')
    tiles_group.draw(screen)
    enemy_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
