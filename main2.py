import random as r
import pygame as pg
import sys


class Setup():
    def __init__(self):
        
        self.display_width = 400
        self.display_height = 700
        self.screen = pg.display.set_mode((self.display_width,self.display_height))
        self.title = "Wordlinator"


        self.word_list = open("words.txt").read().splitlines()
        self.possible_answer = open("possible_answer.txt").read().splitlines()
        
        self.font = pg.font.Font(None, 36)
        self.font_title = pg.font.Font("BebasNeue-Regular.ttf", 40)
        self.font_letter = pg.font.Font("BebasNeue-Regular.ttf", 25)

        self.letters1 = [["q", "w", "e", "r", "t", "z", "u", "i", "o", "p"],
                         ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
                         ["y", "x", "c", "v", "b", "n", "m"]]
        
        self.letters_count = 10
        self.letters_size = 25
        self.letters_gap = 5
        self.letters_row_width = self.letters_count * (self.letters_size + self.letters_gap) - self.letters_gap
        self.x = (self.display_width - self.letters_row_width) //2  


    
    def draw_headline(self, center):
        title = self.font_title.render(self.title.upper(), True, (255,255,255))
        title_render = title.get_rect(center = (center, 50))
        self.screen.blit(title, title_render)
    
    def draw_letters(self):
        x = self.x
        y = 500
        def draw(letter, posx, posy):
            letters = self.font_letter.render(letter.upper(), True, (255,255,255))
            letters_render = letters.get_rect(topleft = (posx, posy))
            self.screen.blit(letters, letters_render)

        for letts in self.letters1:
            for i in letts:
                draw(i, x, y)
                x += self.letters_size + self.letters_gap 

            x = self.x
            y += self.letters_size + self.letters_gap    


class Tiles():
    def __init__(self):
        self.setup = Setup()
        self.y = 100
        self.size = 50
        self.gap = 5
        self.row_width = 5 * (self.size + self.gap) - self.gap
        self.x = (self.setup.display_width - self.row_width) //2   

