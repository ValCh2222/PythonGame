import pygame
from pygame.locals import *
import pickle
from os import path

pygame.init()
pause=False
clock = pygame.time.Clock()
fps = 60
game_over = 0
level=1
max_level=5
score=0
demention =1
script = False
screen_width = 1200
screen_height = 750
main_menu = True
list_of_items=False
number_of_lives=3
#define font
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

#define game variables
tile_size = 50

def reset_level(level):
    player.reset(100,screen.get_height()-130)
    blob_group.empty()
    ball_group.empty()
    platform_group.empty()
    lava_group.empty()
    exit_group.empty()
    scrypt_group.empty()
    stop_scrypt_group.empty()
    found_item_group.empty()
    with open(f'images/level{level}', 'r') as map_file:
        level_map = []
        for line in map_file:
            line = line.strip()
            for t in line:
                line.strip('1')
            level_map.append(line)

    world = World(level_map)
    return(world)
#load images
door_img=pygame.image.load('images/strelka.png')
door_img = pygame.transform.scale(door_img, (tile_size, tile_size))
bg_img = pygame.image.load('images/sky.jpeg')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
play_img = pygame.image.load('images/start.png')
play_img= pygame.transform.scale(play_img, (320, 80))
heart_img = pygame.image.load('images/heart.png')
heart_img= pygame.transform.scale(heart_img, (30, 30))
coin_img = pygame.image.load('images/coin.png')
coin_img= pygame.transform.scale(coin_img, (40, 80))
start_img=pygame.image.load('images/play.png')
start_img = pygame.transform.scale(start_img, (320,80))
exit_img=pygame.image.load('images/exit.png')
exit_img = pygame.transform.scale(exit_img, (320, 80))
chest_img=pygame.image.load('images/collection.png')
chest_img = pygame.transform.scale(chest_img, (320, 80))
back_img=pygame.image.load('images/back.png')
back_img = pygame.transform.scale(back_img, (80, 80))
pause_img=pygame.image.load('images/pause.png')
pause_img = pygame.transform.scale(pause_img, (80, 80))


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def show_lives():
    global number_of_lives
    show = 0
    x=100
    while show!=number_of_lives:
        screen.blit(heart_img, (x, 15))
        x+=40
        show+=1

def check_lives():
    global number_of_lives
    number_of_lives -=1
    if number_of_lives ==0 :
        game_over = -1
        return False
    else :
        return True


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        #draw button
        screen.blit(self.image, self.rect)

        return action
