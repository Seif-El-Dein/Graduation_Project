import pygame
from pygame.locals import *

pygame.init()

#screen_width = 440
#screen_height = 435

#screen = pygame.display.set_mode((screen_width, screen_height))
#pygame.display.set_caption('Manual Control')

font = pygame.font.SysFont('Constantia', 15)

# define colours
bg = (128, 128, 128)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)

# define global variable
clicked = False
counter = 0


class Button():
    # colours for button and text
    button_col = (248, 248, 255)
    hover_col = (75, 225, 255)
    click_col = (50, 150, 255)
    text_col = black
    width = 140
    height = 60

    def __init__(self, x, y, text, screen):
        self.x = x
        self.y = y
        self.text = text
        self.screen = screen

    def draw_button(self):

        global clicked
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # create pygame Rect object for the button
        button_rect = Rect(self.x, self.y, self.width, self.height)

        # check mouseover and clicked conditions
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(self.screen, self.click_col, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
            else:
                pygame.draw.rect(self.screen, self.hover_col, button_rect)
        else:
            pygame.draw.rect(self.screen, self.button_col, button_rect)

        # add shading to button
        pygame.draw.line(self.screen, white, (self.x, self.y), (self.x + self.width, self.y), 2)
        pygame.draw.line(self.screen, white, (self.x, self.y), (self.x, self.y + self.height), 2)
        pygame.draw.line(self.screen, black, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        pygame.draw.line(self.screen, black, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)

        # add text to button
        text_img = font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        self.screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 25))
        return action