class Game_state():
    def __init__(self):
        self.setup = Setup()
        self.rect_list = []
        self.check_list = []
        self.active_state = []
        self.rendered_text = []
        
        self.active_pos = 0
        self.click_change = False

        self.row = 0
        self.row_start = self.row * 5
        self.row_end = self.row_start + 5

        self.random_word = self.get_random_word(self.setup.possible_answer)


    def get_random_word(self, word_l):
            return r.choice(word_l)
    
    
    def rect_list_init(self, T):
        y = T.y
        x = T.x
        for rows in range(6): # rect_list obsahuje info(pozice) o polich -> zabarveni + pisma
            for cols in range(5):
                list_rect = pg.draw.rect(self.setup.screen, color="#000000", rect= (x, y, T.size, T.size))
                self.rect_list.append(list_rect)
                x += T.size + T.gap
                if cols == 4:
                    x = (self.setup.display_width - T.row_width) //2
                    y += T.size + T.gap


    def setup_lists(self):    #setup vsech listu
        if not self.active_state: 
            self.active_state = [False] * len(self.rect_list)
            self.active_state[0] = True
            self.rendered_text = [""] * len(self.rect_list)
            self.check_list = ["⬜"] * len(self.rect_list)
    

    def render_text(self, letter):
        for i, x in enumerate(self.rect_list):
            if i < len(self.active_state) and self.active_state[i] == True:
                if self.row_start <= i < self.row_end:
                    if self.rendered_text[i] == "" or self.click_change:
                        self.rendered_text[i] =f"{letter}"
                        self.active_pos = i
                        self.active_state[i] = False
                        self.click_change = False

    
    def click(self, mouse_pos):
        for i, rect in enumerate(self.rect_list):
            if rect.collidepoint(mouse_pos):
                if self.row_start <= i < self.row_end:
                        self.active_state = [False] * len(self.rect_list)
                        self.active_state[i] = True
                        self.active_pos = i
                        self.click_change = True
                        break
        else:
            pass

    def draw_checked_rects(self, T):
        y = T.y
        x = T.x

        for i,c1 in enumerate(self.rect_list): # kontrola barev
            if self.check_list[i] == "🟩":
                checked_color = "#22AE15"
            elif self.check_list[i] == "🟨":
                checked_color = "#E9A112"
            else:
                checked_color = "#000000"
 
            pg.draw.rect(self.setup.screen, color=checked_color, rect= (x, y, T.size, T.size))
            pg.draw.rect(self.setup.screen, color="#473F3F", rect= (x, y, T.size, T.size), width= 3)


            x += T.size + T.gap # posun poli

            if (i+1) % 5 == 0: #novy radek kdyz dojde na posledni pole radku
                x = T.x
                y += T.size + T.gap
    
    def draw_text(self):
        for i, text in enumerate(self.rendered_text):
            if text:
                # if self.row_start <= i < self.row_end:
                    rect = self.rect_list[i]
                    text_to_blit = self.setup.font.render(text.upper(), True, (255,255,255))
                    text_rect = text_to_blit.get_rect(center=rect.center)
                    self.setup.screen.blit(text_to_blit,text_rect)
        None
    
    def check_text(self, answer):
        word_store = "".join(self.rendered_text[self.row_start:self.row_end])
        if len(word_store) == 5:
            if word_store in self.setup.word_list:
                    for i ,(c1, c2) in enumerate(zip(self.rendered_text[self.row_start:self.row_end], answer)):  ### zip paruje pismena ve slove v danem radku s resenim
                        if c1 == c2 :                                                                            ### enumerate ocisluje tuple s pismeny -> zjisteni pozice
                            self.check_list[self.row_start + i] = "🟩"                                          ###                  
                        elif c1 in answer:                                                                       ### napr guess = PACER, answer = LAKER -> i == 0, c1 == P, c2 == L -> checklist[0] =="⬜"
                            self.check_list[self.row_start + i] = "🟨"                                          ###                                        i == 1, c1 == A, c2 == A -> checklist[1] =="🟩"                                   
                        else:
                            self.check_list[self.row_start + i] = "⬜"
                            for z, ls in enumerate(gs.setup.letters1):
                                for y ,i in enumerate(ls):
                                    if c1 == i:
                                        gs.setup.letters1[z][y] = "_"


                    if self.row < 5: # posun radku
                        self.row += 1
                        self.row_start = self.row * 5
                        self.row_end = self.row_start + 5
                        self.active_state[self.row_start] = True

        None
    
    def delete_text(self):
        if self.row_start <= self.active_pos < self.row_end:
            self.rendered_text[self.active_pos] = ""
            if self.active_pos > 0 and self.active_pos > self.row_start:
                self.active_pos -= 1
            for i in range(len(self.active_state)):
                self.active_state[i] = (i == self.active_pos) # (i==active_pos) hodí True-False

class Wordlinator():
    def __init__(self):
        self.gamestate = Game_state()
        self.tiles = Tiles()

    def mainloop(self, gs):
        clock = pg.time.Clock()
        pg.display.set_caption("Wordlinator")
        gs.rect_list_init(self.tiles)
        gs.setup_lists()
        while True:
            for event in pg.event.get():
                    if event.type == pg.QUIT:
                        sys.exit()
                    if event.type == pg.MOUSEBUTTONDOWN :
                        gs.click(event.pos)
                    if event.type == pg.KEYDOWN:
                        letter = event.unicode
                        if letter.isalpha() and letter.lower() in "abcdefghijklmnopqrstuvwxyz":
                            if gs.rendered_text[gs.active_pos] != "":
                                if gs.active_pos < gs.row_end-1:
                                    if (gs.active_pos+1) < len(gs.active_state):
                                        gs.active_state[gs.active_pos+1] = True
                                        gs.active_pos += 1
                            gs.render_text(letter)
                            if gs.active_pos < gs.row_end-1:
                                if (gs.active_pos+1) < len(gs.active_state):
                                    gs.active_state[gs.active_pos+1] = True
                        if event.key == pg.K_BACKSPACE:
                            gs.delete_text()
                        if event.key == pg.K_RETURN:
                            gs.check_text(gs.random_word)             

            gs.setup.screen.fill((0,0,0))
            gs.setup.draw_headline(gs.setup.display_width / 2)
            gs.draw_checked_rects(self.tiles)
            gs.setup.draw_letters()
            gs.draw_text()          
                        
            pg.display.update()
            clock.tick(60)

if __name__ == "__main__":
    pg.init()
    game = Wordlinator()
    gs = Game_state()
    game.mainloop(gs)
        