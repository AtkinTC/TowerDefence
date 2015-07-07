import sys, pygame
from pygame.locals import *
import pygame.font

w, h = 320,240
screen = None
font = None

def t_add(t1,t2):
    return map(lambda a,b: a+b,t1,t2)

def init(width=320, height=240):
    global screen, w, h, font
    w = width
    h = height
    screen = pygame.display.set_mode((w,h))
    screen.fill((0,0,0))
    pygame.font.init()
    font = pygame.font.SysFont(None, 15)

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
