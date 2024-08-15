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
BORDER_WIDTH = 2
NUM_OF_COLS = 10
NUM_OF_ROWS = 10
CELL_SIZE = (GRID_WIDTH - (BORDER_WIDTH * NUM_OF_COLS)) // NUM_OF_COLS - 1
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
ships_left = 8
# ships_info = [('assets/SHIPS/PlaneF-35Lightning2.png', "Plane", 1), ("assets/SHIPS/ShipBattleshipHull.png", "BattleShip", 4), ("assets/SHIPS/ShipCarrierHull.png", "Carrier", 5), ("assets/SHIPS/ShipCruiserHull.png", "Cruiser", 3), ("assets/SHIPS/ShipDestroyerHull.png", "Destroyer", 2), ("assets/SHIPS/ShipPatrolHull.png", "PatrolHull", 3), ("assets/SHIPS/ShipRescue.png", "Rescue", 4), ("assets/SHIPS/ShipSubMarineHull.png", "Submarine", 3)]
ships_info = [("assets/SHIPS/ShipCarrierHull.png", "Carrier", 3), ("assets/SHIPS/ShipBattleshipHull.png", "BattleShip", 3), ("assets/SHIPS/ShipSubMarineHull.png", "Submarine", 2),("assets/SHIPS/ShipRescue.png", "Rescue", 2), ("assets/SHIPS/ShipCruiserHull.png", "Cruiser", 2), ("assets/SHIPS/ShipPatrolHull.png", "PatrolHull", 2), ("assets/SHIPS/ShipDestroyerHull.png", "Destroyer", 2), ('assets/SHIPS/PlaneF-35Lightning2.png', "Plane", 1)]
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
        self.placed = False
        
    def adjust_ship(self):
        prev_width = self.width
        prev_height = self.height
        prev_center = self.rect.center
        
        if self.angle % 180 != 0:
            self.image = pygame.transform.scale(self.rotated_image, (prev_height, prev_width))
            # self.rect = self.rotated_image.get_rect()
            self.rect.center = prev_center
        else:
            self.image = pygame.transform.scale(self.image, (prev_width, prev_height))
            self.rect = self.image.get_rect()
            self.rect.center = prev_center
        
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
                print("ship pushed")
            if self.rect.left < SIDE_INDENT:
                self.rect.x += GRID_RIGHT
                
    def find_new_loc(self, pos_arr):
        # recent_pos = []
        new_pos = random.sample(pos_arr, 1)
        self.topleft = new_pos
        
        
        

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
        pygame.draw.rect(surface, CLEAR_RED, self.box)
        

    
    def checkClicked(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if self.box.collidepoint(mouse_pos):
            if mouse_click[0] == 1 and self.clicked == False:
                # print("click")
                # btn_sound.play()
                self.clicked = True
                return True
        if mouse_click[0] == 0:
            self.clicked = False


#SET COLUMNS AND ROWS FOR ENEMY AND PLAYER GRID
for i in range(NUM_OF_COLS):
    col_num = SIDE_INDENT + (GRID_WIDTH//NUM_OF_COLS * i)
    enemy_col = SCREEN_WIDTH - (GRID_WIDTH + SIDE_INDENT) + (GRID_WIDTH//NUM_OF_COLS * i)
    row_num = SIDE_INDENT + resize_ocean.get_height()//NUM_OF_ROWS * i
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
        



# choose 8 locations for user ships to be placed in the beginning of the game
# for i in range(0,len(ships_info)):
#     taken_ship_locs = []
#     available_ship_locs = [s for s in enemy_target_boxes if s not in taken_ship_locs]
#     found = False
#     while found == False:
#         rand_box = random.choice(available_ship_locs)
#         if rand_box.coord not in user_ship_coord:
#             user_ship_coord.append((rand_box.pos))
#             taken_ship_locs.append(rand_box.pos)
#             found = True





#Load in all player ships
def load_ships(type):
    for index, ship in enumerate(ships_info):
        angles = [90, 180, 270, 0]
        ship_angle = random.choice(angles)
        ship_height = ship[2] * CELL_SIZE
        ship_width = CELL_SIZE
        ship_img = pygame.image.load(ship[0])
        ship = Ship(type, ship_img, ship_width, ship_height, ship_angle, ship[2], ship[1], (user_ship_coord[index][0], user_ship_coord[index][1]))
        if type == "Player":
            loaded_ships.add(ship)

def select_correct_loc(ship, ship_len, angle, available_ship_locs, taken_ship_locs):
    pass

def load_ships_test(type):
    angles = [90, 180, 270, 0]
    taken_ship_locs = []
    for ship in ships_info:
        if type == "Player":
            available_ship_locs = [s.pos for s in enemy_target_boxes if s.pos not in taken_ship_locs]
        elif type == "Enemy":
            available_ship_locs = [s.pos for s in player_target_boxes if s.pos not in taken_ship_locs]
        ship_len = ship[2]
        print(ship[1])
        print(taken_ship_locs)
        ship_angle = random.choice(angles)
        ship_height = ship_len * CELL_SIZE
        ship_width = CELL_SIZE
        ship_img = pygame.image.load(ship[0])
        

        rand_box = random.choice(available_ship_locs)
        user_ship_coord.append(rand_box)
        current_ship_coord = user_ship_coord[-1]
        new_ship = Ship(type, ship_img, ship_width, ship_height, ship_angle, ship[2], ship[1], (current_ship_coord[0], current_ship_coord[1]))
        new_ship.adjust_ship()
        print(type)
        print("current ship:" + new_ship.title)
        print("Prev coord before rotation:" + str(current_ship_coord))
        print("Angle: " + str(ship_angle))
        print("new top left: " + str(new_ship.rect.topleft))
        print("length: " + str(ship_len))
        
        #Add all of ship coords to the taken loc array so that no other ship can be placed in that location
        for i in range(0,ship_len):
            if ship_angle == 0 or ship_angle ==180:
                ship_y = new_ship.rect.topleft[1] + (CELL_SIZE * i)
                ship_x = new_ship.rect.topleft[0]
            if ship_angle == 90 or ship_angle == 270:
                ship_y = new_ship.rect.topleft[1] 
                ship_x = new_ship.rect.topleft[0] + (CELL_SIZE * i)
            taken_ship_locs.append((ship_x, ship_y))
            new_ship.placed = True
            
          
        if type == "Player":
            loaded_ships.add(new_ship)
        if type == "Enemy":
            enemy_ships.add(new_ship)
            

load_ships_test("Player")
load_ships_test("Enemy")


def collide_if_not_self(ship_one, ship_two):
    if ship_one != ship_two:
        return pygame.sprite.collide_rect(ship_one, ship_two)
    return False 


# for ship in loaded_ships:
#     # ship.adjust_ship()
#     while ship.placed == False:
#         other_ships = pygame.sprite.Group([s for s in loaded_ships if s != ship])
#         if pygame.sprite.spritecollide(ship, other_ships, False):
#             # ship.find_new_loc(enemy_target_boxes)
#             ship.adjust_ship()
#             print(ship.rect.bottom)
#             ship.placed = True
#         else:
#             ship.adjust_ship()
#             ship.placed = True
        





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
            if target.coord not in hit_boxes:
                target.draw()
            if target.coord in hit_boxes:
                target.draw_hit()
            if target.checkClicked():
                hit_boxes.append(target.coord)
                
        for enemy_target in enemy_target_boxes:
            if enemy_target.coord not in enemy_hit_boxes:
                enemy_target.draw()
            # if enemy_target.coord in hit_boxes:
            #     enemy_target.draw_hit()
            
        #Draw Ships on player grid
        # test_ship = all_ships[1]
        
    # Draw display ship to show the player which ship is being moved
    screen.blit(display_ship, (SCREEN_WIDTH//2 - (display_ship.get_width()//2), SCREEN_HEIGHT//3))
    
    text = smaller_plain_font.render(display_ship_title, True, GREEN)
    screen.blit(text, (SCREEN_WIDTH//2 - (display_ship.get_width()//2), 200))
    
    loaded_ships.draw(screen)

            

    


  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
  
  # Update.
  
  # Draw.
  
    pygame.display.update()
    fpsClock.tick(fps)