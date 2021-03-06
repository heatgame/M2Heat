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
from defence import script as defence
from hack_manager import hack_manager

class load():
	def __init__(self):
		self.interval = 100
		self.race = None
		job_manager.job_manager.add_job(self)

	def __del2__(self):
		job_manager.job_manager.del_job(self)

	def get_mob_from_vid(self, vid):
		mobs = b0t.mobs(8, helper.config.distance)
		for mob in mobs:
			mob_data = mob.data()
			if mob_data.dead():
				continue

			if mob_data.vid() != vid:
				continue

			return mob
		
		return None
	
	def reset_interval(self, current_race):
		if current_race == 1 or current_race == 5:
			self.interval = 100
		else:
			self.interval = 300
		self.race = current_race

	def loop(self):
		main_instance = b0t.main_instance()
		if main_instance and hack_manager.botting and (helper.config.attack_hack or helper.config.skill_hack):
			if main_instance.dead() is True:
				return
			
			current_race = player.GetRace()

			if self.race != current_race:
				self.reset_interval(current_race)

			mobs = utility.sort_distance_to_main(b0t.mobs(helper.config.attack_types, helper.config.distance), main_instance)

			# DEFENCE

			for v in defence.vids:

				mob = self.get_mob_from_vid(v)
				if mob == None:
					continue

				mobs.append(mob)

			# DEFENCE_END

			main_position = pos().conv(main_instance.position())
			temp_position = main_position

			hit_counter = helper.config.hit_limit
			temp = list()

			for mob in mobs:		

				if len(temp) >= 20 or hit_counter == 0:
					break

				mob_data = mob.data()
				mob_position = mob_data.position()
				if b0t.background.blocked(mob_position.x, mob_position.y):
					continue

				block_found = False
				for p in finder.find(temp_position, pos().conv(mob_position), 100):
					if b0t.background.blocked(p.x, p.y):
						block_found = True
						break

				if block_found:
					continue

				for p in finder.find(temp_position, pos().conv(mob_position), 1000):
					n_pos = b0t.pos(p.x, p.y, p.z)
					b0t.network.state(n_pos, 0, 0, 0)
					temp.append(n_pos)

				temp_position = pos().conv(mob_position)

				race = player.GetRace()
				if helper.config.skill_hack and (race == 1 or race == 5):
					for i in range(5):
						b0t.network.add_fly_targeting(mob_data.vid(), mob_position)
					b0t.network.shoot(35)
					if helper.config.attack_hack:
						b0t.network.attack(0, mob_data.vid())
				elif helper.config.attack_hack:
					b0t.network.attack(0, mob_data.vid())

				if hit_counter != 100:# unlimited value is 100
					hit_counter -= 1

			blocked = False

			for p in finder.find(temp_position, main_position, 100):
				if b0t.background.blocked(p.x, p.y):
					# logger.trace('block')
					blocked = True
					break
			
			if blocked:
				# logger.trace('temp_size ' + str(len(temp)))
				temp.reverse()
				for p in temp:
					b0t.network.state(p, 0, 0, 0)
			else:
				for p in finder.find(temp_position, main_position, 1000):
					n_pos = b0t.pos(p.x, p.y, p.z)
					b0t.network.state(n_pos, 0, 0, 0)

script = load()
