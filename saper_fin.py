import pygame
import sys
import os
from random import choice
from gui import GUI

pygame.init()
size = width, height = 400, 400
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


all_sprites = pygame.sprite.Group()
fon = pygame.sprite.Group()
flags = pygame.sprite.Group()
cells = pygame.sprite.Group()


def terminate():
    pygame.quit()
    sys.exit()


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
    def __init__(self, rect, text):
        super().__init__(rect, text)
        self.bgcolor = pygame.Color('grey')
        self.pressed = False
        self.last_pressed = False

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
        pygame.draw.line(surface, color2, (self.Rect.right - 1, self.Rect.top), (self.Rect.right - 1, self.Rect.bottom),
                         2)
        pygame.draw.line(surface, color2, (self.Rect.left, self.Rect.bottom - 1),
                         (self.Rect.right, self.Rect.bottom - 1), 2)
        # выводим текст
        surface.blit(self.rendered_text, self.rendered_rect)

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.pressed = self.last_pressed = self.Rect.collidepoint(event.pos)
        else:
            self.pressed = False

        if bool(self.pressed) != bool(self.last_pressed):
            return True


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



class Board:
    def __init__(self, width=100, height=100):
        self.width = width
        self.height = height
        self.cell_size = 20
        self.top = 10
        self.left = 10
        self.board = [[-1 for i in range(height)] for k in range(width)]

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, surface):
        cells.empty()
        for h in range(self.height):
            for w in range(self.width):
                if self.board[w][h] == -1 or self.board[w][h] == 10:
                    cell_img = ImageCell(cells, self.left + w * self.cell_size,
                                               self.top + h * self.cell_size)
                    cells.add(cell_img)                    
                    cells.draw(screen)
                    cells.update()                
                if self.board[w][h] == 0:
                    pygame.draw.rect(screen, (210, 210, 210), 
                                     (self.left + self.cell_size * w + 1,
                                      self.top + self.cell_size * h + 1, 
                                      self.cell_size, self.cell_size))
                if self.board[w][h] != 10 and self.board[w][h] != -1 and self.board[w][h] != 0 and self.board[w][h] != -2 and self.board[w][h] != -20:
                    pygame.draw.rect(screen, (170, 170, 170), 
                                     (self.left + self.cell_size * w + 1,
                                      self.top + self.cell_size * h + 1, 
                                      self.cell_size, self.cell_size))                    
                    text = self.font.render(str(self.board[w][h]), 1, self.font_color)
                    screen.blit(text, (self.left + w * self.cell_size + 1, 
                                       self.top + h * self.cell_size + 1,
                                       self.cell_size,
                                       self.cell_size))   
                pygame.draw.rect(screen, (140, 140, 140),
                                 (self.left + self.cell_size * w, 
                                  self.top + self.cell_size * h,
                                  self.cell_size, self.cell_size), 1)  
                
                

    def on_click(self, cell):
        x, y = cell
        if self.board[y][x] == 0:
            self.board[y][x] = 1

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if ((x - self.left) // self.cell_size < self.width and \
            (x - self.left)) > 0 and ((y - self.top) // self.cell_size < \
                                      self.height and (y - self.top) > 0):
            return (x - self.left) // self.cell_size, \
                   (y - self.top) // self.cell_size

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)


class Flag(pygame.sprite.Sprite):
    flag_image = load_image("flag.jpg")

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image =  pygame.transform.scale(Flag.flag_image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class ImageCell(pygame.sprite.Sprite):
    cell_image = load_image("cell.png")
    
    def __init__(self, group, x, y):
        super().__init__(group)
        self.image =  ImageCell.cell_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y    

class Minesweeper(Board):
    def __init__(self, width, height, mine=0):
        super().__init__(width, height)
        self.mine = mine
        self.font = pygame.font.Font(None, 20)
        self.font_color = pygame.Color('black')
        self.play = True
        self.win = False
        self.flags = {}
        
        coor = 0
        while coor < self.mine:
            coordinat = (choice(range(self.width)), choice(range(self.height)))
            if self.board[coordinat[0]][coordinat[1]] != 10:
                self.board[coordinat[0]][coordinat[1]] = 10
                coor += 1

    def get_top_left(self):
        return self.top, self.left
    
    def mines(self, x, y):
        kol_mine = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == 0 and j == 0):
                    if 0 <= x + i <= len(self.board) - 1 and 0 <= y + j <= len(self.board[0]) - 1:
                        if self.board[x + i][y + j] == 10 or self.board[x + i][y + j] == -20:
                            kol_mine += 1
        self.board[x][y] = kol_mine
        if kol_mine == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    self.open_cell((x + i, y + j))        

    def open_cell(self, cell):
        x, y = cell
        if self.width <= x or x < 0 or self.height <= y or y < 0:
            return
        if self.board[x][y] == 10:
            self.play = False
        if self.board[x][y] == -1:
            self.mines(x, y)
            
    def flag(self, cell):
        global flags
        x, y = cell
        if self.board[x][y] == -1 or self.board[x][y] == 10:
            flag = Flag(flags, x * self.cell_size + self.left, y * self.cell_size + self.top)
            self.flags[(x, y)] = (flag, self.board[x][y])
            self.board[x][y] = -20
            flags.add(flag)

        elif self.board[x][y] == -20:
            self.board[x][y] = self.flags[(x, y)][1]
            del self.flags[(x, y)]
            flags.empty()
            for i in self.flags:
                flags.add(self.flags[i][0])

    def get_click(self, event):
        cell = self.get_cell(event.pos)
        if cell:
            if event.button == 1:
                self.open_cell(cell)
            elif event.button == 3:
                self.flag(cell)

    def get_info(self):
        all_values = [self.board[k][i] for i in range(self.height) for k in range(self.width)]
        if -1 not in all_values:
            self.win = True
            self.play = False
        return self.play, self.win


