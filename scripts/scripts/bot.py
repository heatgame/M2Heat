# -*- coding:utf-8 -*-
from root import job_manager
import logger
import config
import helper
import playerm2g2 as player
import b0t
from utility import finder
from utility import pos
import utility
from hack_manager import hack_manager
import teleport_manager
from teleport_manager import teleport

class load():
	def __init__(self):
		self.index = None
		self.back = False
		self.route_name = None
		self.interval = 100
		self.job = job_manager.job_manager.add_job(self)
		self.a_stone_dead = False

	def __del2__(self):
		job_manager.job_manager.del_job(self)

	def get_closest_way(self, main_instance, route):
		closest_index = 0
		closest_distance = None
		main_position = main_instance.position()

		for index, r in enumerate(route):
			distance = b0t.distance(main_position, r)
			if closest_distance == None or distance < closest_distance:
				if utility.block_control(main_position, r) == False:
					continue
				closest_index = index
				closest_distance = distance
		
		return closest_index

	def find_nearest_mob(self):
		mobs = b0t.mobs(helper.config.attack_types, helper.config.distance)
		main_data = b0t.main_instance()
		
		nearest_distance = helper.config.distance
		nearest_mob_data = None

		for mob in mobs:
			mob_data = mob.data()
			if mob_data.dead():
				continue

			if utility.block_control(main_data.position(), mob_data.position()) == False:
				continue
			
			distance = b0t.distance(main_data.position(), mob_data.position())
			if distance <= nearest_distance:
				nearest_distance = distance
				nearest_mob_data = mob_data
		
		return nearest_mob_data

	def walk(self, main_instance, route):
		if len(route) == 0:
			helper.map.clear_lines()
			return

		if self.index == None:
			self.index = self.get_closest_way(main_instance, route)
			# create new route with a-star algorithm to go closest index
			if b0t.distance(main_instance.position(), route[self.index]) > 6500:
				teleport.go(self.job, main_instance, 'go nearest index', route[self.index], False, True, False)
				return
		
		# follow created route to go closest index
		if 'go nearest index' in teleport_manager.PATH_LIST:
			if teleport.go(self.job, main_instance, 'go nearest index', None) == False:
				return
			else:
				teleport_manager.PATH_LIST.pop('go nearest index')
				
		#
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

		helper.map.clear_lines()
		for index, r in enumerate(route):
			if index < len(route) - 1:
				helper.map.add_line(int(r.x), int(r.y), int(route[index + 1].x), int(route[index + 1].y), 0, 0, 0, 1.0)

	def go_near_metin(self, main_instance):

		if helper.config.attack_types & 32 == False:
			return False

		mobs = utility.sort_distance_to_main(b0t.mobs(32, helper.config.distance), main_instance)

		main_position = main_instance.position()

		for mob in mobs:
			target_position = mob.data().position()

			if b0t.distance(main_position, target_position) < 400:
				return True

			if utility.block_control(main_position, target_position):
				if helper.config.attack_hack or helper.config.skill_hack or helper.config.walk:
					main_instance.move(target_position)
				else:
					b0t.player.on_press_actor(mob.data().vid(), True)
				self.a_stone_dead = True
				return True

		return False

	def loop(self):
		main_instance = b0t.main_instance()
		if main_instance and hack_manager.botting:
			if helper.config.attack_hack or helper.config.skill_hack or helper.config.walk:
				if main_instance.dead():
					return

				if self.go_near_metin(main_instance):
					return

				if self.a_stone_dead:
					self.job.wait_for(3000)
					self.a_stone_dead = False
					return

				if helper.route.name() != self.route_name:
					self.route_name = helper.route.name()
					self.index = None
				
				route = helper.route.current()
				self.walk(main_instance, route)

			else:
				nearest_mob = self.find_nearest_mob()
				if nearest_mob:
					vid = nearest_mob.vid()
					b0t.player.on_press_actor(vid, True)
		else:
			self.index = None

script = load()
