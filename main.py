import cursor as cursor
import pygame
import random

pygame.init()
pause=False
clock = pygame.time.Clock()
fps = 60
skin=1
with open(f'images/playersInfo.txt/skin', 'r+') as map_file:
    skin= int(map_file.read())
game_over = 0
tile_size = 50
screen_width = 1200
screen_height = 750
pygame.init()
star_image= pygame.image.load('images/leveldesign/star_jump.png')
door_img=pygame.image.load('images/leveldesign/strelka.png')
door_img = pygame.transform.scale(door_img, (tile_size, tile_size))
bg_img = pygame.image.load('images/leveldesign/sky.jpeg')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
play_img = pygame.image.load('images/leveldesign/start.png')
play_img= pygame.transform.scale(play_img, (320, 80))
heart_img = pygame.image.load('images/leveldesign/heart.png')
heart_img= pygame.transform.scale(heart_img, (30, 30))
coin_img = pygame.image.load('images/leveldesign/coin.png')
coin_img= pygame.transform.scale(coin_img, (60, 60))
start_img=pygame.image.load('images/leveldesign/play.png')
start_img = pygame.transform.scale(start_img, (320,80))
exit_img=pygame.image.load('images/leveldesign/exit.png')
exit_img = pygame.transform.scale(exit_img, (320, 80))
info_img=pygame.image.load('images/leveldesign/info.png')
info_img = pygame.transform.scale(info_img, (160, 71))
back_img=pygame.image.load('images/leveldesign/back.png')
back_img = pygame.transform.scale(back_img, (80, 80))
pause_img=pygame.image.load('images/leveldesign/pause.png')
pause_img = pygame.transform.scale(pause_img, (80, 80))
back_button_img = pygame.image.load('images/leveldesign/back_button.png')
back_button_img = pygame.transform.scale(back_button_img, (320,80))
continue_button_img=pygame.image.load('images/leveldesign/continue_button.png')
continue_button_img = pygame.transform.scale(continue_button_img, (320,80))
shot_img=pygame.image.load('images/leveldesign/back.png')
sun_image=pygame.image.load(f'images/leveldesign/sun.jpg')
shot_img = pygame.transform.scale(shot_img, (40,40))
shop_img=pygame.image.load('images/leveldesign/shop.png')
shop_img = pygame.transform.scale(shop_img, (80,60))
main_menu_button_img=pygame.image.load('images/leveldesign/main_menu.png')
main_menu_button_img = pygame.transform.scale(main_menu_button_img, (320,80))
new_game_button_img=pygame.image.load('images/leveldesign/new_game.png')
main_menu_button_img = pygame.transform.scale(main_menu_button_img, (320,80))
restart_img=pygame.image.load('images/leveldesign/restart.png')
restart_img= pygame.transform.scale(restart_img, (320,80))
skins_img=pygame.image.load('images/leveldesign/skins.png')
skins_img = pygame.transform.scale(skins_img, (600,600))
choose_img=pygame.image.load('images/leveldesign/choose.png')
choose_img = pygame.transform.scale(choose_img, (140,40))
#with open(f'images/playersInfo.txt/num_of_level.txt', 'r+') as map_file:
    #level = int(map_file.read())
max_level=7
score=0
demention =1
script = False
screen_width = 1200
screen_height = 750
main_menu = True
list_of_items=False
shop_menu = False
number_of_lives=3
all_balls =[]
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)
total_number_of_coins = 0

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
    star_jump_group.empty()
    exit_group.empty()
    heart_group.empty()
    scrypt_group.empty()
    stop_scrypt_group.empty()
    found_item_group.empty()
    blade_group.empty()
    blade2_group.empty()
    with open(f'images/levels/level{level}', 'r') as map_file:
        level_map = []
        for line in map_file:
            line = line.strip()
            for t in line:
                line.strip('1')
            level_map.append(line)

    world = World(level_map)
    return(world)
#load images


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

def extra_lives():
    global number_of_lives
    number_of_lives +=1
