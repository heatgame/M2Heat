import math
import sys
import os#to catch errors
import logger#to catch errors
import b0t, helper
import safebox, playerm2g2 as player
import map_manager

SLOTS = 0
STORAGE_SLOTS = 45

VENDOR_VNUM = 9003
STORE_VNUM = 9005

class pos():
	def __init__(self, x = 0, y = 0, z = 0):
		self.x = x
		self.y = y
		self.z = z

	def conv(self, p):
		self.x = p.x
		self.y = p.y
		self.z = p.z

		return self

class find_points():

	STANDARD_ATTACKABLE_DISTANCE = 400.0

	def distance(self, a, b):
		fdx = a.x - b.x
		fdy = a.y - b.y
		return math.sqrt((fdx * fdx) + (fdy * fdy))

	def get_position_between(self, a, b, slope, length):
		try:
			point = pos(0, 0, 0)

			if slope == 0:
				point.x = a.x + length
				point.y = a.y
			elif slope == sys.float_info.max:
				point.x = a.x
				point.y = a.y + length
			else:
				dx = (length / math.sqrt(1 + (slope * slope)))
				dy = slope * dx

				if a.x > b.x:
					point.x = a.x - dx
				else:
					point.x = a.x + dx

				if a.y > b.y:
					point.y = a.y - dy
				else:
					point.y = a.y + dy
					
			return point
		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			logger.trace(str(exc_type) + ', ' + str(fname) + ', ' + str(exc_tb.tb_lineno))

	def find(self, a, b, max_distance):
		try:
			points = list()

			length = self.distance(a, b)
			if length < self.STANDARD_ATTACKABLE_DISTANCE:
				return points
			
			if length < max_distance:
				points.append(b)
				return points

			if b.x - a.x == 0:
				return points

			count_of_points = length / max_distance
			slope = abs((b.y - a.y) / (b.x - a.x))

			for i in range(int(count_of_points)):
				i = i + 1
				length = max_distance * i
				points.append(self.get_position_between(a, b, slope, length))

			points.append(b)
			return points
		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			logger.trace(str(exc_type) + ', ' + str(fname) + ', ' + str(exc_tb.tb_lineno))

class find_points2():

	def distance(self, a, b):
		fdx = a.x - b.x
		fdy = a.y - b.y
		return math.sqrt((fdx * fdx) + (fdy * fdy))

	def find(self, a, b, step):
		points = list()

		dx = b.x - a.x
		dy = b.y - a.y

		slope = math.atan2(dy, dx)

		distance = self.distance(a, b)

		for p in range(0, int(round(distance, 0)), step):
			point = pos(a.x + p * math.cos(slope), a.y + p * math.sin(slope), 0)
			points.append(point)

		return points

def block_control(main_position, target_position, max_distance = 100):
	for point in finder.find(main_position, target_position, max_distance):
		if b0t.background.blocked(point.x, point.y):
			return False
	return True

def sort_distance_to_main(mobs, main_instance):
	main_position = main_instance.position()
	return sorted(mobs, key = lambda mob:(b0t.distance(main_position, mob.data().position())))

def is_empty_slot(slot, storage = False):
	if storage == False:
		if b0t.player.get_item_index(slot):
			return False
	else:
		if safebox.GetItemID(slot):
			return False
	line = (slot / 5) % 9
	if (line >= 1 and line <= 8):
		for i in range(1, line + 1):
			vnum = 0
			if storage == False:
				vnum = b0t.player.get_item_index(slot - (i * 5))
			else:
				vnum = safebox.GetItemID(slot - (i * 5))
			if vnum:
				item = helper.item(vnum)
				item_size = item.size()
				if item_size >=  i + 1:
					return False

	return True

def find_empty_slot(size, storage = False):
	global SLOTS, STORAGE_SLOTS
	if SLOTS == 0:
		SLOTS = player.GetExtendInvenMax() if hasattr(player, 'GetExtendInvenMax') and player.GetExtendInvenMax() > 0 else player.INVENTORY_PAGE_SIZE * player.INVENTORY_PAGE_COUNT
	for slot in range(SLOTS if storage == False else STORAGE_SLOTS):
		line = (slot / 5) % 9
		if line + (size - 1) > 8:
			continue
		if is_empty_slot(slot, storage) == False:
			continue
		empty = True
		for i in range(1, size):
			temp_slot = slot + (i * 5)
			if storage == False:
				if b0t.player.get_item_index(temp_slot):
					empty = False
			else:
				if safebox.GetItemID(temp_slot):
					empty = False
			
		if empty:
			return slot

	return -1

def get_npc(vnum):
	mobs = b0t.mobs(64, 4000)
	for m in mobs:
		mob_data = m.data()
		if mob_data.vnum() == vnum:
			return mob_data
	return 0

class hooks():
	def __init__(self):
		self.hooked_functions = {}
		self.hooked_originals = {}
	
	def hook(self, function, on_trigger, run_original = True, run_after = False):
		if function in self.hooked_functions:
			return False

		def run(*args, **kwargs):
			if run_original:
				if run_after == False:
					on_trigger(*args, **kwargs)
				ret_val = self.hooked_originals[function](*args, **kwargs)
				if run_after:
					on_trigger(*args, **kwargs)
				return ret_val
			else:
				return on_trigger(*args, **kwargs)

		self.hooked_functions[function] = on_trigger
		self.hooked_originals[function] = getattr(function[0], function[1])
		
		original_func = self.hooked_originals[function]
		setattr(function[0], function[1], run)
		return True

	def unhook(self, function):
		if (function in self.hooked_functions) == False:
			return False
		setattr(function[0], function[1], self.hooked_originals[function])
		self.hooked_functions.pop(function)
		self.hooked_originals.pop(function)
		return True

	def call(self, org_self, function):
		return self.hooked_originals[function](org_self)

hook = hooks()
finder = find_points()