def start_screen():
    active = True
    size = width, height = 400, 400
    screen = pygame.display.set_mode(size)
    gui = GUI()
    gui.add_element(Label((100, 0, 90, 90), "САПЕР"))
    start_button = Button((145, 330, 110, 50), "СТАРТ")
    speed = 40
    img = load_image("boom.png")
    boom = AnimatedSprite(img, 5, 5, 100, 100)

    fonn = pygame.sprite.Sprite()
    fonn.image = load_image("fon.png")
    fonn.rect = fonn.image.get_rect()
    fon.add(fonn)

    while active:
        screen.fill((0, 0, 0))
        fon.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if start_button.get_event(event):
                active = False
                fon.empty()
                break

        all_sprites.draw(screen)
        all_sprites.update()
        start_button.render(screen)
        gui.render(screen)
        pygame.display.flip()
        clock.tick(speed)


def main():
    active = True
    size = width, height = 400, 400
    screen = pygame.display.set_mode(size)
    font = pygame.font.Font(None, 30)
    textCoord = 10
    gui = GUI()

    gui.add_element(Label((140, 0, 70, 60), "САПЁР"))
    gui.add_element(Label((130, 50, 90, 30), "ПРАВИЛА ИГРЫ"))
    gui.add_element(Label((20, 75, 90, 30), "Нужно открыть все ячейки без мин."))
    gui.add_element(Label((20, 95, 90, 30), "Если вы попадаете на ячейку с миной,"))
    gui.add_element(Label((25, 115, 90, 30), "то вы проигрываете."))
    gui.add_element(Label((20, 135, 90, 30), "Клетки открываются нажатием на "))
    gui.add_element(Label((25, 155, 90, 30), "левую кнопку мыши."))
    gui.add_element(Label((20, 175, 90, 30), "Возможное расположение мины отмечается "))
    gui.add_element(Label((25, 195, 90, 30), "правой кнопкой мыши"))

    buttons = [Button((15, 340, 110, 40), "Новичок"), Button((140, 340, 130, 40), "Любитель"),
               Button((290, 340, 100, 40), "Профи")]

    fon2 = pygame.sprite.Sprite()
    fon2.image = load_image("start.png")
    fon2.rect = fon2.image.get_rect()
    fon.add(fon2)

    while active:
        fon.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            for i in buttons:
                if i.get_event(event):
                    fon.empty()
                    return buttons.index(i)

        gui.render(screen)
        for i in buttons:
            i.render(screen)
        pygame.display.flip()


def end_screen(end):
    active = True
    size = width, height = 400, 400
    screen = pygame.display.set_mode(size)
    gui = GUI()
    end_button = Button((150, 330, 110, 50), "МЕНЮ")
    if end == 0:
        gui.add_element(Label((40, 0, 110, 60), "ВЫ ПРОИГРАЛИ!"))
    if end == 1:
        gui.add_element(Label((40, 0, 110, 60), "ВЫ ВЫИГРАЛИ!"))
    fon2 = pygame.sprite.Sprite()
    fon2.image = load_image("start.png")
    fon2.rect = fon2.image.get_rect()
    fon.add(fon2)
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if end_button.get_event(event):
                active = False
                fon.empty()
                break
        fon.draw(screen)
        gui.render(screen)
        end_button.render(screen)
        pygame.display.flip()


def game(typ):
    active = True
    types = [Minesweeper(9, 9, 10), Minesweeper(13, 13, 40), Minesweeper(19, 19, 80)]
    minesweeper = types[typ]
    fon2 = pygame.sprite.Sprite()
    fon2.image = load_image("start.png")
    fon2.rect = fon2.image.get_rect()
    fon.add(fon2)
    while active:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONUP:
                minesweeper.get_click(event)

        fon.draw(screen)
        minesweeper.render(screen)
        flags.draw(screen)
        play, win = minesweeper.get_info()

        if not play and not win:
            return 0
        elif not play and win:
            return 1

        pygame.display.flip()


start_screen()

while True:
    typ = main()
    end = game(typ)
    flags.empty()
    cells.empty()
    end_screen(end)
