# -*- coding:utf-8 -*-
import os
import b0t, helper

class point():
	def __init__(self, index, x, y, vnum):
		self.index = index
		self.x = x
		self.y = y
		self.vnum = vnum

class point_parser():
	def __init__(self, folder):
		self.points = {}

		point_files = os.listdir(folder) #glob.glob(folder + '*.txt')
		
		for base in point_files:
			file = open(folder + base, 'r')
			name = os.path.splitext(base)[0]
			name = name[:-6]
			self.points[name] = []
			for p in file:
				tokens = p.split()
				self.points[name].append(point(int(tokens[0]), int(tokens[1]), int(tokens[2]), int(tokens[3])))
		
	def get_points(self):
		return self.points

points = point_parser(__file__.replace('scripts\\game\\map_manager.py', 'resources\\points\\')).get_points()

def get_npc_position(map_name, vnum):
	for p in points[map_name]:
		if p.vnum == vnum:
			return b0t.pos(p.x, p.y, 0)

	return None

def get_warp_position(map_name, target_map_name):
	for p in points[map_name]:
		npc = helper.npc(p.vnum)
		if npc.type != 3:
			continue

		warp_to_position = npc.position()
		map_info = b0t.background.map_info(warp_to_position.x * 100, warp_to_position.y * 100)
		if map_info.name() != target_map_name:
			continue

		return b0t.pos(p.x, p.y, 0)

	return None