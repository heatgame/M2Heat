# -*- coding:utf-8 -*-
from root import job_manager
import logger
import config
import helper, timer
import b0t
import playerm2g2 as player, m2netm2g as net, game, ime, event, safebox
import math
import sys#to catch errors
import os#to catch errors
import traceback#to catch errors
import utility
utility = reload(utility)
import teleport_manager
teleport_manager = reload(teleport_manager)
from teleport_manager import teleport
from utility import hook
from hack_manager import hack_manager

SHOP_OPEN = False
STORAGE_OPEN = False

LAST_SENT_PASSWORD = 0

_game = None

def SendPassword(password):
	global LAST_SENT_PASSWORD
	if LAST_SENT_PASSWORD + 2000 <= timer.get_epoch_ms():
		ime.SetText(password)
		ime.PasteBackspace()
		ime.PasteReturn()
		LAST_SENT_PASSWORD = timer.get_epoch_ms()

def StartShop(self, vid):
	global SHOP_OPEN
	SHOP_OPEN = True

def AskSafeboxPassword(self):
	if helper.config.pickup_enable_auto_store == False:
		return

	if len(helper.config.storage_password) != 0:
		SendPassword(helper.config.storage_password)

def OpenSafeboxWindow(self, size):
	global STORAGE_OPEN, _game
	_game = self
	STORAGE_OPEN = True

def CommandCloseSafebox(self):
	global STORAGE_OPEN
	STORAGE_OPEN = False

