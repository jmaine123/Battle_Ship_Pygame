import sys, pygame
import pygame.locals
import random

pygame.init()

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 900
SIDE_MEDU_WIDTH = 200
GRID_WIDTH = 600
GRID_HEIGHT = 600
SIDE_INDENT = 20
TOP_INDENT = 20
GRID_BOTTOM = GRID_HEIGHT + TOP_INDENT
GRID_RIGHT = SCREEN_WIDTH - SIDE_INDENT
GRID_LEFT = SIDE_INDENT + GRID_WIDTH
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
ocean = pygame.image.load("assets/frederic-christian-zaGqaYfbNp8-unsplash.jpg")
resize_ocean = pygame.transform.scale(ocean, (GRID_WIDTH, GRID_HEIGHT))
player_grid = resize_ocean
enemy_grid = resize_ocean
last_hit_message = ""
game_over = False

# ships_info = [('assets/SHIPS/PlaneF-35Lightning2.png', "Plane", 1), ("assets/SHIPS/ShipBattleshipHull.png", "BattleShip", 4), ("assets/SHIPS/ShipCarrierHull.png", "Carrier", 5), ("assets/SHIPS/ShipCruiserHull.png", "Cruiser", 3), ("assets/SHIPS/ShipDestroyerHull.png", "Destroyer", 2), ("assets/SHIPS/ShipPatrolHull.png", "PatrolHull", 3), ("assets/SHIPS/ShipRescue.png", "Rescue", 4), ("assets/SHIPS/ShipSubMarineHull.png", "Submarine", 3)]
ships_info = [("assets/SHIPS/ShipCarrierHull.png", "Carrier", 4), ("assets/SHIPS/ShipBattleshipHull.png", "BattleShip", 3), ("assets/SHIPS/ShipSubMarineHull.png", "Submarine", 3),("assets/SHIPS/ShipRescue.png", "Rescue", 3), ("assets/SHIPS/ShipCruiserHull.png", "Cruiser", 2), ("assets/SHIPS/ShipPatrolHull.png", "PatrolHull", 2), ("assets/SHIPS/ShipDestroyerHull.png", "Destroyer", 2), ('assets/SHIPS/PlaneF-35Lightning2.png', "Plane", 1)]
# ships_info = [("assets/SHIPS/ShipBattleshipHull.png", "BattleShip", 4),('assets/SHIPS/PlaneF-35Lightning2.png', "Plane", 1)]



starting_enemy_ship_locs = []
all_ships = []
display_index = 0
display_ship_path = ships_info[display_index][0]
display_ship_title = ships_info[display_index][1]

#grid variables
# cols = [SIDE_MEDU_WIDTH, 320, 440, 560, 680, 800, 920,a 1040, 1160, 1280]
# rows = [0, 120, 240, 360, 480, 600, 720, 840, 960, 1080, 1200]

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
ships_left = 8
enemy_ships_left = 8



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
                
    def find_new_loc(self, direc_index):
        if self.rect.top <= TOP_INDENT + FULL_CELL_SIZE:
            direc_index+= 1
        if self.rect.right >= GRID_RIGHT - FULL_CELL_SIZE:
            direc_index+= 1
        if self.rect.right <= GRID_LEFT + FULL_CELL_SIZE:
            direc_index+= 1
        if self.rect.top <= GRID_BOTTOM:
            direc_index = 0
        if direc_index > 3:
            direc_index = 0
        directions = ["UP", "LEFT", "RIGHT", "DOWN"]
        direction = directions[direc_index]
        if direction == "UP":
            self.rect.y -= FULL_CELL_SIZE
        if direction == "DOWN":
            self.rect.y += FULL_CELL_SIZE   
        if direction == "LEFT":
            self.rect.x -= FULL_CELL_SIZE      
        if direction == "RIGHT":
            self.rect.x += FULL_CELL_SIZE
        
        print(f'{self.title} was moved {direction}')      


def check_box_ship_collision(target, ships_group, mouse_pos):
    global enemy_ships_left
    for ship in ships_group:
        if ship.rect.collidepoint(mouse_pos) and target.clicked == False:
            target.hit = True
            if ship.exploded == False and target not in hit_boxes:
                ship.hits-= 1
                print(f'{ship.title}: {ship.hits} left')
            if ship.hits == 0 and ship.exploded == False:
                enemy_ships_left -= 1
                print(f'{ship.title} has exploded')
                print(f'{enemy_ships_left} ships left')
                ship.exploded = True


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
            pygame.draw.rect(screen, BLACK, self.border_rect)
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
        screen.blit(surface, self.pos)
        # pygame.draw.rect(surface, CLEAR_RED, self.box)
        

    
    def checkClicked(self):
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
    other_ships = [s for s in ships_group if s.title != ship.title]
    # print(ship.title)
    collided = pygame.sprite.spritecollide(ship, other_ships, False)

    if collided:
        other_ship_title = collided[0].title
        ship.find_new_loc(0)
        move_collided_ships(ship, ships_group)
        print(ship.type)
        print(f'{ship.title} has collided with {other_ship_title}')
    else:
        print(f'{ship.title} was placed')
        
def check_ship_collision(type):
    if type == "Enemy":
        ships_group = enemy_ships
    elif type == "Player":
        ships_group = loaded_ships
    for ship in reversed(list(ships_group)):
        move_collided_ships(ship, ships_group)


check_ship_collision("Player")
check_ship_collision("Enemy")
        





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
                # print("click")
                # btn_sound.play()
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
        print(enemy_ships_left)
        # main_menu = True
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
        
        enemy_ships.draw(screen)
                
    #Draw boxes that are not hit
        for target in player_target_boxes:
            hit_boxes_coords = [box.coord for box in hit_boxes ]
            if target.coord not in hit_boxes_coords:
                target.draw()
            if target.coord in hit_boxes_coords and target.hit == True:
                target.draw_hit()
            if target.checkClicked() and game_over == False:
                hit_boxes.append(target)
                
        for enemy_target in enemy_target_boxes:
            if enemy_target.coord not in enemy_hit_boxes:
                enemy_target.draw()
        
        
        #Show Ships that have exploded      
        for ship in enemy_ships:
            if ship.hits == 0:
                screen.blit(ship.image, ship.rect)
                check_game_over()

        
        
            
        # Draw display ship to show the player which ship is being moved
        screen.blit(display_ship, (SCREEN_WIDTH//2 - (display_ship.get_width()//2), SCREEN_HEIGHT//3))
        
        ship_text = smaller_plain_font.render(display_ship_title, True, GREEN)
        screen.blit(ship_text, (SCREEN_WIDTH//2 - (ship_text.get_width()//2), 200))
        game_status_txt = "You Won"
        game_status_surf = smaller_plain_font.render(game_status_txt, True, GREEN)
        if game_over:
            screen.blit(game_status_surf, (SCREEN_WIDTH//2 - (game_status_surf.get_width()//2), 100))
        
        
        loaded_ships.draw(screen)

            

    


  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
  
  # Update.
  
  # Draw.
  
    pygame.display.update()
    fpsClock.tick(fps)