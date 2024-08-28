import sys, pygame
import pygame.locals
import random
from pygame import mixer

pygame.init()
pygame.mixer.init

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 900
SIDE_MEDU_WIDTH = 200
GRID_WIDTH = 600
GRID_HEIGHT = 600
SIDE_INDENT = 20
TOP_INDENT = 20
GRID_BOTTOM = GRID_HEIGHT + TOP_INDENT
GRID_RIGHT = SCREEN_WIDTH - SIDE_INDENT
GRID_LEFT = SCREEN_WIDTH - SIDE_INDENT - GRID_WIDTH
ENEMY_GRID_RIGHT = SIDE_INDENT + GRID_WIDTH
ENEMY_GRID_LEFT = SIDE_INDENT
BORDER_WIDTH = 1
NUM_OF_COLS = 10
NUM_OF_ROWS = 10
CELL_SIZE = (GRID_WIDTH - (BORDER_WIDTH * NUM_OF_COLS)) // NUM_OF_COLS - 1
FULL_CELL_SIZE = CELL_SIZE + (BORDER_WIDTH * 2)
BLUE = (68, 132, 235)
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
RED = (255,0,0)
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


#game variables
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battle Ship")
menu_font = pygame.font.SysFont("skia", 32)
title_font = pygame.font.SysFont("skia", 72, bold=True)
plain_font = pygame.font.SysFont("skia", FONT_SIZE, bold=True)
smaller_plain_font = pygame.font.SysFont("skia", SMALL_FONT_SIZE, bold=True)
super_small_text = pygame.font.SysFont("skia", SUPER_SMALL_FONT, bold=True)
main_menu = False
ocean = pygame.image.load("assets/Ocean-Background.jpg")
resize_ocean = pygame.transform.scale(ocean, (GRID_WIDTH, GRID_HEIGHT))
player_grid = resize_ocean
enemy_grid = resize_ocean
last_hit_message = ""
game_over = False
player_turn = "Player"
ship_direction = 0

#Music and effects
splash_sound = mixer.Sound("./assets/cannon_miss.ogg")
sinking_ship_sound = mixer.Sound("./assets/full-explosion.wav")
plane_missile_sound = mixer.Sound("./assets/missile-sound.wav")
plane_flying_sound = mixer.Sound("./assets/missile-sound.wav")
enemy_small_explostion_sound = mixer.Sound("./assets/Small-Explostion.wav")
enemy_plane_sound = mixer.Sound("./assets/Plane-Flyby.wav")
sound_arr = []



# ships_info = [('assets/SHIPS/PlaneF-35Lightning2.png', "Plane", 1), ("assets/SHIPS/ShipBattleshipHull.png", "BattleShip", 4), ("assets/SHIPS/ShipCarrierHull.png", "Carrier", 5), ("assets/SHIPS/ShipCruiserHull.png", "Cruiser", 3), ("assets/SHIPS/ShipDestroyerHull.png", "Destroyer", 2), ("assets/SHIPS/ShipPatrolHull.png", "PatrolHull", 3), ("assets/SHIPS/ShipRescue.png", "Rescue", 4), ("assets/SHIPS/ShipSubMarineHull.png", "Submarine", 3)]
ships_info = [("assets/SHIPS/ShipBattleshipHull.png", "BattleShip", 5), ("assets/SHIPS/ShipCarrierHull.png", "Carrier", 4), ("assets/SHIPS/ShipRescue.png", "Rescue", 4),  ("assets/SHIPS/ShipSubMarineHull.png", "Submarine", 3), ("assets/SHIPS/ShipCruiserHull.png", "Cruiser", 2), ("assets/SHIPS/ShipPatrolHull.png", "PatrolHull", 2), ("assets/SHIPS/ShipDestroyerHull.png", "Destroyer", 2), ('assets/SHIPS/PlaneF-35Lightning2.png', "Plane", 1)]
# ships_info = [("assets/SHIPS/ShipBattleshipHull.png", "BattleShip", 4),('assets/SHIPS/PlaneF-35Lightning2.png', "Plane", 1)]



starting_enemy_ship_locs = []
all_ships = []
display_index = 0
display_ship_path = ships_info[display_index][0]
display_ship_title = ships_info[display_index][1]


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
explosions = pygame.sprite.Group()
ships_left = 8
enemy_ships_left = 8


class explosion(pygame.sprite.Sprite):
    def __init__(self, image, pos, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (width, height))
        self.pos = pos
        self.width = width
        self.height = height
        self.rect = self.image.get_rect()



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


