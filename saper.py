import pygame
import sys
import os
from random import choice

def terminate():
    pygame.quit()
    sys.exit()


def start_screen(width=400, height=400):
    size = width, height = width, height
    screen = pygame.display.set_mode(size)    
    font = pygame.font.Font(None, 30)
    textCoord = 10
    fon2 = pygame.sprite.Sprite()
    fon2.image = load_image("start.png")
    fon2.rect = fon2.image.get_rect()
    fon.add(fon2)    
    gui = GUI()
    gui.add_element(Button((15, 300, 110, 40), "Новичок", 1))
    gui.add_element(Button((140, 300, 130, 40), "Любитель", 2))
    gui.add_element(Button((290, 300, 100, 40), "Профи", 3))
    
    gui.add_element(Label((140, 0, 70, 60), "САПЁР"))
    gui.add_element(Label((130, 50, 90, 30), "ПРАВИЛА ИГРЫ"))
    gui.add_element(Label((20, 75, 90, 30), "Нужно открыть все ячейки без мин."))
    gui.add_element(Label((20, 95, 90, 30), "Если вы попадаете на ячейку с миной,"))
    gui.add_element(Label((25, 115, 90, 30), "то вы проигрываете."))
    gui.add_element(Label((20, 135, 90, 30), "Клетки открываются нажатием на "))
    gui.add_element(Label((25, 155, 90, 30), "левую кнопку мыши."))
    gui.add_element(Label((20, 175, 90, 30), "Возможное расположение мины отмечается "))
    gui.add_element(Label((25, 195, 90, 30), "правой кнопкой мыши"))
      
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            gui.get_event(event)
        fon.draw(screen)
        gui.render(screen)
        gui.update() 
        pygame.display.flip()
        clock.tick(fps)
        
def end_screen(end=0, width=400, height=400):
    size = width, height = width, height
    screen = pygame.display.set_mode(size)    
    gui = GUI()
    gui.add_element(Button((150, 320, 110, 50), "МЕНЮ", 0))
    if end == 0:
        gui.add_element(Label((40, 0, 110, 60), "ВЫ ПРОИГРАЛИ!"))
    if end == 1:
        gui.add_element(Label((40, 0, 110, 60), "ПОЗДРАВЛЯЕМ!"))
        gui.add_element(Label((40, 40, 110, 60), "ВЫ ВЫИГРАЛИ!"))
    fon1 = pygame.sprite.Sprite()
    fon1.image = load_image("fon.png")
    fon1.rect = fon1.image.get_rect()
    fon.add(fon1)    
        
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            gui.get_event(event)
        fon.draw(screen)
        gui.render(screen)
        gui.update()
        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(50)        
        pygame.display.flip()
        clock.tick(fps)
        
def load_image(name, colorkey = None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message) 
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey)
    return image 


def mine(num):
    boards = [Minesweeper(9, 9, 10), Minesweeper(11, 11, 40), Minesweeper(15, 15, 80)]
    mine = boards[num]
    top, left = mine.get_cell_size_top_left()[1]
    cell_size = mine.get_cell_size_top_left()[0]
    row, col = mine.get_row_col()    
    size = width, height = left * 2 + row * cell_size, top * 2 + col * cell_size
    screen = pygame.display.set_mode(size)
    running = True  
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and  event.button == 3:
                mine.get_click(event.pos, 2)
            if event.type == pygame.MOUSEBUTTONDOWN and  event.button == 1:
                mine.get_click(event.pos)
        fon.draw(screen)
        mine.render()    
        pygame.display.flip()  


def button_open(num):
    if num == 0:
        start_screen()
    elif num == 1:
        mine(0)
    elif num == 2:
        mine(1)
    elif num == 3:
        mine(2)
    

