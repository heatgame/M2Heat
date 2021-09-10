# -*- coding:utf-8 -*-
from root import job_manager
import logger
import config
import helper
import playerm2g2 as player
import m2netm2g as net
import b0t
from utility import finder
from utility import pos
import utility
from hack_manager import hack_manager

class load():
	def __init__(self):
		self.temp_item_list = list()
		self.interval = 300
		self.drop_item_loop_counter = 0
		job_manager.job_manager.add_job(self)

	def __del2__(self):
		job_manager.job_manager.del_job(self)

	def pickup(self, item):
		const_cpos = pos().conv(b0t.main_instance().position())
		current_cpos = pos().conv(b0t.main_instance().position())

		item_position = item.data().position()

		if b0t.background.blocked(item_position.x, item_position.y):
			return False

		for point in finder.find(current_cpos, pos().conv(item_position), 100):
			if b0t.background.blocked(point.x, point.y):
				return False

		for point in finder.find(current_cpos, pos().conv(item_position), 1000):
			tpos = b0t.pos(point.x, point.y, point.z)
			b0t.network.state(tpos, 0, 0, 0)

		current_cpos = pos().conv(item.data().position())
		b0t.network.pickup(item.key())

		for point in finder.find(current_cpos, const_cpos, 1000):
			tpos = b0t.pos(point.x, point.y, point.z)
			b0t.network.state(tpos, 0, 0, 0)
		
		# vnum = item.data().vnum()
		# if vnum != 1:
		# 	item_data = helper.item(vnum)
		# 	logger.trace('name: ' + item_data.name() + ' pos: ' + str(item_position.x) + ' ' + str(item_position.y))

		return True

	def find_item_index(self, item):
		for i in range(90):
			item_vnum = b0t.player.get_item_index(i)
			if item_vnum == item:
				return i
		return -1

	def drop_attributeless_item(self, index):
		if index == -1:
			return False
		(btype, svalue) = player.GetItemAttribute(index, 0)
		if btype == 0 or btype == -1:
			net.SendItemDropPacketNew(index, 1)
		return True
	
	def drop_item_loop(self):
		if self.drop_item_loop_counter == 3:
			for temp_item in self.temp_item_list:
				index = self.find_item_index(temp_item)
				if self.drop_attributeless_item(index):
					self.temp_item_list = [x for x in self.temp_item_list if x != temp_item]
					self.drop_item_loop_counter = 0
					break
		else:
			self.drop_item_loop_counter += 1

	def loop(self):
		main_instance = b0t.main_instance()
		if main_instance and hack_manager.picking:
			if main_instance.dead() is True:
				return
			
			items = b0t.items(helper.config.distance)
			items = utility.sort_distance_to_main(items, main_instance)
			
			for item in items:
				# vnum = item.data().vnum()
				# item_data = helper.item(vnum)
				# if (vnum != 1 and item_data.sell_price() >= 1000) or vnum == 79505:
				if item.data().vnum() != 1:
					self.pickup(item)
					return
			
			for item in items:
				if item.data().vnum() == 1:
					if self.pickup(item):
						return

script = load()
