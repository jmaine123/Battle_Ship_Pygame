import os
import time
import sys, pygame
import pygame.locals
import random
from pygame import mixer

pygame.init()
pygame.mixer.init

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 900
SIDE_MEDU_WIDTH = 200
GRID_WIDTH = 600
GRID_HEIGHT = 600
SIDE_INDENT = 20
TOP_INDENT = 40
GRID_BOTTOM = GRID_HEIGHT + TOP_INDENT
GRID_RIGHT = SCREEN_WIDTH - SIDE_INDENT
GRID_LEFT = SCREEN_WIDTH - SIDE_INDENT - GRID_WIDTH
ENEMY_GRID_RIGHT = SIDE_INDENT + GRID_WIDTH
ENEMY_GRID_LEFT = SIDE_INDENT
BORDER_WIDTH = 1
NUM_OF_COLS = 10
NUM_OF_ROWS = 10
CELL_SIZE = (GRID_WIDTH - (BORDER_WIDTH * NUM_OF_COLS)) // NUM_OF_ROWS - 1
FULL_CELL_SIZE = CELL_SIZE + (BORDER_WIDTH * 2)

#COLORS
BLUE = (68, 132, 235)
DARK_BLUE = (16, 52, 110)
CLEAR_RED = (255,0,0,85)
CLEAR_DARK_PURPLE = (51, 0, 204, 85)
CLEAR_BLUE = (52, 122, 235, 85)
PURPLE = (51, 0, 204)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 223, 0)
ORANGE = (255, 165, 0)
TEAL = (3, 244, 252)
AQUA = (37, 179, 162)
RED = (255,0,0)
DARK_GREEN = (39, 176, 50)
DARK_BLUE_GREEN = (3, 133, 140)
DARK_AQUA = (14, 114, 201)
DARK_RED = (133, 4, 6)

#FONT SIZES
FONT_SIZE = 40
SMALL_FONT_SIZE = 30
SUPER_SMALL_FONT = 20
BIG_FONT_SIZE = 50
IMAGE_SIZE = (300, 300)
IMAGE_PADDING = 10
MAIN_MENU_BTN_WIDTH = 200
MAIN_MENU_BTN_HEIGHT = 50

 
fps = 60
fpsClock = pygame.time.Clock()
turnClock = pygame.time.Clock()


#Font variables
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battle Ship")
#skia
menu_font = pygame.font.SysFont("futura", 32)
title_font = pygame.font.SysFont("futura", 102)
plain_font = pygame.font.SysFont("futura", FONT_SIZE)
game_font = pygame.font.SysFont("futura", 22)
smaller_plain_font = pygame.font.SysFont("futura", SMALL_FONT_SIZE)
super_small_font = pygame.font.SysFont("futura", SUPER_SMALL_FONT, bold=True)

# Game Variables
main_menu = True
game_over = False
game_progress = "Menu"
# ocean = pygame.image.load("./assets/Ocean-Background.jpg")
ocean = pygame.image.load(resource_path("./assets/Ocean-Background.jpg"))
# ocean = resource_path("./Ocean-Background.jpg")
main_menu_ocean = pygame.transform.scale(ocean, (SCREEN_WIDTH, SCREEN_HEIGHT))
resize_ocean = pygame.transform.scale(ocean, (GRID_WIDTH, GRID_HEIGHT))
player_ocean = resize_ocean
enemy_ocean = resize_ocean
last_hit_message = ""
player_turn = "Player"
ship_direction = 0
turn_timer = 0
target_img = pygame.image.load(resource_path("./assets/red-aim2.png"))
target_icon = pygame.transform.scale(target_img, (CELL_SIZE, CELL_SIZE))


#Music and effects
pirates_music = mixer.music.load(resource_path("./assets/Pirates.mp3"))
splash_sound = mixer.Sound(resource_path("./assets/cannon_miss.ogg"))
sinking_ship_sound = mixer.Sound(resource_path("./assets/full-explosion.wav"))
plane_missile_sound = mixer.Sound(resource_path("./assets/missile-sound.wav"))
plane_flying_sound = mixer.Sound(resource_path("./assets/missile-sound.wav"))
enemy_small_explostion_sound = mixer.Sound(resource_path("./assets/Small-Explostion.wav"))
enemy_plane_sound = mixer.Sound(resource_path("./assets/Plane-Flyby.wav"))
sonar_sound = mixer.Sound(resource_path("./assets/Sonar.wav"))
sound_arr = []


#Ship tuples with ship information and image path (path, title, length)
ships_info = [("./assets/SHIPS/ShipBattleshipHull.png", "Battleship", 5), ("./assets/SHIPS/ShipCarrierHull.png", "Carrier", 4), ("./assets/SHIPS/ShipRescue.png", "Rescue", 4),  ("./assets/SHIPS/ShipSubMarineHull.png", "Submarine", 3), ("./assets/SHIPS/ShipCruiserHull.png", "Cruiser", 3), ("./assets/SHIPS/ShipPatrolHull.png", "Patrol Hull", 2), ("./assets/SHIPS/ShipDestroyerHull.png", "Destroyer", 2), ('./assets/SHIPS/PlaneF-35Lightning2.png', "Plane", 1)]




