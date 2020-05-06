import pygame as pg
from settings import *
from random import randint, uniform, choice
vec = pg.math.Vector2

class Planet(pg.sprite.Sprite):
	def __init__(self, game):
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.choice = choice(self.game.planet_img)
		self.image = self.choice
		self.rect = self.image.get_rect()
		self.pos = vec(randint(100, WIDTH - 100), randint(100, HEIGHT - 100))
		self.vel = vec(randint(-30, 30), randint(-30, 30))
		self.acc = vec(0, 0)
		self.mass = randint(50, 100) #35-60
		self.size = self.mass ** (1/2)
		self.force = 0
		self.rot = 0
		self.rect.center = self.pos
		self.image = pg.transform.scale(self.choice, (int(self.size), int(self.size)))

	def update(self, other_list):
		acc_list_x = []
		acc_list_y = []
		for other in other_list:
			self.force = G * (self.mass**2 * other.mass**2) / (self.pos.distance_to(other.pos) ** 2)
			self.rot = (other.pos - self.pos).angle_to(vec(1, 0))
			self.image = pg.transform.scale(self.choice, (int(self.size), int(self.size)))
			self.rect = self.image.get_rect()
			self.rect.center = self.pos
			self.acc = vec(self.force/self.mass, 0).rotate(-self.rot)

			#separating out the components of acceleration and summing list for accurate movement
			acc_list_x.append(self.acc.x)
			acc_list_y.append(self.acc.y)

		self.acc_x = sum(acc_list_x)
		self.acc_y = sum(acc_list_y)
		if self.game.min_max:
			self.acc_x = min(max(self.acc_x, -25), 25)
			self.acc_y = min(max(self.acc_y, -25), 25)
		self.acc = vec(self.acc_x, self.acc_y)
		self.vel += self.acc * self.game.dt
		self.pos += self.vel * self.game.dt

	def draw_line(self, surf):
		moves = [self.pos, self.pos]
		corr_moves = list(moves)
		moves.append(self.pos)
		pg.draw.lines(surf, (255, 255, 255), False, corr_moves, 10)
	
	def collision(self, other):
		#conservation of energy
		self.choice = self.game.collide_planet
		self.vel = (self.mass * self.vel + other.mass * other.vel) / (self.mass + other.mass)
		self.mass += other.mass

class CenterGravity(pg.sprite.Sprite):
	def __init__(self, game):
		self.groups = game.cg_group
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = self.game.center_icon
		self.rect = self.image.get_rect()
		self.pos = vec(0, 0)
		self.rect.midbottom = self.pos

	def update(self):
		self.image = self.game.center_icon
		self.rect = self.image.get_rect()
		self.rect.midbottom = self.pos
		self.pos = vec(self.game.cg_pos_x, self.game.cg_pos_y)