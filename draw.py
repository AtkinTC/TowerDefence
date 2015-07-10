import sys, pygame
from pygame.locals import *
import pygame.font
import pygame.image
import pygame.transform

w, h = 320,240
screen = None
font = None

tile = None

image_dict = {}
image_dict_large = -1

def t_add(t1,t2):
    return map(lambda a,b: a+b,t1,t2)

def init(width=320, height=240):
    global screen, w, h, font, tile
    w = width
    h = height
    screen = pygame.display.set_mode((w,h))
    screen.fill((0,0,0))
    pygame.font.init()
    font = pygame.font.SysFont(None, 15)

def load_image(name, alpha=False):
    global image_dict, image_dict_large
    im = pygame.image.load(name)
    if alpha:
        im = im.convert_alpha(screen)
    else:
        im = im.convert(screen)

    id = 0
    while id in image_dict:
        id += 1
    image_dict_large = max(image_dict_large, id)
    image_dict[id] = im
    return id

def draw_image(id, x, y, area=None, angle=0):
    im = image_dict.get(id, None)
    if im:
        if angle:
            im = pygame.transform.rotate(im, angle)
        screen.blit(im, (x,y), area)

def fill(x, y, w, h, r, g, b):
    screen.fill((r,g,b),(x,y,w,h))

def draw_point(pos, r, g, b):
    pygame.draw.line(screen, (r,g,b), pos, pos, 1)
        
def draw_line(pos1, pos2, r, g, b, width=1):
    pygame.draw.line(screen, (r,g,b), pos1, pos2, width)

def draw_circle(pos, rad, r, g, b):
    pygame.draw.circle(screen, (r,g,b), pos, rad)

def draw_arc(pos, rad, ang1, ang2, r, g, b, width=1):
    rect = (pos[0]-rad, pos[1]-rad, rad*2, rad*2)
    pygame.draw.arc(screen, (r,g,b), rect, ang1, ang2, width)

def draw_poly(poly, r, g, b):
    poly.append(poly[0])
    for i in range(len(poly)-1):
        draw_line(poly[i], poly[i+1], r,g,b)

def draw_text(text, pos, r,g,b):
    text = font.render(text, True, (r,g,b))
    screen.blit(text, pos)

def flip(col = (0,0,0)):
    pygame.display.flip()
    screen.fill(col)