class Board:
    def __init__(self, width=100, height=100):
        self.width = width
        self.height = height
        self.cell_size = 20
        self.top = 10
        self.left = 10
        self.board = self.board = [[-1 for _ in range(height)] for _ in range(width)]
        
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        
    def render(self):
        for h in range(self.height):
            for w in range(self.width):
                if self.board[w][h] == 0:
                    pygame.draw.rect(screen, (155, 155, 155), 
                                     (self.left + self.cell_size * w + 1,
                                      self.top + self.cell_size * h + 1, 
                                      self.cell_size - 2, self.cell_size - 2))
                if self.board[w][h] == -2 or self.board[w][h] == -20:
                    mine_img.image = pygame.transform.scale(load_image("flag.jpg"), (20, 20))
                    mine_img.rect = mine_img.image.get_rect()
                    mine_img.rect.x = self.left + self.cell_size * w + 1
                    mine_img.rect.y = self.top + self.cell_size * h + 1
                    mines.add(mine_img)
                    mines.draw(screen)
                    mines.update()
                if self.board[w][h] != 10 and self.board[w][h] != -1 and self.board[w][h] != 0 and self.board[w][h] != -2 and self.board[w][h] != -20:
                    pygame.draw.rect(screen, (155, 155, 155), 
                                     (self.left + self.cell_size * w + 1,
                                      self.top + self.cell_size * h + 1, 
                                      self.cell_size - 2, self.cell_size - 2))                    
                    text = self.font.render(str(self.board[w][h]), 1, self.font_color)
                    screen.blit(text, (self.left + w * self.cell_size + 1, 
                                       self.top + h * self.cell_size + 1,
                                       self.cell_size - 2,
                                       self.cell_size - 2))                    
                pygame.draw.rect(screen, pygame.Color('black'), 
                                 (self.left + self.cell_size * w, 
                                  self.top + self.cell_size * h,
                                  self.cell_size, self.cell_size), 1)                
                
    def get_cell_size_top_left(self):
        return self.cell_size, (self.top, self.left)
    
    def get_row_col(self):
        return self.width, self.height
                
    def get_click(self, mouse_pos, button=1):
        print(button)
        cell = self.get_cell(mouse_pos)
        if cell and button == 1:
            self.open_cell(cell)
        if cell and button == 2:
            self.flag(cell)
          
        
    def on_click(self, cell):
        if not isinstance(cell, bool):
            x, y = cell
            if self.board[x][y] == -1:
                self.board[x][y] = 0  
                
    def get_cell(self, mouse_pos):
        x = (mouse_pos[0] - self.left) // self.cell_size
        y = (mouse_pos[1] - self.top) // self.cell_size
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            return x, y
   
   
class Minesweeper(Board):
    def __init__(self, width, height, mine=10):
        super().__init__(width, height)
        self.mine = mine
        self.font = pygame.font.Font(None, 20)
        self.font_color = pygame.Color(10, 10, 10)  
        
        coor = 0
        while coor < self.mine:
            coordinat = (choice(range(self.width)), choice(range(self.height)))
            if self.board[coordinat[0]][coordinat[1]] != 10:
                self.board[coordinat[0]][coordinat[1]] = 10
                coor += 1
            
    def mines(self, x, y):
        print(self.board)
        if self.board[x][y] != 10 and self.board[x][y] == -1 and self.board[x][y] != -20 and self.board[x][y] != -2:
            kol_mine = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if not (i == 0 and j == 0):
                        if 0 <= x + i <= len(self.board) - 1 and 0 <= y + j <= len(self.board[0]) - 1:
                            if self.board[x + i][y + j] == 10 or self.board[x + i][y + j] == -20:
                                kol_mine += 1
            self.board[x][y] = kol_mine
            return kol_mine
        
    
    def open_cell(self, cell):
        x, y = cell
        n = 0
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            if self.mines(x, y) == 0:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        self.open_cell((x + j, y + i))            
            if self.board[x][y] == 10:
                end_screen(0)
        for i in self.board:
            if -1 not in i:
                n += 1
        if n == len(self.board):
            end_screen(1)
    
    def flag(self, cell):
        x, y = cell
        if x >= 0 and x < self.width and y >= 0 and y < self.height: 
            print(self.board[x][y])
            if self.board[x][y] == -1:
                self.board[x][y] = -2
            elif self.board[x][y] == 10:
                self.board[x][y] = -20  
            elif self.board[x][y] == -2:
                self.board[x][y] = -1
            elif self.board[x][y] == -20:
                self.board[x][y] = 10

        
