import pygame as pg
import sys
from os import path
from sprites import *
from settings import *
from text import *

class Game:
	def __init__(self):
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		# pg.display.set_caption(TITLE)
		self.clock = pg.time.Clock()
		pg.key.set_repeat(500, 100)
		self.load_data()
		self.draw_cg = False
		self.min_max = True
		self.line_draw = False
		self.show_trace = False

	def load_data(self):
		game_folder = path.dirname(__file__)
		img_folder = path.join(game_folder, 'img')
		self.planet_img = [pg.image.load(path.join(img_folder, 'planet.png')).convert_alpha(),
		pg.image.load(path.join(img_folder, 'planet2.png')).convert_alpha(),
		pg.image.load(path.join(img_folder, 'planet3.png')).convert_alpha(),
		pg.image.load(path.join(img_folder, 'planet4.png')).convert_alpha(),
		pg.image.load(path.join(img_folder, 'planet5.png')).convert_alpha()]
		self.collide_planet = pg.image.load(path.join(img_folder, 'on_fire.png')).convert_alpha()
		self.center_icon = pg.image.load(path.join(img_folder, 'center.png')).convert_alpha()

	def new(self):
		self.start_time = pg.time.get_ticks()
		self.all_sprites = pg.sprite.Group()
		if self.show_trace:
			self.screen.fill((0, 0, 50))
			self.text()

		self.planets = [Planet(self) for i in range(NUMBER_OF_PLANETS)]

		self.cg_group = pg.sprite.Group()
		self.center_of_gravity = CenterGravity(self)

	def run(self):
		#gameloop - self.playing = False => game over
		self.playing = True
		while self.playing:
			self.dt = self.clock.tick(FPS) / 1000
			self.events()
			self.start = pg.time.get_ticks()
			self.update()
			self.draw()

	def quit(self):
		pg.quit()
		sys.exit()

	def update(self):
		self.all_sprites
		for sprite in self.all_sprites:
			self.all_sprites.remove(sprite) # remove current sprite
			sprite.update(self.all_sprites) # update
			self.collision_game(sprite, self.all_sprites) # check for collision
			self.all_sprites.add(sprite) # add current sprite again

			#setting boundaries
			if sprite.rect.left > WIDTH or sprite.rect.right < 0 or sprite.rect.top > HEIGHT or sprite.rect.bottom < 0:
				sprite.kill()

		#restart if only one planet left (migth change to 0)
		if len(self.all_sprites) == 1:
			self.new()

		if self.draw_cg:
			self.center_gravity()
			self.cg_group.update()

		self.keypress()

	def collision_game(self, sprite, group, dokill=False):
		now = pg.time.get_ticks()
		if now - self.start_time > 1000: # 1000 = 1s
			collide = pg.sprite.spritecollide(sprite, group, True)
			if collide:
				sprite.collision(collide[0])

	def draw(self):
		# show FPS
		pg.display.set_caption('{:.2f}'.format(self.clock.get_fps()))

		if self.show_trace:
			self.background = self.screen.copy()
			self.background.blit(self.screen, (0, 0, 0, 0))
			self.background.fill((0, 0, 50, 100))
		else:
			self.screen.fill((0, 0, 50))
			self.text()

		self.all_sprites.draw(self.screen)

		self.cg_group.draw(self.screen)

		# draw lines
		self.draw_lines()

		pg.display.flip()

	def text(self):
		# draw text
		draw_text(self.screen, 'Planets = %s (use arrowkeys up/down to change)' % NUMBER_OF_PLANETS, 20, 10, 12, WHITE)
		draw_text(self.screen, 'Show CG = %r (press Return)' % self.draw_cg, 20, 10, 12*2, WHITE)
		draw_text(self.screen, 'Show line to CG = %r (first, "show CG" must be active, then press L)' % self.line_draw, 20, 10, 12*3, WHITE)
		draw_text(self.screen, 'Set speed boundary = %r (press Backspace)' % self.min_max, 20, 10, 12*4, WHITE)
		draw_text(self.screen, 'Show trace of planets = %r' % self.show_trace, 20, 10, 12*5, WHITE)
		draw_text(self.screen, 'Press R to restart', 20, 10, 12*6, WHITE)


	def events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.quit()
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.quit()

	def draw_lines(self):
		if self.line_draw and self.draw_cg:
			for sprite in self.all_sprites:
				pg.draw.aaline(self.screen, LIGHTBLUE, sprite.pos, self.center_of_gravity.pos)

	def center_gravity(self):
		# tot_m = sum([sprite.mass for sprite in self.all_sprites])
		if self.draw_cg:
			centerGravity_x = []
			centerGravity_y = []
			tot_m = []
			for sprite in self.all_sprites:
				centerGravity_x.append(sprite.pos.x*sprite.mass)
				centerGravity_y.append(sprite.pos.y*sprite.mass)
				tot_m.append(sprite.mass)

			tot_mass = sum(tot_m)
			self.cg_pos_x = sum(centerGravity_x)/tot_mass
			self.cg_pos_y = sum(centerGravity_y)/tot_mass

	def keypress(self):
		global NUMBER_OF_PLANETS
		keys = pg.key.get_pressed()
		if keys[pg.K_r]:
			self.new()
		if keys[pg.K_UP]:
			if NUMBER_OF_PLANETS < 60:
				NUMBER_OF_PLANETS += 1
		if keys[pg.K_DOWN]:
			if NUMBER_OF_PLANETS > 2:
				NUMBER_OF_PLANETS -= 1
		if keys[pg.K_RETURN]:
			if self.draw_cg:
				self.draw_cg = False
			else:
				self.draw_cg = True
		if keys[pg.K_BACKSPACE]:
			if self.min_max:
				self.min_max = False
			else:
				self.min_max = True
		if keys[pg.K_l]:
			if self.line_draw:
				self.line_draw = False
			else:
				self.line_draw = True
		if keys[pg.K_SPACE]:
			if self.show_trace:
				self.show_trace = False
			else:
				self.show_trace = True

g = Game()
while True:
	g.new()
	g.run()