class Player():
    def __init__(self, x, y):
        self.number_of_jumpes=2
        #self.number_of_lives = number_of_lives
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 3):
            img_right = pygame.image.load(f'images/guy{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.dead_image = pygame.image.load('images/ghost.jpg')
        self.dead_image = pygame.transform.scale(self.dead_image, (40, 80))
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()


    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 3):
            img_right = pygame.image.load(f'images/guy{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load('images/ghost.jpg')
        self.dead_image = pygame.transform.scale(self.dead_image, (40, 80))
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True
        self.number_of_jumpes= self.number_of_jumpes
        #self.number_of_lives = self.number_of_lives


    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 5
        collision_thresh = 20

        if game_over == 0:
            #get keypresses
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.number_of_jumpes >0 :
                self.vel_y = -15
                self.jumped = True
                self.number_of_jumpes -=1


            if key[pygame.K_SPACE] and self.jumped == False and self.number_of_jumpes>0 and self.rect.y>0 and self.rect.y<screen_height :
                self.vel_y = -13
                self.number_of_jumpes-=1
                print(self.number_of_jumpes)
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT] and self.rect.x >0:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT] and self.rect.x <1150:
                print(self.rect.x)
                dx += 5
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]


            #handle animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]


            #add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            #check for collision
            for tile in world.tile_list:
                #check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                #check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    #check if above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False
                        self.number_of_jumpes = 2


            #check for collision with enemies
            if pygame.sprite.spritecollide(self, blob_group, False):
                if check_lives():
                    self.reset(100,700)
                else:
                    game_over = -1

            # check for collision with exit
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1
            # check for collision with  moving platforms
            for platform in platform_group:
                # check for x collision
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # check for y collision
                if platform.rect.colliderect(self.rect.x , self.rect.y + dy, self.width, self.height):
                    # check for y collision if under platform
                    if abs((self.rect.top +dy)- platform.rect.bottom) < collision_thresh :
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    # check for y collision if upper the  platform
                    elif abs((self.rect.bottom  +dy) - platform.rect.top) < collision_thresh :
                        self.rect.bottom = platform.rect.top -1
                        self.in_air = False
                        self.jumped = False
                        self.number_of_jumpes = 2
                        #self.jumped = False
                        dy = 0
                    # moving with platforms
                    if platform.move_x !=0:
                        self.in_air = False
                        self.rect.x += platform.move_direction


            #check for collision with lava
            if pygame.sprite.spritecollide(self, lava_group, False):
                if check_lives():
                    self.reset(100,700)
                else:
                    game_over = -1
            # check for collision with scrypts
            if pygame.sprite.spritecollide(self, scrypt_group, False):
                script = True

            #collision with a ball
            if pygame.sprite.spritecollide(self, ball_group, False):
                if check_lives():
                    self.reset(100,700)
                else:
                    game_over = -1

            # check for collision with stop_scrypt_group
            if pygame.sprite.spritecollide(self, stop_scrypt_group, False):
                script = False

            #update player coordinates
            self.rect.x += dx
            self.rect.y += dy


        elif game_over == -1:
            self.image = self.dead_image
            draw_text('GAME OVER!', font, (255, 0, 255), (screen_width // 2) - 200, screen_height//2 )
            if self.rect.y > 200:
                self.rect.y -= 5

        #draw player onto screen
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        return game_over


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        self.image = pygame.image.load('images/enemy11.png')
        self.image = pygame.transform.scale(self.image, (60, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        for num in range(1, 9):
            img_right = pygame.image.load(f'images/enemy{demention}{num}.png')
            img_right = pygame.transform.scale(img_right, (50, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1
            # handle animation

        self.counter = 0
        self.index += 1
        if self.index >= len(self.images_right):
            self.index = 0
        if self.move_direction <0:
            self.image = self.images_right[self.index]
        if self.move_direction >0:
            self.image = self.images_left[self.index]


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = door_img
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class Script(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = door_img
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Moving_platform(pygame.sprite.Sprite):

    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(f'images/platform{demention}.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.move_y = move_y

    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('images/lava.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(f'images/sun.jpg')
        self.image = pygame.transform.scale(img, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_x=10

        def update(self):
            self.rect.x += self.move_direction * self.move_x
            self.rect.y += self.move_direction * self.move_y
            self.move_counter += 1
            if abs(self.move_counter) > 50:
                self.move_direction *= -1
                self.move_counter *= -1

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('images/coin.png')
        self.image = pygame.transform.scale(img, (tile_size//2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
class World():
    def __init__(self, data):
        self.tile_list = []

        #load images
        dirt_img = pygame.image.load(f'images/ground{demention}.png')
        grass_img = pygame.image.load(f'images/ground{demention}.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == '1':
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == '2':
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == '3':
                    blob = Enemy(col_count * tile_size, row_count * tile_size + 20)
                    blob_group.add(blob)
                if tile == '3':
                    blob = Enemy(col_count * tile_size, row_count * tile_size + 15)
                    blob_group.add(blob)
                if tile == 's':
                    scrypt = Script(col_count * tile_size, row_count * tile_size )
                    scrypt_group.add(scrypt)
                if tile == '4':
                    platform = Moving_platform(col_count * tile_size, row_count * tile_size + (tile_size),1,0)
                    platform_group.add(platform)
                if tile == '5':
                    platform = Moving_platform(col_count * tile_size, row_count * tile_size + (tile_size),0,1)
                    platform_group.add(platform)
                if tile == '6':
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                if tile == '8':
                    exit = Exit(col_count * tile_size, row_count * tile_size )
                    exit_group.add(exit)
                if tile == '7':
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                if tile == 'l':
                    item_mes= Button(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    found_item_group.Add(item_mes)
                if tile == 'f':
                    script =Script(col_count * tile_size , row_count * tile_size )
                    stop_scrypt_group.add(script)
                if tile == 'b' :
                   ball= Ball(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                   ball_group.add(ball)

                col_count += 1
            row_count += 1




    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

class Items():
    def __init__(self, data):
        self.tile_list = []

        #load images
        dirt_img = pygame.image.load('images/ground1.png')
        grass_img = pygame.image.load('images/ground1.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == '1':
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                #if tile == '2':

                if tile == '5':
                    platform = Moving_platform(col_count * tile_size, row_count * tile_size + (tile_size ))
                    platform_group.add(platform)
                if tile == '6':
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                if tile == '8':
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exit_group.add(exit)
                if tile == '7':
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                if tile == 'l':
                    item_mes= Button(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    found_item_group.Add(item_mes)
                col_count += 1
            row_count += 1




    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen,(255,255,255), tile[1],2)



player = Player(100, screen_height - 130)

blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
scrypt_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
found_item_group = pygame.sprite.Group()
stop_scrypt_group= pygame.sprite.Group()
ball_group= pygame.sprite.Group()

#creating our world
with open(f'images/level{level}','r') as map_file:
    level_map=[]
    for line in map_file:
        line=line.strip()
        for t in line:
            line.strip('1')
        level_map.append(line)
with open(f'images/items','r') as map_file:
    items_map=[]
    for line in map_file:
        line=line.strip()
        for t in line:
            line.strip('1')
        items_map.append(line)

world = World(level_map)
items = Items(items_map)

#

# create buttons
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, play_img)
start_button = Button(screen_width // 2 - 450, screen_height // 2, start_img)
exit_button = Button(screen_width -700, screen_height // 2, exit_img)
chest_button = Button(screen_width // 2 + 200, screen_height // 2, chest_img)
back_button = Button(screen_width // 2 , screen_height // 2, back_img)
pause_button = Button(screen_width // - 200 , screen_height // 2, pause_img)
run = True
while run:

    clock.tick(fps)

    screen.blit(bg_img, (0, 0))


    if main_menu == True and list_of_items==False:
        if chest_button.draw():
            list_of_items = True
            main_menu = False
        while list_of_items:
            items.draw()

            for event in pygame.event.get():
                key = pygame.key.get_pressed()
                if key[pygame.K_SPACE]:
                    list_of_items=False
                    main_menu = True
            pygame.display.update()


        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
    elif(main_menu ==False and list_of_items==False):
        world.draw()
        if pause_button.draw():
            pause = True
        while pause:
            for event in pygame.event.get():
                key = pygame.key.get_pressed()
                if key[pygame.K_SPACE]:
                    pause = False

        if game_over == 0 and pause == False:
            blob_group.update()
            ball_group.update()
            platform_group.update()
            # update score
            # check if a coin has been collected
            if pygame.sprite.spritecollide(player, coin_group, True):
                score += 1
            draw_text('X ' + str(score), font_score, (255, 255, 255), tile_size - 10, 10)

        ball_group.draw(screen)
        blob_group.draw(screen)
        platform_group.draw(screen)
        lava_group.draw(screen)
        coin_group.draw(screen)
        exit_group.draw(screen)
        found_item_group.draw(screen)
        game_over = player.update(game_over)
        show_lives()
        # if player has died
        if game_over == -1 :
            if restart_button.draw():
                world_data = []
                world = reset_level(level)
                game_over = 0
                number_of_lives =3
                score = 0

        # if player has completed the level
        if game_over == 1:
            # reset game and go to next level
            level += 1
            if level <= max_level:
                # reset level
                world_data = []
                world = reset_level(level)
                game_over = 0
            else:
                draw_text('YOU WIN!', font, (0, 255 / 0), (screen_width // 2) - 140, screen_height // 2)
                if restart_button.draw():
                    level = 1
                    # reset level
                    world_data = []
                    world = reset_level(level)
                    game_over = 0
                    score = 0




    for event in pygame.event.get():
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            run = False
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
