# -*- coding:utf-8 -*-
from root import job_manager
import logger
import config
import helper
import playerm2g2 as player
import b0t

class load():
	def __init__(self):
		self.interval = 250
		job_manager.job_manager.add_job(self)

	def __del2__(self):
		job_manager.job_manager.del_job(self)

	def find_potions(self, red = True):
		for i in range(90):
			item_vnum = b0t.player.get_item_index(i)
			if red:
				if item_vnum >= 27001 and item_vnum <= 27003:
					return i
				if (item_vnum >= 27201 and item_vnum <= 27203) or (item_vnum == 27122 or item_vnum == 27051 or item_vnum == 70390):
					return i
			else:
				if item_vnum >= 27004 and item_vnum <= 27006:
					return i

		return -1

	def loop(self):
		if helper.config.auto_potion == False:
			return

		main_instance = b0t.main_instance()
		if main_instance:
			if main_instance.dead() is True:
				return
			
			hp = player.GetStatus(player.HP)
			sp = player.GetStatus(player.SP)

			max_hp = player.GetStatus(player.MAX_HP)
			max_sp = player.GetStatus(player.MAX_SP)

			if hp < max_hp / 100 * helper.config.auto_potion_percent:
				slot = self.find_potions()
				if slot != -1:
					b0t.network.item_use(slot)

			if sp < max_sp / 100 * helper.config.auto_potion_percent:
				slot = self.find_potions(False)
				if slot != -1:
					b0t.network.item_use(slot)


script = load()