# starting_enemy_ship_locs = []
# all_ships = []



#Variables to draw grid
cols = []
enemy_cols = []
rows = []


#Ship Variables
user_ship_coord = []
player_target_boxes = []
enemy_target_boxes = []
hit_boxes = []
enemy_hit_boxes = []
loaded_ships = pygame.sprite.Group()
enemy_ships = pygame.sprite.Group()
explosion_imgs = pygame.image.load(resource_path("./assets/Single_explosion.png")).convert_alpha()
explosions_group = pygame.sprite.Group()
menu_larges_ship_img = pygame.image.load(resource_path("./assets/shipz ripples/images/ship_large_body.png")).convert_alpha()
menu_small_ship_img = pygame.image.load(resource_path("./assets/shipz ripples/images/ship_medium_body_b.png")).convert_alpha()
ripple_img = pygame.image.load(resource_path("./assets/shipz ripples/images/water_ripple_big_003.png")).convert_alpha()
small_ripple_img = pygame.image.load(resource_path("./assets/shipz ripples/images/water_ripple_small_004.png")).convert_alpha()
menu_ships = pygame.sprite.Group()
ships_left = 8
enemy_ships_left = 8
enemy_ship_updates = []
player_ship_updates = []





class MenuShip(pygame.sprite.Sprite):
    def __init__(self, image, ripple_img, pos, width, height, angle, txt, font, direction):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.font = font
        self.txt = self.font.render(txt, True, TEAL, None)
        self.txt_surf = self.txt.get_rect()
        self.pos = pos
        self.rotated_image = pygame.transform.rotate(image, angle)
        self.image = pygame.transform.scale(self.rotated_image, (width, height))
        self.ripple_rotated = pygame.transform.rotate(ripple_img, angle)
        self.ripple = pygame.transform.scale(self.ripple_rotated, (width, height + self.height - 40))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.ripple_rect = self.ripple.get_rect()
        self.ripple_rect.center = self.rect.topleft
        self.txt_surf.center = self.rect.center
        self.direction = direction
    
    def draw_ripples(self):
        screen.blit(self.ripple, (self.rect.left + self.width//20 - 20, self.rect.top - self.height//2 + 20))
        # screen.blit(self.ripple, self.ripple_rect.center)
    
    def draw_text(self):
        screen.blit(self.txt, (self.rect.centerx - self.txt.get_width()//2, self.rect.centery - self.txt.get_height()//2 ))
    
    def update_features(self):
        self.txt_surf.center = self.rect.center
        
        
           





class Explosion(pygame.sprite.Sprite):
    def __init__(self, image, pos, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (width, height))
        self.pos = pos
        self.width = width
        self.height = height
        self.rect = self.image.get_rect()
        self.rect.center = self.pos



class Ship(pygame.sprite.Sprite):
    def __init__(self, type, image, width, height, angle, hits, title, coord):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.image = pygame.transform.scale(image, (width, height))
        self.angle = angle
        self.rotated_image = pygame.transform.rotate(self.image, self.angle)
        self.height = height
        self.width = CELL_SIZE
        self.rect = self.rotated_image.get_rect()
        self.hits = hits
        self.title = title
        self.rect.topleft = [coord[0], coord[1]]
        self.ship_sections_coords = []
        self.placed = False
        self.exploded = False
        
    def adjust_ship(self):
        prev_width = self.width
        prev_height = self.height
        prev_topleft = self.rect.topleft
        # prev_center = self.rect.center
        
        if self.angle % 180 != 0:
            self.image = pygame.transform.scale(self.rotated_image, (prev_height, prev_width))
            # self.rect = self.rotated_image.get_rect()
        else:
            self.image = pygame.transform.scale(self.image, (prev_width, prev_height))
            self.rect = self.image.get_rect()
        # self.rect.center = prev_center
        self.rect.topleft = prev_topleft
        self.put_on_grid()
            
    def put_on_grid(self):
        if self.rect.bottom > GRID_BOTTOM:
            self.rect.y -= self.rect.bottom - GRID_BOTTOM
        if self.rect.top < TOP_INDENT:
            self.rect.y += TOP_INDENT
        if self.type == "Player":
            if self.rect.right > GRID_RIGHT:
                self.rect.x -= self.rect.right - GRID_RIGHT
            if self.rect.left < GRID_LEFT:
                self.rect.x += GRID_RIGHT
        if self.type == "Enemy":
            if self.rect.right > SIDE_INDENT + GRID_WIDTH:
                self.rect.x -= self.rect.right - (SIDE_INDENT + GRID_WIDTH)
                # print("ship pushed")
            if self.rect.left < SIDE_INDENT:
                self.rect.x += GRID_RIGHT
                
    def find_new_loc(self, left_side, right_side):
        TOP_RIGHT = (self.rect.top - FULL_CELL_SIZE <= TOP_INDENT + BORDER_WIDTH) and self.rect.right + FULL_CELL_SIZE >= right_side
        TOP_LEFT = (self.rect.top - FULL_CELL_SIZE <= TOP_INDENT + BORDER_WIDTH) and self.rect.left - FULL_CELL_SIZE <= left_side
        TOP = self.rect.top - FULL_CELL_SIZE <= TOP_INDENT + BORDER_WIDTH
        LEFT = self.rect.left - FULL_CELL_SIZE <= left_side
        RIGHT = self.rect.right + FULL_CELL_SIZE >= right_side
        BOTTOM_RIGHT = (self.rect.bottom + FULL_CELL_SIZE >= GRID_BOTTOM) and self.rect.right + FULL_CELL_SIZE >= right_side
        BOTTOM_LEFT = (self.rect.bottom + FULL_CELL_SIZE >= GRID_BOTTOM) and self.rect.left - FULL_CELL_SIZE <= left_side
        BOTTOM = self.rect.bottom + FULL_CELL_SIZE >= GRID_BOTTOM
        global ship_direction
        if TOP_RIGHT:
            print(f'{self.title} top is {self.rect.top} and  right is {self.rect.right}' )
            print("Reached TOP RIGHT CORNER")
            ship_direction = 1
        elif TOP_LEFT:
            print(f'{self.title} top is {self.rect.top} and  right is {self.rect.left}' )
            print("Reached TOP LEFT CORNER")
            ship_direction = 2
        elif BOTTOM_RIGHT:
            print(f'{self.title} top is {self.rect.bottom} and  right is {self.rect.right}' )
            print("Reached BOTTOM RIGHT CORNER")
            ship_direction = 0
        elif BOTTOM_LEFT:
            print(f'{self.title} top is {self.rect.bottom} and  right is {self.rect.left}' )
            print("Reached BOTTOM LEFT CORNER")
            ship_direction = 3
        elif TOP:
            print(f'{self.title} top is {self.rect.top}')
            print("Can't go Up anymore")
            ship_direction = 1
        elif LEFT:
            print(f'{self.title} left is {self.rect.left}')
            print("Can't go Left anymore")
            ship_direction = 2
        elif RIGHT:
            print(f'{self.title} right is {self.rect.right}')
            print("Can't go Right anymore")
            ship_direction = 0
        elif BOTTOM:
            print(f'{self.title} bottom is {self.rect.bottom}')
            print("Can't go Down anymore")
            ship_direction = 3
        directions = ["UP", "LEFT", "DOWN", "RIGHT"]
        direction = directions[ship_direction]
        if direction == "UP":
            self.rect.y -= FULL_CELL_SIZE
        if direction == "DOWN":
            self.rect.y += FULL_CELL_SIZE   
        if direction == "LEFT":
            self.rect.x -= FULL_CELL_SIZE      
        if direction == "RIGHT":
            self.rect.x += FULL_CELL_SIZE
        
        print(f'{self.title} was moved {direction}')     
        
    # def update_section_coords(self):
    #     top = self.rect.topleft
    #     bottom = self.rect.midbottom
        


def check_enemy_hit(target):
    global sinking_ship_sound
    global ships_left
    global enemy_ship_updates
    
    for ship in loaded_ships:
        # print(ship.rect.top)
        # print(ship.rect.bottom)
        # print(ship.rect.left)
        # print(ship.rect.right)
        
        if ship.rect.colliderect(target.box):
            # print("Enemey HIT!!!")
            ship.hits -= 1
            sound_arr.append(plane_flying_sound)
            target.hit = True
            status_txt = f"{ship.title} was hit at column {target.coord[0] + 1} , row {target.coord[1] + 1}"
            enemy_ship_updates.append((ship.image, status_txt, ship.angle))
            
            if ship.hits == 0:
                ship.exploded = True
                status_txt = f"{ship.title} was sunk!!!"
                enemy_ship_updates.append((ship.image, status_txt, ship.angle))
                sound_arr.append(sinking_ship_sound)
                ships_left -= 1
            return True
    return False




def find_enemy_nearest_targets(rand_box):
    targets_list = []
    print(f"Target position for enemy hit is {rand_box.pos}")
    rand_box_index = enemy_target_boxes.index(rand_box)
    right_box_index = rand_box_index + 1
    left_box_index = rand_box_index - 1
    right_target = enemy_target_boxes[right_box_index]
    left_target = enemy_target_boxes[left_box_index]
    
    if right_box_index and right_target not in enemy_hit_boxes:
        print(f' Position of box to the right is {right_target.pos}')
        targets_list.append(right_target)
    
    if left_box_index and left_target not in enemy_hit_boxes:
        print(f' Position of box to the right is {right_target.pos}')
        targets_list.append(left_target)
    
    return targets_list
    
    print("Possible right and left targets ")
    # print(targets_list)
    
    
        
        
    

def enemy_choose_target(smart_move = False, prev_move = None, nearest_targets = None):
    global plane_missile_sound
    global enemy_hit_boxes
    global player_turn
    global turn_timer
    
    
    if (smart_move == True and nearest_targets != None) and len(nearest_targets) != 0:
        possible_hits = nearest_targets
    
    else:
        possible_hits = [box for box in enemy_target_boxes if box not in enemy_hit_boxes]
    
    # possible_hits = [box for box in enemy_target_boxes if box not in enemy_hit_boxes]
    
    if (game_over == False or len(possible_hits) != 1 ) and len(possible_hits)!= 0:
        rand_box = random.choice(possible_hits)
        if rand_box not in enemy_hit_boxes:
            enemy_hit_boxes.append(rand_box)
            sound_arr.append(enemy_plane_sound)
            if check_enemy_hit(rand_box):
                sound_arr.append(enemy_small_explostion_sound)
                new_exp = Explosion(explosion_imgs, rand_box.box.center, rand_box.width, rand_box.height)
                explosions_group.add(new_exp)
                player_turn = "Enemy"
                nearest_targets = find_enemy_nearest_targets(rand_box)
                enemy_choose_target(smart_move=True, prev_move=rand_box, nearest_targets=nearest_targets)
            else:
                print("Miss")
                player_turn = "Player"
                sound_arr.append(splash_sound)

    
    
def missile_sound(collide):
    global plane_missile_sound
    global splash_sound
    global player_turn

    if collide:
        player_turn = "Player"
    elif collide == False:
        player_turn = "Enemy"

        
        
    
    


def check_box_ship_collision(target, ships_group, mouse_pos):
    global sinking_ship_sound
    global enemy_ships_left
    global player_turn
    global hit_boxes
    global turn_timer
    collide = False
    for ship in ships_group:
        if ship.rect.collidepoint(target.box.center) and target.clicked == False:
            status_txt = f"{ship.title} was hit at column {target.coord[0] + 1} , row {target.coord[1] + 1}"
            player_ship_updates.append((ship.image, status_txt, ship.angle))
            player_turn = "Player"
            target.hit = True
            if ship.exploded == False and target not in hit_boxes:
                ship.hits-= 1
                print(f'{ship.title}: {ship.hits} left')
                sound_arr.append(plane_flying_sound)
                new_exp = Explosion(explosion_imgs, target.box.center, CELL_SIZE, CELL_SIZE)
                explosions_group.add(new_exp)
            if ship.hits == 0 and ship.exploded == False:
                enemy_ships_left -= 1
                sound_arr.append(sinking_ship_sound)
                status_txt = f"{ship.title} has exploded!!!"
                player_ship_updates.append((ship.image, status_txt, ship.angle))
                print(f'{ship.title} has exploded')
                print(f'{enemy_ships_left} ships left')
                ship.exploded = True
                #Need to add function to remove all target boxes red background that collide with ship
            collide = True
        else:
            turn_timer = pygame.time.get_ticks()
            player_turn = "Enemy" 
        missile_sound(collide)




class TargetBox():
    def __init__(self, type, color, pos, width, height, col, row):
        self.type = type
        self.color = color
        self.hover_color = AQUA
        self.border_color = TEAL
        self.pos = pos
        self.height = height
        self.width = width
        self.box = pygame.rect.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.border_rect = pygame.rect.Rect(self.pos[0] - BORDER_WIDTH, self.pos[1] - BORDER_WIDTH, self.width + (BORDER_WIDTH * 2), self.height + (BORDER_WIDTH * 2))
        self.clicked = False
        self.coord = [col, row]
        self.hit = False
        self.hoverd = False
        
    def draw(self):
        # border_rect = pygame.rect.Rect(self.pos[0] - 2, self.pos[1] - 2, self.width + 4, self.height + 4)
        if self.type == "Player":
            if self.hoverd == False:
                pygame.draw.rect(screen, self.border_color, self.border_rect)
                pygame.draw.rect(screen, self.color, self.box)
            if self.hoverd == True:
                pygame.draw.rect(screen, self.border_color, self.border_rect)
                pygame.draw.rect(screen, self.hover_color, self.box)
                
        if self.type == "Enemy":
            # pygame.draw.rect(screen, CLEAR_DARK_PURPLE, self.border_rect)
            enemy_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            enemy_surface.set_alpha(250)
            enemy_surface.fill(CLEAR_DARK_PURPLE)
            screen.blit(enemy_surface, (self.pos))
            # pygame.draw.rect(screen, ORANGE, self.box)
    
    def draw_hit(self):
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        surface.set_alpha(250)
        surface.fill(RED)
        pygame.draw.rect(screen, CLEAR_DARK_PURPLE, self.border_rect)
        screen.blit(surface, self.pos)
        # pygame.draw.rect(surface, CLEAR_RED, self.box)

    def draw_miss(self):
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        surface.set_alpha(250)
        surface.fill(CLEAR_DARK_PURPLE)
        pygame.draw.rect(screen, TEAL, self.border_rect)
        screen.blit(surface, self.pos)
        # pygame.draw.rect(surface, CLEAR_RED, self.box)
        

    
    def checkClicked(self):
        global player_turn
        global game_progress
        
        if player_turn == "Player" and game_progress == "Fight":
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()    
            if self.box.collidepoint(mouse_pos):
                if mouse_click[0] == 1 and self.clicked == False:
                    check_box_ship_collision(self, enemy_ships, mouse_pos)
                    self.clicked = True
                    return True
            if mouse_click[0] == 0:
                # self.clicked = False
                return False


    def isHoveredOver(self, hover_color):
        mouse_pos = pygame.mouse.get_pos()
        over = self.box.collidepoint(mouse_pos)
        
        if over:
            self.hoverd = True
            self.hover_color = hover_color
        elif over == False:
            self.hoverd = False
            




#SET COLUMNS AND ROWS FOR ENEMY AND PLAYER GRID
for i in range(NUM_OF_COLS):
    col_num = SIDE_INDENT + BORDER_WIDTH + (GRID_WIDTH//NUM_OF_COLS * i)
    enemy_col = SCREEN_WIDTH - (GRID_WIDTH + SIDE_INDENT) + (GRID_WIDTH//NUM_OF_COLS * i)
    row_num = TOP_INDENT + BORDER_WIDTH + resize_ocean.get_height()//NUM_OF_ROWS * i
    enemy_cols.append(enemy_col)
    cols.append(col_num)
    rows.append(row_num)
            
            


#DRAW TILES ON PLAYER GRID      
for i in range(NUM_OF_COLS):
    for j in range(NUM_OF_ROWS):
        box = TargetBox("Player", BLUE, (cols[i], rows[j]), CELL_SIZE, CELL_SIZE, i, j)
        enemy_box = TargetBox("Enemy", BLUE, (enemy_cols[i], rows[j]), CELL_SIZE, CELL_SIZE, i, j)
        player_target_boxes.append(box)
        enemy_target_boxes.append(enemy_box)

        





#Load in all player  and enemy ships
def load_ships(type):
    angles = [90, 180, 270, 0]
    taken_ship_locs = []
    for ship in ships_info:
        if type == "Player":
            available_ship_locs = [s.pos for s in enemy_target_boxes if s.pos not in taken_ship_locs]
        elif type == "Enemy":
            available_ship_locs = [s.pos for s in player_target_boxes if s.pos not in taken_ship_locs]
        ship_len = ship[2]
        # print(ship[1])
        # print(taken_ship_locs)
        ship_angle = random.choice(angles)
        ship_height = ship_len * CELL_SIZE
        ship_width = CELL_SIZE
        ship_img = pygame.image.load(resource_path(ship[0]))
        

        rand_box = random.choice(available_ship_locs)
        user_ship_coord.append(rand_box)
        current_ship_coord = user_ship_coord[-1]
        new_ship = Ship(type, ship_img, ship_width, ship_height, ship_angle, ship[2], ship[1], (current_ship_coord[0], current_ship_coord[1]))
        new_ship.adjust_ship()
        # print("---------------")
        # print(type)
        # print("current ship:" + new_ship.title)
        # print("Prev coord before rotation:" + str(current_ship_coord))
        # print("Angle: " + str(ship_angle))
        # print("new top left: " + str(new_ship.rect.topleft))
        # print("length: " + str(ship_len))
        
        #Add all of ship coords to the taken loc array so that no other ship can be placed in that location
        for i in range(0,ship_len):
            if ship_angle == 0 or ship_angle ==180:       
                ship_y = new_ship.rect.topleft[1] + (CELL_SIZE * i) + (BORDER_WIDTH * 2)
                ship_x = new_ship.rect.topleft[0]
            if ship_angle == 90 or ship_angle == 270:
                ship_y = new_ship.rect.topleft[1] 
                ship_x = new_ship.rect.topleft[0] + (CELL_SIZE * i) * (BORDER_WIDTH * 2)
            taken_ship_locs.append((ship_x, ship_y))
            new_ship.placed = True
            
          
        if type == "Player":
            loaded_ships.add(new_ship)
        if type == "Enemy":
            enemy_ships.add(new_ship)
            

load_ships("Player")
load_ships("Enemy")
 


def move_collided_ships(ship, ships_group):
    global ship_direction
    other_ships = [s for s in ships_group if s.title != ship.title]
    # print(ship.title)
    collided = pygame.sprite.spritecollide(ship, other_ships, False)

    if collided:
        other_ship_title = collided[0].title
        if ship.type == "Enemy":
            ship.find_new_loc(ENEMY_GRID_LEFT, ENEMY_GRID_RIGHT)
        if ship.type == "Player":
            ship.find_new_loc(GRID_LEFT, GRID_RIGHT)
        move_collided_ships(ship, ships_group)
        print(ship.type)
        print(f'{ship.title} has collided with {other_ship_title}')
    else:
        ship_direction = 0
        print(f'{ship.title} was placed')
  
        
def check_ship_to_ship_collision(type):
    if type == "Enemy":
        ships_group = enemy_ships
    elif type == "Player":
        ships_group = loaded_ships
    for ship in reversed(list(ships_group)):
        move_collided_ships(ship, ships_group)


check_ship_to_ship_collision("Player")
check_ship_to_ship_collision("Enemy")
        





class Button:
    def __init__(self, txt, font, color, pos):
        self.text = txt
        self.button_font = font
        self.text_surf = self.button_font.render(self.text, True, PURPLE)
        self.color = color
        self.hover_color = DARK_GREEN
        self.border_color = PURPLE
        self.pos = pos
        self.height = self.text_surf.get_height() + 20
        self.width = self.text_surf.get_width() + 20
        self.button = pygame.rect.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.text_rect = self.text_surf.get_rect(center = self.button.center)
        self.border_rect = pygame.rect.Rect(self.pos[0] - 2, self.pos[1] - 2, self.width + 4, self.height + 4)
        self.clicked = False
        self.hoverd = False
        
    def draw(self):
        if self.hoverd == False:
            pygame.draw.rect(screen, self.border_color, self.border_rect, border_radius=15)
            pygame.draw.rect(screen, self.color, self.button, border_radius=15)
            self.text_surf = self.button_font.render(self.text, True, PURPLE)
            screen.blit(self.text_surf, self.text_rect)
        elif self.hoverd == True:
            pygame.draw.rect(screen, self.color, self.border_rect, border_radius=15)
            pygame.draw.rect(screen, self.hover_color, self.button, border_radius=15)
            screen.blit(self.text_surf, self.text_rect)
            
    
            
    def checkClicked(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if self.button.collidepoint(mouse_pos):
            self.color = self.hover_color
            if mouse_click[0] == 1 and self.clicked == False:
                sonar_sound.play()
                self.clicked = True
                # print("I have been clicked")
                # self.update_color()
                return True
        if mouse_click[0] == 0:
            self.clicked = False
    
    def isHoveredOver(self, color, hover_color):
        mouse_pos = pygame.mouse.get_pos()
        over = self.button.collidepoint(mouse_pos)
        
        if over:
            self.hoverd = True
            self.hover_color = hover_color
            self.text_surf = self.button_font.render(self.text, True, color)
        elif over == False:
            self.hoverd = False
            
        





#Check if game is over to move to another screen
def check_game_over():
    global main_menu
    global game_over
    global game_progress
    global enemy_ships_left
    
    
    if enemy_ships_left == 0:
        game_over = True
        game_progress = "Game Over"
        
    if ships_left == 0:
        game_over = True
        game_progress = "Game Over"
        
        
def draw_ship_status(type):
    global enemy_ship_updates
    global player_ship_updates
    
    if type == "Enemy":
        status_arr = enemy_ship_updates
        status_color = RED
    else:
        status_arr = player_ship_updates
        status_color = GREEN
        
    for index, status in enumerate(status_arr):
        SPACE = 40
        first_row = GRID_BOTTOM + SPACE
        second_row = first_row + SPACE
        third_row = second_row + SPACE
        fourth_row = third_row + SPACE
        fifth_row = fourth_row + SPACE
        
        status_text = super_small_font.render(f'{status[1]}', True, status_color)
        
        if type == "Enemy":
            column = GRID_LEFT + GRID_WIDTH//2 - 20
            img_column = column - 100
        if type == "Player":
            column = ENEMY_GRID_LEFT
            img_column = column + status_text.get_width() + 5


        
        if index > 4:
            status_arr.pop(0)
        
        #Adjust status ship image
        
        
        if status[2] == 0 or status[2] == 180:
            old_hit_ship = pygame.transform.rotate(status[0], 270)
        else:
            old_hit_ship = status[0]
            
        hit_ship = pygame.transform.scale(old_hit_ship, (70,30))
        
        if index == 0 and len(status_arr) > 0:
            screen.blit(status_text, (column, first_row))
            screen.blit(hit_ship, (img_column, first_row))
        elif index == 1 and len(status_arr) > 0:
            status_text = super_small_font.render(f'{status[1]}', True, status_color)
            screen.blit(status_text, (column, second_row))
            screen.blit(hit_ship, (img_column, second_row))
        elif index == 2 and len(status_arr) > 0:
            status_text = super_small_font.render(f'{status[1]}', True, status_color)
            screen.blit(status_text, (column, third_row))
            screen.blit(hit_ship, (img_column, third_row))
        elif index == 3 and len(status_arr) > 0:
            status_text = super_small_font.render(f'{status[1]}', True, status_color)
            screen.blit(status_text, (column, fourth_row))
            screen.blit(hit_ship, (img_column, fourth_row))
        elif index == 4 and len(status_arr) > 0:
            status_text = super_small_font.render(f'{status[1]}', True, status_color)
            screen.blit(status_text, (column, fifth_row))
            screen.blit(hit_ship, (img_column, fifth_row))
        
            


def shuffle_ships(type):
    if type == "Enemy":
        enemy_ships.empty()
    if type == "Player":
        loaded_ships.empty() 
    load_ships(type)
    check_ship_to_ship_collision(type)
            


def start_game():
    global user_ship_coord
    global ships_left
    global enemy_ships_left
    global player_ship_updates
    global enemy_ship_updates
    global player_turn
    global game_over
    global game_progress
    
    # Reset Target boxes for both players and users
    for index, target in enumerate(player_target_boxes):
        target.hit = False
        target.clicked = False
        target.hoverd = False
        enemy_target_boxes[index].hit = False
        enemy_target_boxes[index].clicked = False
        
    
    
    # Clear Groups
    hit_boxes.clear()
    enemy_hit_boxes.clear()
    explosions_group.empty()
    # enemy_ships.empty()
    # loaded_ships.empty()
    ships_left = 8
    enemy_ships_left = 8
    enemy_ship_updates.clear()
    player_ship_updates.clear()
    user_ship_coord.clear()
    
    shuffle_ships("Enemy")
    shuffle_ships("Player")
    
    game_over = False
    game_progress = "Set Board"
    player_turn = "Player"
    

def draw_scoreboard():
    pass
    
main_ship = MenuShip(menu_larges_ship_img, ripple_img, (-100,200), 900, 300, 270, "BATTLESHIP", title_font, "RIGHT")
menu_ships.add(main_ship)

created_by_ship = MenuShip(menu_small_ship_img, small_ripple_img, (SCREEN_WIDTH + 700,600), 250, 100, 90, "CREATED BY", menu_font, "LEFT")
menu_ships.add(created_by_ship)

name_ship = MenuShip(menu_small_ship_img, ripple_img, (SCREEN_WIDTH + 700,700), 450, 100, 270, "JERMAINE SMIKLE", menu_font, "RIGHT")
menu_ships.add(name_ship)

def update_menu_ships():
    for ship in menu_ships:
        if ship.direction == "RIGHT":
            ship.rect.x +=1
            ship.draw_ripples()
            ship.update_features()
            
            if ship.rect.left > SCREEN_WIDTH:
                ship.rect.x = - (ship.width) - 200
        if ship.direction == "LEFT":
            ship.rect.x -=2
            ship.draw_ripples()
            ship.update_features()
            
            if ship.rect.right < 0:
                ship.rect.x = SCREEN_WIDTH + 700


def draw_menu_ship_text():
    for ship in menu_ships:
        ship.draw_text()
        
# print(pygame.font.get_fonts())



def draw_mouse_icon():
    if game_over == False:
        pygame.mouse.set_visible(False)
        target_icon_rect = target_icon.get_rect()
        target_icon_rect.center = pygame.mouse.get_pos()
        screen.blit(target_icon, target_icon_rect)
    else:
        pygame.mouse.set_visible(True)
        
        
def show_exploded_ships():
    #Show Ships that have exploded      
    for ship in enemy_ships:
        if ship.hits == 0:
            screen.blit(ship.image, ship.rect)
            check_game_over()
            
            
def play_sound_arr():
    #Play sounds in array
    for s in sound_arr:
        if game_over == False:
            s.play()
            # pygame.time.wait(500)
            sound_arr.pop(0)
        if game_over:
            sound_arr.clear()
            
            
def display_game_status():
    #Draw Game Over
    lose_txt = "DEFEATED!!"
    win_txt = "VICTORY!!"
    

    if ships_left == 0:
        game_status_surf = smaller_plain_font.render(lose_txt, True, RED)
        screen.blit(game_status_surf, (SCREEN_WIDTH//2 - (game_status_surf.get_width()//2), 100))
    if enemy_ships_left == 0:
        game_status_surf = smaller_plain_font.render(win_txt, True, GREEN)
        screen.blit(game_status_surf, (SCREEN_WIDTH//2 - (game_status_surf.get_width()//2), 100))
        

def draw_ships_left():
    # Draw how many ships are left for both sides
    enemy_ships_left_text = smaller_plain_font.render(f'Enemy Ships Left', True, BLUE)
    enemy_text_coord = (ENEMY_GRID_RIGHT - enemy_ships_left_text.get_width()//2, GRID_BOTTOM + 40)
    screen.blit(enemy_ships_left_text, enemy_text_coord)
    pygame.draw.line(screen, BLUE, (ENEMY_GRID_RIGHT - enemy_ships_left_text.get_width()//2, GRID_BOTTOM + 40 + enemy_ships_left_text.get_height()), (ENEMY_GRID_RIGHT + enemy_ships_left_text.get_width()//2, GRID_BOTTOM + 40 + enemy_ships_left_text.get_height()) )

    enemy_left_num = smaller_plain_font.render(str(enemy_ships_left), True, RED)
    screen.blit(enemy_left_num, (enemy_text_coord[0] + enemy_ships_left_text.get_width()//2, enemy_text_coord[1] + enemy_ships_left_text.get_height() ))


    player_ships_left_text = smaller_plain_font.render(f'Player Ships Left', True, BLUE)
    player_text_coord = (GRID_LEFT - player_ships_left_text.get_width()//2, GRID_BOTTOM + 40)
    screen.blit(player_ships_left_text, player_text_coord)
    pygame.draw.line(screen, BLUE, (GRID_LEFT - player_ships_left_text.get_width()//2, GRID_BOTTOM + 40 + player_ships_left_text.get_height()), (GRID_LEFT + player_ships_left_text.get_width()//2, GRID_BOTTOM + 40 + player_ships_left_text.get_height()) )

    player_left_num = smaller_plain_font.render(str(ships_left), True, GREEN)
    screen.blit(player_left_num, (player_text_coord[0] + player_ships_left_text.get_width()//2, enemy_text_coord[1] + player_ships_left_text.get_height() ))
    
    
def show_button(button_name, font, color, x, y):
    btn = Button(button_name, font, color, (x, y))
    btn.button.centerx = center





pygame.mixer.music.play(-1)
 
# Game loop.
while True:
    
  
    if main_menu:
        # screen.fill(BLUE)
        screen.blit(main_menu_ocean, (0,0))
        menu_x = SCREEN_WIDTH//2 - 175//2
        menu_y = SCREEN_HEIGHT//2
        new_game = Button("New Game", menu_font, GREEN, (menu_x, menu_y)) 
        new_game.isHoveredOver(TEAL, DARK_GREEN)
        
        
            
        update_menu_ships()
        menu_ships.draw(screen)
        draw_menu_ship_text()
        
        


        
        
        if game_progress == "Menu":
            new_game.draw()
            if new_game.checkClicked() and game_progress == "Menu":
                main_menu = False
                game_progress = "Set Board"
                start_game()
                
                
                
    
    if (game_progress == "Set Board" or game_progress == "Fight") and main_menu == False:
        #Draw GRID
        screen.fill(DARK_BLUE)
        screen.blit(player_ocean, (SIDE_INDENT,TOP_INDENT))
        screen.blit(enemy_ocean, (SCREEN_WIDTH - (GRID_WIDTH + SIDE_INDENT),TOP_INDENT))
        
        width = 250
        height = 50
        menu_x = SCREEN_WIDTH//2 - width//2
        menu_y = SCREEN_HEIGHT//2
        center = SCREEN_WIDTH//2
        if game_progress == "Set Board":    
            shuffle_button = Button("SHUFFLE SHIPS", game_font, TEAL, (center, menu_y - 150))
            shuffle_button.button.centerx = center
            shuffle_button.text_rect.centerx = center
            shuffle_button.border_rect.centerx = center
            shuffle_button.isHoveredOver(TEAL, DARK_BLUE)
            
            shuffle_button.draw()
            
            fight_button = Button("FIGHT", game_font, GREEN, (center, menu_y - 70))
            fight_button.button.centerx = center
            fight_button.text_rect.centerx = center
            fight_button.border_rect.centerx = center
            fight_button.isHoveredOver(TEAL, DARK_GREEN)
            fight_button.draw()
            
            
            
            if shuffle_button.checkClicked():
                shuffle_ships("Player")
                
            if fight_button.checkClicked():
                game_progress = "Fight"

        menu_button = Button("MAIN MENU", game_font, YELLOW, (center, menu_y + 100))
        menu_button.button.centerx = center
        menu_button.text_rect.centerx = center
        menu_button.border_rect.centerx = center
        menu_button.isHoveredOver(TEAL, (193, 196, 16))
        menu_button.draw()
        
        if menu_button.checkClicked():
            main_menu = True
            game_progress = "Menu"

        #Draw Enemy ships first so that they are hidden under tarets boxes
        enemy_ships.draw(screen)
        
        
                
    #Draw boxes that are not hit
        #Enemy boxes that the player is targeting
        for target in player_target_boxes:
            hit_boxes_coords = [box.coord for box in hit_boxes ]
            if target.coord not in hit_boxes_coords:
                target.draw()
            if target.coord in hit_boxes_coords and target.hit == True:
                target.draw_hit()
            if (target.checkClicked() and (game_over == False and game_progress == "Fight")):
                hit_boxes.append(target)
            if game_progress == "Fight":
                target.isHoveredOver(AQUA)
                target.border_color = TEAL
                target.color = BLUE
            if game_progress == "Set Board":
                target.border_color = DARK_BLUE_GREEN
                target.color = DARK_BLUE
                
                
                
        
        #Player boxes that the enemy is targeting
        for enemy_target in enemy_target_boxes:
            enemy_hit_boxes_coords = [box.coord for box in enemy_hit_boxes ]
            if enemy_target.coord not in enemy_hit_boxes_coords:
                enemy_target.draw()
            if enemy_target.coord in enemy_hit_boxes_coords and enemy_target.hit == True:
                enemy_target.draw_hit()
            if enemy_target.coord in enemy_hit_boxes_coords and enemy_target.hit == False:
                enemy_target.draw_miss()
                

        
        play_sound_arr()



        
        show_exploded_ships()
        
        if player_turn == "Enemy" and (game_over == False and game_progress == "Fight"):
            current_time = pygame.time.get_ticks()
            enemy_choose_target()
            print(turn_timer)
            print(current_time)
                
            
            
        draw_ships_left()       
        
        
        #Draw Player ships on top of the grid so that the player can see them
        loaded_ships.draw(screen)
        
        #Draw all explosions
        explosions_group.draw(screen)
                
        
        # Draw Ship Status Text for every hit and explosion
        draw_ship_status("Enemy")
        draw_ship_status("Player")

    #Draw Restart Button when game is Over
    if game_over and game_progress == "Game Over":
        display_game_status()
        center = SCREEN_WIDTH//2
        menu_y = 150            
                    
        restart_game = Button("RESTART", game_font, GREEN, (center, menu_y))
        restart_game.button.centerx = center
        restart_game.text_rect.centerx = center
        restart_game.border_rect.centerx = center
        restart_game.draw()
        
        if restart_game.checkClicked():
            # print("Restarting....")
            start_game()
        
        if menu_button.checkClicked():
            main_menu = True
            game_progress = "Menu"
                
            

    


  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    draw_mouse_icon()
            
  

    # Update  
    pygame.display.update()
    fpsClock.tick(fps)
    
if __name__ == "__main__":
    pass