class GUI:
    def __init__(self):
        self.elements = []
        
    def add_element(self, element):
        self.elements.append(element)
        
    def render(self, surface):
        for element in self.elements:
            render = getattr(element, 'render', None)
            if callable(render):
                element.render(surface)
                
    def update(self):
        for element in self.elements:
            update = getattr(element, 'update', None)
            if callable(update):
                element.update()
                
    def get_event(self, event):
        for element in self.elements:
            get_event = getattr(element, 'get_event', None)
            if callable(get_event):
                element.get_event(event)        


class Label:
    def __init__(self, rect, text):
        self.Rect = pygame.Rect(rect)
        self.text = text
        self.bgcolor = pygame.Color('white')
        self.font_color = pygame.Color('black')
        self.font = pygame.font.Font(None, self.Rect.height - 4)
        self.rendered_text = None
        self.rendered_rect = None
        
    def render(self, surface):
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        self.rendered_rect = self.rendered_text.get_rect(x=self.Rect.x + 2, 
                                                     centery=self.Rect.centery)
        surface.blit(self.rendered_text, self.rendered_rect)
        
        
class Button(Label):
    buttons = {}
    def __init__(self, rect, text, num):
        super().__init__(rect, text)
        self.bgcolor = pygame.Color('grey')
        self.pressed = False
        self.buttons[num] = rect
    
    def render(self, surface):
        surface.fill(self.bgcolor, self.Rect)
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        if not self.pressed:
            color1 = pygame.Color("white")
            color2 = pygame.Color("black")
            self.rendered_rect = self.rendered_text.get_rect(x=self.Rect.x + 5, centery=self.Rect.centery)
        else:
            color1 = pygame.Color("black")
            color2 = pygame.Color("white")
            self.rendered_rect = self.rendered_text.get_rect(x=self.Rect.x + 7, centery=self.Rect.centery + 2)

        # рисуем границу
        pygame.draw.rect(surface, color1, self.Rect, 2)
        pygame.draw.line(surface, color2, (self.Rect.right - 1, self.Rect.top), (self.Rect.right - 1, self.Rect.bottom), 2)
        pygame.draw.line(surface, color2, (self.Rect.left, self.Rect.bottom - 1),
                         (self.Rect.right, self.Rect.bottom - 1), 2)
        # выводим текст
        surface.blit(self.rendered_text, self.rendered_rect)
        
    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos 
            if x > self.Rect.left and x < self.Rect.width+self.Rect.left and y > self.Rect.top and y < self.Rect.height + self.Rect.top:
                self.pressed = self.Rect.collidepoint(event.pos)
             
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            x, y = event.pos
            for i in self.buttons.keys():
                coor = self.buttons[i]
                print(((i, coor), x > coor[0] and x < coor[0] + coor[2] and y > coor[1] and y < coor[1] + coor [3]))
                if x > coor[0] and x < coor[0] + coor[2] and y > coor[1] and y < coor[1] + coor [3]:
                    self.pressed = False
                    button_open(i)
                    
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, colums, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, colums, rows)
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.rect.move(x, y)
        
    def cut_sheet(self, sheet, colums, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // colums, 
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(colums):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location,
                                                                self.rect.size)))
                
    def update(self):
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.image = self.frames[self.current_frame]
            
pygame.init()

fps = 50
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
fon = pygame.sprite.Group()
mines = pygame.sprite.Group()
gui = GUI()

gui.add_element(Label((100, 0, 90, 90), "САПЕР"))
gui.add_element(Button((145, 340, 110, 50), "СТАРТ", 0))

size = width, height = 400, 400
screen = pygame.display.set_mode(size)
running = True
fonn = pygame.sprite.Sprite()
mine_img = pygame.sprite.Sprite()
img = load_image("boom.png")
boom = AnimatedSprite(img, 5, 5, 100, 100)
fonn.image = load_image("fon.png")
fonn.rect = fonn.image.get_rect()
fon.add(fonn)
mine_img.image = pygame.transform.scale(load_image("flag.jpg"), (20, 20))
mine_img.rect = mine_img.image.get_rect()
mines.add(mine_img)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        gui.get_event(event)
    fon.draw(screen)
    gui.render(screen)
    gui.update()  
    all_sprites.draw(screen)
    all_sprites.update()
    clock.tick(50)    
    pygame.display.flip()
    
pygame.quit()