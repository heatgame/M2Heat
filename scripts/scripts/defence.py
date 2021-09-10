# -*- coding:utf-8 -*-
from root import job_manager
import logger, timer
import config
import helper
import playerm2g2 as player
import b0t
from utility import finder
from utility import pos
from hack_manager import hack_manager

class load():
	def __init__(self):
		self.interval = 600
		self.auto_tick = 0
		self.vids = []
		job_manager.job_manager.add_job(self)

	def __del2__(self):
		job_manager.job_manager.del_job(self)
		
	def check_pk_players(self):
		for mob in b0t.mobs(8, 20000):
			mob_data = mob.data()
			if mob_data == None:
				continue

			if mob_data.pk() == False and mob_data.alignment() > 0:
				continue

			vid = mob_data.vid()
			if vid in self.vids:
				continue
			
			logger.trace('FOUND PK PLAYER: ' + mob_data.name() + ' VID: ' + str(vid))

			self.vids.append(vid)

	def send_auto(self, vid, mob_pos):
		b0t.network.fly_targeting(vid, mob_pos)
		b0t.network.shoot(0)
		
	def loop(self):
		main_instance = b0t.main_instance()
		if main_instance == None or hack_manager.botting == False:
			return

		self.check_pk_players()

		if main_instance.dead():
			return

		for vid in self.vids:
		 	self.send_auto(vid, b0t.pos(0, 0, 0))

script = load()