class Moving_platform(pygame.sprite.Sprite):

    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(f'images/leveldesign/platform{demention}.png')
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
        img = pygame.image.load('images/leveldesign/lava.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Player():

    def __init__(self, x, y):
        with open(f'images/playersInfo.txt/skin', 'r+') as map_file:
            self.skin_num=(int)(map_file.read())

        self.number_of_jumpes=2
        #self.number_of_lives = number_of_lives
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 3):

            img_right = pygame.image.load(f'images/skins/character{self.skin_num}{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.dead_image = pygame.image.load('images/skins/ghost.png')
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
        self.skin_num=self.skin_num
        for num in range(1, 6):
            img_right = pygame.image.load(f'images/skins/character{self.skin_num}{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load('images/skins/ghost.png')
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
            if (key[pygame.K_SPACE] or key[pygame.K_w]) and self.jumped == False and self.number_of_jumpes >0 :
                self.vel_y = -15
                self.jumped = True
                self.number_of_jumpes -=1


            if (key[pygame.K_SPACE] or key[pygame.K_w]) and self.jumped == False and self.number_of_jumpes>0 and self.rect.y>0 and self.rect.y<screen_height :
                self.vel_y = -13
                self.number_of_jumpes-=1
            if ((key[pygame.K_SPACE]) == False) and  (key[pygame.K_w]==False) :
                self.jumped = False
            if (key[pygame.K_LEFT] or key[pygame.K_a]) and self.rect.x >0:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if (key[pygame.K_RIGHT] or key[pygame.K_d]) and self.rect.x <1150:
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
            # check for collision with blades
            if pygame.sprite.spritecollide(self, blade_group, False) or pygame.sprite.spritecollide(self, blade2_group, False):
                if check_lives():
                    self.reset(100, 700)
                else:
                    game_over = -1
            # check for collision with stars_jump
            if pygame.sprite.spritecollide(self, star_jump_group, False):
                self.in_air = False
                self.jumped = False
                self.number_of_jumpes = 2




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
        self.image = pygame.image.load('images/enemies/enemy11.png')
        self.image = pygame.transform.scale(self.image, (60, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        for num in range(1, 9):
            img_right = pygame.image.load(f'images/enemies/enemy{1}{num}.png')
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








class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        img = image
        self.image = pygame.transform.scale(image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10

        def update(self):
            if self.rect.x <=screen_width - self.move_x:
                self.rect.x +=  self.move_x
                screen.blit(self.image , (self.rect.x , self.rect.y))
                return True
            else:
                return False


class Blade(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        self.image = pygame.image.load('images/enemies/blade1.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        for num in range(1, 10):
            img_right = pygame.image.load(f'images/enemies/blade{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            self.imgs_right.append(img_right)
        self.image = self.imgs_right[self.index]
        self.move_counter = -1
        self.move_direction = 1

    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1
        self.index += 1
        if self.index >= len(self.imgs_right):
            self.index = 1
        self.image = self.imgs_right[self.index]
    def __init__(self, x, y ,  distance):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/enemies/blade1.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.distance = distance
        self.imgs_right=[]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_x=2
        self.move_y=2
        self.index=1
        self.images=[]
        for num in range(1, 10):
            img_right = pygame.image.load(f'images/enemies/blade{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            self.imgs_right.append(img_right)
        self.image = self.imgs_right[self.index]
        self.move_counter=-1
        self.move_direction=1



    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1
        self.index+=1
        if self.index >= len(self.imgs_right):
            self.index = 1
        self.image=self.imgs_right[self.index]


class Blade2(pygame.sprite.Sprite):
    def __init__(self, x, y ,  distance, z, f):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/enemies/blade1.png')
        #self.image = pygame.transform.scale(self.image, (100, 100))
        self.distance = distance
        self.img_right=[]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_x=z
        self.move_y=f
        self.index=1
        self.images=[]
        for num in range(1, 10):
            img_right = pygame.image.load(f'images/enemies/blade{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            self.img_right.append(img_right)
        #self.image = self.img_right[self.index]
        self.move_counter=-1
        self.move_direction=1

    def update(self):
        for i in range (0,100):
            if self.index>= len(self.img_right):
                self.index=1

            self.image = self.img_right[self.index]
            if i>50:
                self.rect.x += self.move_direction
            else:

                self.rect.y += self.move_direction

            self.index += 1
            self.move_counter += 1
            if abs(self.move_counter) > 50:
                self.move_direction *= -1
                self.move_counter *= -1


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

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y , image):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('images/leveldesign/coin.png')
        self.image = pygame.transform.scale(image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
class World():
    def __init__(self, data):
        self.tile_list = []

        #load images
        dirt_img = pygame.image.load(f'images/leveldesign/ground{demention}.png')
        grass_img = pygame.image.load(f'images/leveldesign/ground -with-circled-end-right{demention}.png')
        grass_img_left_circled = pygame.image.load(f'images/leveldesign/ground -with-circled-end-left{demention}.png')

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
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2), coin_img)
                    coin_group.add(coin)
                if tile == 'l':
                    item_mes= Button(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    found_item_group.Add(item_mes)
                if tile == 'f':
                    script =Script(col_count * tile_size , row_count * tile_size )
                    stop_scrypt_group.add(script)
                if tile == 'b' :

                   ball= Ball(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2),  sun_image)
                   ball_group.add(ball)
                if tile == 'h' :
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2),heart_img)
                    heart_group.add(coin)
                if tile == 'i' :
                   ball= Ball(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2),  star_image)
                   star_jump_group.add(ball)
                if tile == 't' :
                   blade= Blade(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2),1)
                   blade_group.add(blade)

                if tile == 'u' :
                   blade= Blade2(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2),1,0,0)
                   blade2_group.add(blade)
                if tile == 'v':
                    blade = Blade2(col_count * tile_size + (tile_size // 2),row_count * tile_size + (tile_size // 2), 0, 2, 10)
                    blade2_group.add(blade)
                if tile == "a":
                    img = pygame.transform.scale(grass_img_left_circled, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                col_count += 1
            row_count += 1




    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

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
heart_group = pygame.sprite.Group()
star_jump_group = pygame.sprite.Group()
blade_group = pygame.sprite.Group()
blade2_group = pygame.sprite.Group()
#creating our world
with open(f'images/playersInfo.txt/num_of_level.txt', 'r+') as map_file:
    level = int(map_file.read())
with open(f'images/levels/level{level}','r') as map_file:
    level_map=[]
    for line in map_file:
        line=line.strip()
        for t in line:
            line.strip('1')
        level_map.append(line)
with open(f'images/levels/items','r') as map_file:
    items_map=[]
    for line in map_file:
        line=line.strip()
        for t in line:
            line.strip('1')
        items_map.append(line)


world = World(level_map)

# create buttons
restart_button = Button(screen_width // 2 -200, screen_height // 2 + 100, restart_img)
new_game_button = Button(screen_width   - 800, screen_height // 2, new_game_button_img)
exit_button = Button(screen_width -400, screen_height // 2, exit_img)
info_button = Button(10, 10, info_img)
back_button = Button(10 , 10, back_img)
pause_button = Button(10, 10, pause_img)
shop_menu_button = Button(1100 , 10,  shop_img)
continue_button = Button(screen_width // 2 - 600, screen_height // 2,  continue_button_img)
main_menu_button=Button(screen_width//2 , screen_height//2, main_menu_button_img)
choose_skin_1_button= Button(screen_width//2-255, screen_height//2-93, choose_img)
choose_skin_2_button= Button(screen_width//2-78 , screen_height//2-93, choose_img)
choose_skin_3_button= Button(screen_width//2+100 , screen_height//2-93, choose_img)
choose_skin_4_button= Button(screen_width//2-255 , screen_height//2+115, choose_img)
choose_skin_5_button= Button(screen_width//2-78 , screen_height//2+115, choose_img)
choose_skin_6_button= Button(screen_width//2+100 , screen_height//2+115, choose_img)
run = True

while run:


    clock.tick(fps)

    screen.blit(bg_img, (0, 0))

    cursor_image=pygame.transform.scale(pygame.image.load('images/leveldesign/cursor.png'), (50,50))



    if main_menu == True and list_of_items==False:
        screen.blit(cursor_image, pygame.mouse.get_pos())
        if info_button.draw():
            list_of_items = True
            main_menu = False
        while list_of_items:

            if back_button.draw():
                list_of_items = False
                main_menu = True

            for event in pygame.event.get():
                key = pygame.key.get_pressed()
                if key[pygame.K_SPACE]:
                    list_of_items = False
                    main_menu = True
            pygame.display.update()
        if continue_button.draw():
            main_menu = False
        if exit_button.draw():
            run = False
        if new_game_button.draw():
            with open(f'images/playersInfo.txt/num_of_level.txt', 'r+') as map_file:
                map_file.write('1')
            level=1
            main_menu = False
        if shop_menu_button.draw():
            shop_menu =True
            main_menu = False
    elif shop_menu:
        screen.blit(cursor_image, pygame.mouse.get_pos())
        with open(f'images/playersInfo.txt/skin', 'r+') as map_file:
            screen.blit(skins_img, (screen_width//2-300 , screen_height//2-300))
            screen.blit(coin_img , (1140,16))
            if choose_skin_1_button.draw():
                map_file.seek(0)
                map_file.write("1")
            if choose_skin_2_button.draw():
                map_file.seek(0)
                map_file.write("3")
            if choose_skin_3_button.draw():
                map_file.seek(0)
                map_file.write("2")
            if choose_skin_4_button.draw():
                map_file.seek(0)
                map_file.write("4")
            if choose_skin_5_button.draw():
                map_file.seek(0)
                map_file.write("5")
            if choose_skin_6_button.draw():
                map_file.seek(0)
                map_file.write("6")
        with open('images/playersInfo.txt/money.txt', 'r+') as money_file:
            result = money_file.read()
        draw_text(f'{result}', font, (50, 255 , 0), 1030, 10)
        if back_button.draw():
             shop_menu = False
             main_menu = True
        for event in pygame.event.get():
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                list_of_items = False
                main_menu = True

        pygame.display.update()




    elif(main_menu ==False and list_of_items==False and shop_menu==False):
        pygame.mouse.set_visible(0)

        with open(f'images/playersInfo.txt/num_of_level.txt', 'r+') as map_file:
            level = int(map_file.read())
        if level>2:
            demention = 2
        else:
            demention=1
        world.draw()
        key = pygame.key.get_pressed()
        if  key[pygame.K_q] :
            pause = True
        while pause:
            pygame.mouse.set_visible(1)
            screen.blit(cursor_image, pygame.mouse.get_pos())
            for event in pygame.event.get():
                key = pygame.key.get_pressed()
                if key[pygame.K_SPACE]:
                    pause = False

        if game_over == 0 and pause == False:
            blob_group.update()
            ball_group.update()
            platform_group.update()
            blade_group.update()
            blade2_group.update()
            for ball in all_balls:
                if  ball.update():
                    ball.draw(screen)

                else:
                    all_balls.remove(ball)

            # update score
            # check if a coin has been collected
            if pygame.sprite.spritecollide(player, coin_group, True):
                score += 1
            draw_text('X ' + str(score), font_score, (255, 255, 255), tile_size - 10, 10)
            if pygame.sprite.spritecollide(player, heart_group, True):
                number_of_lives += 1

        ball_group.draw(screen)
        blob_group.draw(screen)
        platform_group.draw(screen)
        lava_group.draw(screen)
        coin_group.draw(screen)
        exit_group.draw(screen)
        heart_group.draw(screen)
        found_item_group.draw(screen)
        star_jump_group.draw(screen)
        blade_group.draw(screen)
        blade2_group.draw(screen)
        game_over = player.update(game_over)
        show_lives()


        # if player has died
        if game_over == -1 :
            screen.blit(cursor_image, pygame.mouse.get_pos())
            if restart_button.draw():
                world_data = []
                world = reset_level(level)
                game_over = 0
                number_of_lives =3
                score = 0

        # if player has completed the level
        if game_over == 1:
            #write money and update score
            with open('images/playersInfo.txt/money.txt', 'r+') as money_file:
                result=money_file.read()
                money_file.seek(0)
                result=int(result)
                result2=score+result
                money_file.write(f'{result2}')
            score=0
            # reset game and go to next level
            if level<=max_level:
                level += 1

            if level>2:
                demention = 2
            elif level<2:
                demention = 1
            with open(f'images/playersInfo.txt/num_of_level.txt', 'r+') as map_file:
                map_file.truncate(0)
                map_file.write(f'{level}')

            if level <= max_level:
                # reset level
                world_data = []
                world = reset_level(level)
                game_over = 0
            elif level>max_level:
                draw_text('YOU WIN!', font, (0, 255 , 0), (screen_width // 2) - 140, screen_height // 2)
                if new_game_button.draw():
                    level=1
                    demention=1
                    with open(f'images/playersInfo.txt/num_of_level.txt', 'r+') as map_file:
                        map_file.write(f'{level}')
                    # reset level
                    world_data = []
                    world = reset_level(level)
                    game_over = 0
                    score = 0
                    level = 1

                if main_menu_button.draw():
                    shop_menu = False
                    main_menu = True






    for event in pygame.event.get():
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            run = False
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()



pygame.quit()
