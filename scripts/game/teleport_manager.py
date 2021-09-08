import chr as _chr
import re
import logger
import game, event, m2netm2g as net
import b0t, helper
import map_manager
import utility
from utility import hook
import sys, os

TELEPORTER_VNUM = 9012
OLD_MAN_VNUM = 20009
PATH_LIST = {}

class teleport_t():
	def __init__(self):
		self.first_towns = ['metin2_map_a1', 'metin2_map_b1', 'metin2_map_c1']
		self.second_towns = ['metin2_map_a3', 'metin2_map_b3', 'metin2_map_c3']
		self.graph = {'metin2_map_a1': [('metin2_map_a3', False, 0, 0), ('map_a2', True, 20009, 0), ('map_n_snowm_01', True, 20009, 1)],
					  'metin2_map_a3' : [('metin2_map_monkeydungeon', False, 0, 0), ('metin2_map_n_desert_01', True, 20009, 0), ('metin2_map_n_flame_01', True, 20009, 1), ('metin2_map_guild_01', False, 0, 0), ('metin2_map_a1', False, 0, 0)],
					  'metin2_map_guild_01' : [('metin2_map_a3', False, 0, 0)],
					  'metin2_map_b1' : [('metin2_map_b3', False, 0, 0), ('map_a2', True, 20009, 0), ('map_n_snowm_01', True, 20009, 1)],
					  'metin2_map_b3' : [('metin2_map_monkeydungeon', False, 0, 0), ('metin2_map_n_desert_01', True, 20009, 0), ('metin2_map_n_flame_01', True, 20009, 1), ('metin2_map_guild_02', False, 0, 0), ('metin2_map_b1', False, 0, 0)],
					  'metin2_map_guild_02' : [('metin2_map_b3', False, 0, 0)],
					  'metin2_map_c1' : [('metin2_map_c3', False, 0, 0), ('map_a2', True, 20009, 0), ('map_n_snowm_01', True, 20009, 1)],
					  'metin2_map_c3' : [('metin2_map_monkeydungeon', False, 0, 0), ('metin2_map_n_desert_01', True, 20009, 0), ('metin2_map_n_flame_01', True, 20009, 1), ('metin2_map_guild_03', False, 0, 0), ('metin2_map_c1', False, 0, 0)],
					  'metin2_map_guild_03' : [('metin2_map_c3', False, 0, 0)],
					  'metin2_map_monkeydungeon' : [('metin2_map_a3', False, 0, 0), ('metin2_map_b3', False, 0, 0), ('metin2_map_c3', False, 0, 0)],
					  'metin2_map_n_flame_01' :  [('metin2_map_a3', False, 0, 0), ('metin2_map_b3', False, 0, 0), ('metin2_map_c3', False, 0, 0)],
					  'map_a2' : [('metin2_map_a1', False, 0, 0), ('metin2_map_b1', False, 0, 0), ('metin2_map_c1', False, 0, 0), ('metin2_map_milgyo', False, 0, 0), ('metin2_map_skipia_dungeon_01', True, 20009, -1)],
					  'metin2_map_skipia_dungeon_01' : [('metin2_map_skipia_dungeon_02', False, 0, 0), ('map_a2', True, 20009, -1)],
					  'metin2_map_skipia_dungeon_02' : [('metin2_map_skipia_dungeon_01', False, 0, 0)],
					  'metin2_map_milgyo' : [('map_a2', False, 0, 0), ('metin2_map_deviltower1', True, 20009, -1), ('metin2_map_devilsCatacomb', True, 20009, -1)],
					  'metin2_map_deviltower1' : [('metin2_map_milgyo', False, 0, 0)],
					  'metin2_map_devilsCatacomb' : [('metin2_map_milgyo', True, 20009, -1)],
					  'map_n_snowm_01' : [('metin2_map_a1', False, 0, 0), ('metin2_map_b1', False, 0, 0), ('metin2_map_c1', False, 0, 0), ('metin2_map_trent', False, 0, 0)],
					  'metin2_map_trent' : [('metin2_map_trent02', False, 0, 0), ('map_n_snowm_01', False, 0, 0)],
					  'metin2_map_trent02' : [('metin2_map_trent', False, 0, 0)],
					  'metin2_map_n_desert_01' : [('metin2_map_a3', False, 0, 0), ('metin2_map_b3', False, 0, 0), ('metin2_map_c3', False, 0, 0), ('metin2_map_monkeydungeon_02', False, 0, 0), ('metin2_map_monkeydungeon_03', False, 0, 0), ('metin2_map_WL_01', False, 0, 0), ('metin2_map_spiderdungeon', False, 0, 0)],
					  'metin2_map_spiderdungeon' : [('metin2_map_spiderdungeon_02', True, 20009, -1), ('metin2_map_n_desert_01', False, 0, 0)],
					  'metin2_map_spiderdungeon_02' : [('metin2_map_spiderdungeon_03', False, 0, 0), ('metin2_map_spiderdungeon', True, 20009, -1)],
					  'metin2_map_spiderdungeon_03' : [('metin2_map_spiderdungeon_02', False, 0, 0)],
					  'metin2_map_monkeydungeon_02' : [('metin2_map_n_desert_01', False, 0, 0)],
					  'metin2_map_monkeydungeon_03' : [('metin2_map_n_desert_01', False, 0, 0)],
					  'metin2_map_WL_01': [('metin2_map_nusluck01', False, 0, 0)],
					  'metin2_map_nusluck01': [('metin2_map_WL_01', False, 0, 0)]}

		self.path = []
		self.path_index = 0
		self.curr_npc_position = None
		self.starting_map_name = None
		self.starting_position = None
		self.first_town_r = re.compile('metin2_map_.1')
		self.second_town_r = re.compile('metin2_map_.3')
		self.closest_map_with_vendor = None
		self.send_direct_enter = False
		self.teleport_current_map = None

	def find_all_paths(self, start, end, path=[]):
		if type(start) != tuple:
			return self.find_all_paths((start, False, 0, 0), end, path)
		path = path + [start]
		if start[0] == end:
			path.pop(0)
			return [path]
		if not self.graph.has_key(start[0]):
			return []
		paths = []
		for node, use_tp, tp_vnum, answer in self.graph[start[0]]:
			if not any(node in i for i in path):
				new_paths = self.find_all_paths((node, use_tp, tp_vnum, answer), end, path)
				for new_path in new_paths:
					paths.append(new_path)
		return paths

	def find_shortest_path(self, start, end, path=[]):
		if type(start) != tuple:
			return self.find_shortest_path((start, False, 0, 0), end, path)
		path = path + [start]
		if start[0] == end:
			path.pop(0)
			return path
		if not self.graph.has_key(start[0]):
			return None
		shortest = None
		for node, use_tp, tp_vnum, answer in self.graph[start[0]]:
			if not any(node in i for i in path):
				new_path = self.find_shortest_path((node, use_tp, tp_vnum, answer), end, path)
				if new_path:
					if not shortest or len(new_path) < len(shortest):
						shortest = new_path
		return shortest

	def teleport(self, job, main_instance, target_pos, direct_enter = False):
		if b0t.distance(main_instance.position(), target_pos) < 400 or (self.teleport_current_map != None and self.teleport_current_map != b0t.current_map()):
			self.teleport_current_map = None
			self.send_direct_enter = False
			return True

		if self.teleport_current_map == None:
			self.teleport_current_map = b0t.current_map()

		if direct_enter:
			if self.send_direct_enter:
				net.DirectEnter(0, 0)
				self.send_direct_enter = False
				job.wait_for(7500)
				return False

		main_instance_position = main_instance.position()
		# logger.trace('x: ' + str(main_instance_position.x) + ' y: ' + str(main_instance_position.y))
		# logger.trace('x: ' + str(target_pos.x) + ' y: ' + str(target_pos.y))
		path = helper.astar.find_path(main_instance_position, target_pos, 10000, 1)
		if len(path) == 0:
			return True
		for p in path:
			b0t.network.state(p, 0, 0, 0)

		if direct_enter == False:
			_chr.SetPixelPosition(path[-1].x, path[-1].y, path[-1].z)

		self.send_direct_enter = True
		job.wait_for(2000)

		return False

	def go(self, job, main_instance, name = '', target_pos = None, reverse = False, use_teleport = False, direct_enter = False):
		if use_teleport:
			return self.teleport(job, main_instance, target_pos, direct_enter)
		# add new index, if doesn't exists
		global PATH_LIST
		if (name in PATH_LIST) == False:
			path = helper.astar.find_path(main_instance.position(), target_pos, 10000, 1)
			if len(path) == 0:
				return True
			if reverse:
				PATH_LIST[name] = (len(path) - 1, path)
			else:
				PATH_LIST[name] = (0, path)
		
		index = PATH_LIST[name][0]
		route = PATH_LIST[name][1]
		# go next index, if player close to current index
		is_close = b0t.distance(main_instance.position(), route[index]) < 400
		if reverse and is_close:
			PATH_LIST[name] = (index - 1, route)
		elif is_close:
			PATH_LIST[name] = (index + 1, route)
		# finish the function, if the route is over and delete the item in dictionary list, if the reverse is enabled
		index = PATH_LIST[name][0]
		if index >= len(route) or index < 0:
			if reverse:
				PATH_LIST.pop(name)
			else:
				PATH_LIST[name] = (len(route) - 1, route)
			return True
		# draw lines to map
		helper.map.clear_lines()
		for i, r in enumerate(route):
			if i < len(route) - 1:
				helper.map.add_line(int(r.x), int(r.y), int(route[i + 1].x), int(route[i + 1].y), 0, 0, 0, 1.0)
		# move to current index
		# logger.trace('x: ' + str(route[index].x) + ' y: ' + str(route[index].y) + ' z: ' + str(route[index].z))
		main_instance.move(route[index])
		return False

	def go_to_map(self, job, main_instance, target):
		if not self.path:
			if self.starting_map_name == None:
				self.starting_map_name = b0t.current_map()

			self.path = self.find_shortest_path(b0t.current_map(), target)
			hook.hook((game.GameWindow, 'OpenQuestWindow'), lambda self, skin, idx: None, False)
		
		if self.path_index == len(self.path):
			if b0t.current_map() == target:
				self.path = []
				self.path_index = 0
				hook.unhook((game.GameWindow, 'OpenQuestWindow'))
				return True
			return False

		main_instance_position = main_instance.position()
		target_map = self.path[self.path_index]
		map_name = target_map[0]
		use_npc = target_map[1]
		npc_vnum = target_map[2]
		answer = target_map[3]

		if self.curr_npc_position == None:
			if use_npc:
				self.curr_npc_position = map_manager.get_npc_position(b0t.current_map(), npc_vnum)
			else:
				self.curr_npc_position = map_manager.get_warp_position(b0t.current_map(), map_name)

		if self.go(job, main_instance, map_name, self.curr_npc_position, False, True, True):
			if use_npc:
				npc = utility.get_npc(npc_vnum)
				if npc == 0:
					job.wait_for(1000)
					return False
				
				npc_vid = npc.vid()

				if npc_vnum == 20009:
					b0t.network.state(npc.position(), 0, 0, 0)
					b0t.network.on_click(npc_vid)
					event.SelectAnswer(1, 0)
					event.SelectAnswer(1, 0)
					event.SelectAnswer(1, answer)

			self.curr_npc_position = None
			self.path_index += 1
			global PATH_LIST
			if map_name in PATH_LIST:
				PATH_LIST.pop(map_name)

		return False

	def get_closest_map_with_vendor(self):
		first_town = 'metin2_map_' + chr(96 + net.GetEmpireID()) + '1'
		second_town = 'metin2_map_' + chr(96 + net.GetEmpireID()) + '3'

		path_to_first_town = self.find_shortest_path(self.starting_map_name, first_town)
		path_to_second_town = self.find_shortest_path(self.starting_map_name, second_town)

		if len(path_to_first_town) < len(path_to_second_town):
			return first_town
		return second_town

	def go_to_closest_vendor_or_store(self, job, main_instance, store=False):
		if self.starting_map_name == None:
			self.starting_map_name = b0t.current_map()
			self.starting_position = main_instance.position()

		if not (self.starting_map_name in self.first_towns or self.starting_map_name in self.second_towns):
			if self.closest_map_with_vendor == None:
				self.closest_map_with_vendor = self.get_closest_map_with_vendor()
			if self.go_to_map(job, main_instance, self.closest_map_with_vendor) == False:
				return False
		
		if self.curr_npc_position == None:
			if store:
				self.curr_npc_position = map_manager.get_npc_position(b0t.current_map(), utility.STORE_VNUM)
			else:
				self.curr_npc_position = map_manager.get_npc_position(b0t.current_map(), utility.VENDOR_VNUM)

		if self.go(job, main_instance, 'vendor_or_store', self.curr_npc_position, False, store is False, store is False) == False:
			return False

		self.curr_npc_position = None
		self.closest_map_with_vendor = None		
		global PATH_LIST
		if 'vendor_or_store' in PATH_LIST:
			PATH_LIST.pop('vendor_or_store')
		return True
	
	def return_to_starting_position(self, job, main_instance):
		if not (self.starting_map_name in self.first_towns or self.starting_map_name in self.second_towns):
			if self.go_to_map(job, main_instance, self.starting_map_name) == False:
				return False

		if self.go(job, main_instance, self.starting_map_name, self.starting_position, False, True) == False:
			return False

		global PATH_LIST
		if self.starting_map_name in PATH_LIST:
			PATH_LIST.pop(self.starting_map_name)
		self.starting_map_name = None
		self.starting_position = None
		return True

teleport = teleport_t()