class load():
	STATE_CHECK = 0
	STATE_MOVE = 1
	STATE_SELL = 2
	STATE_STACK = 3
	STATE_STORE = 4
	STATE_RETURN = 5

	def __init__(self):
		self.interval = 100
		self.state = self.STATE_CHECK
		self.sellable_slots = list()
		self.stackable_slots = list()
		self.storable_slots = list()
		self.job = job_manager.job_manager.add_job(self)

	def __del2__(self):
		job_manager.job_manager.del_job(self)
		hook.unhook((game.GameWindow, 'OpenQuestWindow'))
		hook.unhook((game.GameWindow, 'StartShop'))
		hook.unhook((game.GameWindow, 'AskSafeboxPassword'))
		hook.unhook((game.GameWindow, 'OpenSafeboxWindow'))
		hook.unhook((game.GameWindow, 'CommandCloseSafebox'))

	def has_attr(self, slot):
		for i in range(5):
			(btype, svalue) = player.GetItemAttribute(slot, i)
			if btype == 0 or btype == -1:
				return False
			
			if svalue >= 10:
				return True

		return False

	def is_inventory_full(self):
		if utility.find_empty_slot(2) == -1:
			return True
		
		return False

	def retrieve_sellable_list(self):
		for i in range(utility.SLOTS):
			vnum = b0t.player.get_item_index(i)
			if vnum == 0:
				continue
			
			item = helper.item(vnum)
			item_type = item.type()
			if item == None or item.sellable() == False:
				continue

			if item_type >= 1 and item_type <= 2:
				if self.has_attr(i):
					continue
			elif item_type == 10: # STONE
				grade = int(item.name().split('+')[1])
				if grade >= 3:
					continue
			elif helper.config.pickup_sell_potions:
				is_item_potion = (vnum >= 27001 and vnum <= 27008) or (vnum >= 27051 and vnum <= 27054) or (vnum >= 27100 and vnum <= 27105) or (vnum >= 27110 and vnum <= 27123) or (vnum >= 27201 and vnum <= 27212)
				if is_item_potion == False:
					continue
			else:
				continue

			self.sellable_slots.append(i)

	def retrieve_storable_list(self):
		for i in range(utility.SLOTS):
			vnum = b0t.player.get_item_index(i)
			if vnum == 0:
				continue
			
			item = helper.item(vnum)
			if item == None or item.storable() == False:
				continue
			
			item_type = item.type()
			if item_type >= 1 and item_type <= 2: # weapons and armors
				if self.has_attr(i) == False:
					continue

			if (item_type >= 3 and item_type <= 4): # usables aka potions
				continue

			self.stackable_slots.append(i)
			self.storable_slots.append(i)

	def stack_item(self, vnum, slot, count):
		item = helper.item(vnum)
		item_size = item.size()

		for i in range(utility.STORAGE_SLOTS):
			curr_vnum = safebox.GetItemID(i)
			curr_count = safebox.GetItemCount(i)
			if curr_vnum != vnum or item.stackable() == False or curr_count + count > 200:
				continue

			new_slot = utility.find_empty_slot(item_size)
			if new_slot == -1:
				continue

			logger.trace('STACK_ITEM storage_slot: ' + str(i) + ' inventory_slot: ' + str(slot))

			net.SendSafeboxCheckoutPacket(i, new_slot)
			net.SendItemMovePacket(new_slot, slot, curr_count)

			return True
		
		return False

	def store_item(self, vnum, slot):
		item = helper.item(vnum)
		item_size = item.size()

		empty_storage_slot = utility.find_empty_slot(item_size, True)
		if empty_storage_slot == -1:
			return False

		logger.trace('STORE_ITEM inventory_slot: ' + str(slot) + ' storage_slot: ' + str(empty_storage_slot))

		net.SendSafeboxCheckinPacket(slot, empty_storage_slot)

		return True

	def loop(self):
		try:
			main_instance = b0t.main_instance()
			if main_instance and (helper.config.pickup_enable_auto_sell or helper.config.pickup_enable_auto_store) and helper.status.is_ingame:# and helper.config.botting:
				if main_instance.dead():
					return

				main_position = main_instance.position()

				hook.hook((game.GameWindow, 'StartShop'), StartShop)
				hook.hook((game.GameWindow, 'AskSafeboxPassword'), AskSafeboxPassword, True, True)
				hook.hook((game.GameWindow, 'OpenSafeboxWindow'), OpenSafeboxWindow)
				hook.hook((game.GameWindow, 'CommandCloseSafebox'), CommandCloseSafebox)

				if self.state == self.STATE_CHECK:
					# logger.trace('sell.py STATE_CHECK')
					if self.is_inventory_full():
						# logger.trace('inventory full')
						hack_manager.stop()
						if helper.config.pickup_enable_auto_sell:
							self.state = self.STATE_MOVE
						else:
							self.state = self.STATE_SELL
				elif self.state == self.STATE_MOVE:
					#logger.trace('sell.py STATE_MOVE')
					if teleport.go_to_closest_vendor_or_store(self.job, main_instance):
						npc = utility.get_npc(utility.VENDOR_VNUM)
						if npc == 0:
							self.job.wait_for(1000)
							return
						
						npc_vid = npc.vid()
						#prepare shop window
						hook.hook((game.GameWindow, 'OpenQuestWindow'), lambda self, skin, idx: None, False)
						b0t.network.on_click(npc_vid)
						event.SelectAnswer(1, 0)

						self.job.wait_for(1000)
						global SHOP_OPEN
						if SHOP_OPEN == True:						
							#prepare sell list
							self.retrieve_sellable_list()
							self.state = self.STATE_SELL
				elif self.state == self.STATE_SELL:
					#logger.trace('sell.py STATE_SELL')				
					if len(self.sellable_slots):
						if SHOP_OPEN == False:
							self.state = self.STATE_MOVE
							return

						current_slot = self.sellable_slots.pop()
						current_vnum = b0t.player.get_item_index(current_slot)
						current_item = helper.item(current_vnum)
						current_count = b0t.player.get_item_count(current_slot)
						logger.trace('slot: ' + str(current_slot) + ' name: ' + current_item.name() + ' price: ' + str(current_item.sell_price()))
						b0t.network.sell(current_slot, current_count, 1)

						self.job.wait_for(250)
					elif helper.config.pickup_enable_auto_store:
						if teleport.go_to_closest_vendor_or_store(self.job, main_instance, True):
							npc = utility.get_npc(utility.STORE_VNUM)
							if npc == 0:
								self.job.wait_for(1000)
								return

							npc_vid = npc.vid()
							#prepare storage window
							hook.hook((game.GameWindow, 'OpenQuestWindow'), lambda self, skin, idx: None, False)
							b0t.network.on_click(npc_vid)
							event.SelectAnswer(1, 1)

							self.job.wait_for(1)
							global STORAGE_OPEN
							if STORAGE_OPEN == True:						
								#prepare storable list
								self.retrieve_storable_list()
								self.state = self.STATE_STACK
					else:
						global SHOP_OPEN
						SHOP_OPEN = False
						self.state = self.STATE_RETURN
				elif self.state == self.STATE_STACK:
					if len(self.stackable_slots):
						if STORAGE_OPEN == False:
							self.state = self.STATE_SELL
							return

						current_slot = self.stackable_slots.pop()
						current_vnum = b0t.player.get_item_index(current_slot)
						current_count = b0t.player.get_item_count(current_slot)

						if self.stack_item(current_vnum, current_slot, current_count):
							self.job.wait_for(1000)
					else:
						self.state = self.STATE_STORE
				elif self.state == self.STATE_STORE:
					if len(self.storable_slots):
						if STORAGE_OPEN == False:
							self.state = self.STATE_SELL
							return

						current_slot = self.storable_slots.pop()
						current_vnum = b0t.player.get_item_index(current_slot)

						if self.store_item(current_vnum, current_slot):
							self.job.wait_for(1000)
					else:
						# _game.CommandCloseSafebox()
						player.SendStorageClose(5)
						self.job.wait_for(5000)
						self.state = self.STATE_RETURN
				elif self.state == self.STATE_RETURN:
					hook.unhook((game.GameWindow, 'OpenQuestWindow'))
					#logger.trace('sell.py STATE_RETURN')
					if teleport.return_to_starting_position(self.job, main_instance):
						hack_manager.resume()
						self.state = self.STATE_CHECK

			if not helper.config.pickup_enable_auto_sell and not helper.config.pickup_enable_auto_store:
				self.state = self.STATE_CHECK
				
		except Exception as e:
			e = traceback.format_exc()
			logger.trace(e)

script = load()