def check_enemy_hit(target):
    global sinking_ship_sound
    global ships_left
    print(target.box.center)
    for ship in loaded_ships:
        print(ship.rect.top)
        print(ship.rect.bottom)
        print(ship.rect.left)
        print(ship.rect.right)
        
        if ship.rect.colliderect(target.box):
            print("Enemey HIT!!!")
            ship.hits -= 1
            sound_arr.append(plane_flying_sound)
            target.hit = True
            if ship.hits == 0:
                ship.exploded = True
                # sinking_ship_sound.play()
                sound_arr.append(sinking_ship_sound)
                ships_left -= 1
            return True
    return False
        
    

def enemy_choose_target():
    global plane_missile_sound
    global enemy_hit_boxes
    global player_turn
    
    
    
    possible_hits = [box for box in enemy_target_boxes if box not in enemy_hit_boxes]
    if game_over == False:
        rand_box = random.choice(possible_hits)
        if rand_box not in enemy_hit_boxes:
            enemy_hit_boxes.append(rand_box)
            sound_arr.append(enemy_plane_sound)
            if check_enemy_hit(rand_box):
                # plane_missile_sound.play()
                sound_arr.append(enemy_small_explostion_sound)
                # rand_box.color = GREEN
                print("Hit")
                
                player_turn = "Enemy"
                enemy_choose_target()
            else:
                print("Miss")
                player_turn = "Player"
                sound_arr.append(splash_sound)

            
        print(rand_box)
    
    
def missile_sound(collide):
    global plane_missile_sound
    global splash_sound
    global player_turn
    # plane_missile_sound.play(fade_ms=3000)
    if collide:
        player_turn = "Player"
    elif collide == False:
        player_turn = "Enemy"
        # splash_sound.play()
        
        # print("hit!!!")
        
        
    
    


def check_box_ship_collision(target, ships_group, mouse_pos):
    global sinking_ship_sound
    global enemy_ships_left
    global player_turn
    collide = False
    for ship in ships_group:
        if ship.rect.collidepoint(mouse_pos) and target.clicked == False:
            player_turn = "Player"
            target.hit = True
            if ship.exploded == False and target not in hit_boxes:
                ship.hits-= 1
                print(f'{ship.title}: {ship.hits} left')
                sound_arr.append(plane_flying_sound)
            if ship.hits == 0 and ship.exploded == False:
                enemy_ships_left -= 1
                # sinking_ship_sound.play()
                sound_arr.append(sinking_ship_sound)
                print(f'{ship.title} has exploded')
                print(f'{enemy_ships_left} ships left')
                ship.exploded = True
            collide = True
        else:
            player_turn = "Enemy"
        # print(player_turn)
        # print(collide)  
        missile_sound(collide)




class TargetBox():
    def __init__(self, type, color, pos, width, height, col, row):
        self.type = type
        self.color = color
        self.hover_color = WHITE
        self.pos = pos
        self.height = height
        self.width = width
        self.box = pygame.rect.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.border_rect = pygame.rect.Rect(self.pos[0] - BORDER_WIDTH, self.pos[1] - BORDER_WIDTH, self.width + (BORDER_WIDTH * 2), self.height + (BORDER_WIDTH * 2))
        self.clicked = False
        self.coord = [col, row]
        self.hit = False
        
    def draw(self):
        # border_rect = pygame.rect.Rect(self.pos[0] - 2, self.pos[1] - 2, self.width + 4, self.height + 4)
        if self.type == "Player":
            pygame.draw.rect(screen, TEAL, self.border_rect)
            pygame.draw.rect(screen, self.color, self.box)
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
        if player_turn == "Player":
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            if self.box.collidepoint(mouse_pos):
                if mouse_click[0] == 1 and self.clicked == False:
                    check_box_ship_collision(self, enemy_ships, mouse_pos)
                    self.clicked = True
                    return True
            if mouse_click[0] == 0:
                self.clicked = False
            




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


for target in player_target_boxes:
    print(target.box.x, target.box.y)
        





