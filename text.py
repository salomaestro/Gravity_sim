import pygame as pg
from settings import *

pg.font.init()

FONT_TYPE = pg.font.match_font('freesansbold.ttf')

def draw_text(surf, text, size, x, y, color, font_name=FONT_TYPE):
	font = pg.font.Font(font_name, size)
	text_surface = font.render(text, True, color)
	text_rect = text_surface.get_rect()
	text_rect = (x, y)
	surf.blit(text_surface, text_rect)