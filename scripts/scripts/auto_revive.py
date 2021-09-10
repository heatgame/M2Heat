# -*- coding:utf-8 -*-
from root import job_manager
import logger
import helper
import playerm2g2 as player, m2netm2g as net
import b0t
import utility
from hack_manager import hack_manager
import math

"""
		if b0t.distance(main_instance.position(), route[self.index]) < 400:
			if self.back == False and self.index >= len(route) - 1:
				self.back = True
			if self.back == False:
				self.index += 1
			
			if self.back == True and self.index <= 0:
				self.back = False
				self.index += 1
			elif self.back == True:
				self.index -= 1

		main_instance.move(route[self.index])
"""

class load():

	PI = 3.14159265359

	def __init__(self):
		self.interval = 1000
		self.job = job_manager.job_manager.add_job(self)
		self.hacks_stopped = False
		self.points = None
		self.points_index = 0

	def __del2__(self):
		job_manager.job_manager.del_job(self)

	def circle(self, theta, x, y, r = 1600):
		radians_between_each_point = 2 * self.PI / 360
		x = x + r * math.cos(radians_between_each_point * theta)
		y = y + r * math.sin(radians_between_each_point * theta)
		return (x, y)

	def turn(self, main_instance):
		main_pos = main_instance.position()
		if self.points == None:
			self.points = list()
			self.points_index = 0
			for i in range(1, 360):
				if i % 40 == 0:
					xy = self.circle(i, main_pos.x, main_pos.y)
					self.points.append(xy)
		else:
			current_pos = self.points[self.points_index]
			pos = b0t.pos(current_pos[0], current_pos[1], 0)
			if b0t.distance(main_pos, pos) < 400:
				self.points_index += 1
				if self.points_index >= len(self.points):
					self.points_index = 0
				return
			main_instance.move(pos)

	def wait_for_hp(self, main_instance):
		hp = player.GetStatus(player.HP)
		max_hp = player.GetStatus(player.MAX_HP)
		if hp < max_hp / 100 * 30:
			self.turn(main_instance)
			return False
		return True

	def loop(self):
		main_instance = b0t.main_instance()
		if main_instance and helper.config.auto_revive:
			main_instance = b0t.main_instance()
			if main_instance.dead() == False:
				if hack_manager.stopped:
					self.interval = 50
					if self.hacks_stopped and self.wait_for_hp(main_instance) == True:
						hack_manager.resume()
						self.points = None
						self.hacks_stopped = False
				return
			else:
				self.interval = 1000

			net.SendCommandPacket(net.PLAYER_CMD_RESTART, 1)

			if self.hacks_stopped == False:
				self.hacks_stopped = True
				hack_manager.stop()

script = load()