#Load in all player ships
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
        ship_img = pygame.image.load(ship[0])
        

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
    def __init__(self, txt, color, pos, width, height):
        self.text = txt
        self.text_surf = menu_font.render(self.text, True, PURPLE)
        self.color = color
        self.display_color = self.color
        self.hover_color = WHITE
        self.pos = pos
        self.height = height
        self.width = width
        self.button = pygame.rect.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.text_rect = self.text_surf.get_rect(center = self.button.center)
        self.border_rect = pygame.rect.Rect(self.pos[0] - 2, self.pos[1] - 2, self.width + 4, self.height + 4)
        self.clicked = False
        
    def draw(self):
        # border_rect = pygame.rect.Rect(self.pos[0] - 2, self.pos[1] - 2, self.width + 4, self.height + 4)
        pygame.draw.rect(screen, PURPLE, self.border_rect, border_radius=15)
        pygame.draw.rect(screen, self.display_color, self.button, border_radius=15)
        screen.blit(self.text_surf, self.text_rect)
    
            
    def checkClicked(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if self.button.collidepoint(mouse_pos):
            self.display_color = self.hover_color
            if mouse_click[0] == 1 and self.clicked == False:
                self.clicked = True
                self.update_color()
                return True
        if mouse_click[0] == 0:
            self.display_color = self.color
            self.clicked = False
    
    def isHoveredOver(self, color):
        mouse_pos = pygame.mouse.get_pos()
        over = self.button.collidepoint(mouse_pos)
        



# Load and scale display ship
display_ship_img = pygame.image.load(display_ship_path)
display_ship = pygame.transform.rotate(display_ship_img, 90)

if ships_info[display_index][2] > 2:
    display_ship_width = 200
else:
    display_ship_width = 100

display_ship = pygame.transform.scale(display_ship, (display_ship_width,CELL_SIZE))



#Check if game is over to move to another screen
def check_game_over():
    global main_menu
    global game_over
    global enemy_ships_left
    if enemy_ships_left == 0:
        game_over = True
        
    if ships_left == 0:
        game_over = True






        
 
# Game loop.
while True:
    
  
    if main_menu:
        # screen.fill(BLUE)
        menu_x = SCREEN_WIDTH//4 + 170//2
        menu_y = SCREEN_HEIGHT//2
        new_game = Button("New Game", GREEN, (menu_x, menu_y), 175, 50)
        new_game.draw()
    
    else:
        screen.fill(BLACK)
        screen.blit(player_grid, (SIDE_INDENT,SIDE_INDENT))
        screen.blit(enemy_grid, (SCREEN_WIDTH - (GRID_WIDTH + SIDE_INDENT),SIDE_INDENT))
        
        
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
            if (target.checkClicked() and game_over == False):
                hit_boxes.append(target)
                
        
        #Player boxes that the enemy is targeting
        for enemy_target in enemy_target_boxes:
            enemy_hit_boxes_coords = [box.coord for box in enemy_hit_boxes ]
            if enemy_target.coord not in enemy_hit_boxes_coords:
                enemy_target.draw()
            if enemy_target.coord in enemy_hit_boxes_coords and enemy_target.hit == True:
                enemy_target.draw_hit()
            if enemy_target.coord in enemy_hit_boxes_coords and enemy_target.hit == False:
                enemy_target.draw_miss()
        
        
        #Show Ships that have exploded      
        for ship in enemy_ships:
            if ship.hits == 0:
                screen.blit(ship.image, ship.rect)
                check_game_over()
        
        if player_turn == "Enemy":
            enemy_choose_target()

        
        
            
        # Draw display ship to show the player which ship is being moved
        screen.blit(display_ship, (SCREEN_WIDTH//2 - (display_ship.get_width()//2), SCREEN_HEIGHT//3))
        
        ship_text = smaller_plain_font.render(display_ship_title, True, GREEN)
        screen.blit(ship_text, (SCREEN_WIDTH//2 - (ship_text.get_width()//2), 200))
        
        #Draw Game Over
    
        lose_txt = "You Lost!!"
        win_txt = "You Won!!"
            
        
        if game_over and ships_left == 0:
            game_status_surf = smaller_plain_font.render(lose_txt, True, GREEN)
            screen.blit(game_status_surf, (SCREEN_WIDTH//2 - (game_status_surf.get_width()//2), 100))
        elif game_over and enemy_ships_left == 0:
            game_status_surf = smaller_plain_font.render(win_txt, True, GREEN)
            screen.blit(game_status_surf, (SCREEN_WIDTH//2 - (game_status_surf.get_width()//2), 100))
            
        #Draw whose turn
        if player_turn == "Enemy":
            player_turn_txt = "ENEMY"
        elif player_turn == "Player":
            player_turn_txt = "YOUR"
        else:
            player_turn_txt = ""
        
        full_player_turn = f'{player_turn} TURN'
        
        
        turn_text = smaller_plain_font.render(player_turn, True, PURPLE, WHITE)
        screen.blit(turn_text, (SCREEN_WIDTH//2 - (turn_text.get_width()//2), 500))
        
        
        ships_left_text = smaller_plain_font.render(f'{ships_left} ships left', True, BLUE)
        screen.blit(ships_left_text, (SCREEN_WIDTH//2 - (ships_left_text.get_width()//2), 600))

        enemy_ships_left_text = smaller_plain_font.render(f'{enemy_ships_left} Enemy ships left', True, BLUE)
        screen.blit(enemy_ships_left_text, (SCREEN_WIDTH//2 - (enemy_ships_left_text.get_width()//2), 700))
        
        
        
        
        loaded_ships.draw(screen)
        
        for s in sound_arr:
            s.play()
            pygame.time.wait(500)
            sound_arr.pop(0)

            

    


  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
  
  # Update.
  
  # Draw.
  
    pygame.display.update()
    fpsClock.tick(fps)