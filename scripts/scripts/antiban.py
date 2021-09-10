# -*- coding:utf-8 -*-
from root import job_manager
import logger
import config
import helper
import game
from utility import hook
import b0t
import m2netm2g as net, app
import wintoast
from hack_manager import hack_manager

last_private_message_mode = None
detected_name = ''

def OnRecvWhisper(self, mode, name, line):
	global last_private_message_mode
	global detected_name
	last_private_message_mode = mode
	detected_name = name

class load():
	PLAYER_DETECT = 1
	GM_DETECT =     2
	PM_DETECT =     3
	GMS_PM_DETECT = 4

	TITLES = {PLAYER_DETECT:'Player detected!', GM_DETECT:'GM detected!', PM_DETECT:'PM detected!', GMS_PM_DETECT:"GM'S PM detected!"}

	def __init__(self):
		self.interval = 50
		self.job = job_manager.job_manager.add_job(self)
		self.hacks_stopped = False
		self.is_turned_on_once = True

	def __del2__(self):
		job_manager.job_manager.del_job(self)

	def player_around(self, look_for_gm = False):
		global detected_name
		for mob in b0t.mobs(8, 9999999999):
			mob_data = mob.data()
			if mob_data:
				name = mob.data().name()
				if name in helper.whitelist.current():
					continue
				if mob.data().vid() and (look_for_gm == False or name.find('[') != -1):
					detected_name = name
					return True
		return False

	def is_any_state_triggered(self):
		global last_private_message_mode
		if helper.config.antiban_trigger_player:# catch any player
			if self.player_around():
				return self.PLAYER_DETECT
		if helper.config.antiban_trigger_gm:# catch gm
			if self.player_around(True):
				return self.GM_DETECT
		if helper.config.antiban_trigger_pm and last_private_message_mode != None:# catch any private message
			last_private_message_mode = None
			return self.PM_DETECT
		if helper.config.antiban_trigger_gms_pm and last_private_message_mode == 5:# catch gm's private message
			last_private_message_mode = None
			return self.GMS_PM_DETECT
		return 0

	def trigger(self, state):
		global detected_name
		if helper.config.antiban_logout:
			helper.config.auto_login = False
			b0t.network.set_login_phase()
		if helper.config.antiban_stop_hacks:
			helper.config.botting = False
			helper.config.picking = False
			helper.config.move_speed = 0
		if helper.config.antiban_exit_game:
			app.Abort()
		if helper.config.antiban_create_notification:
			wintoast.create_toast(self.TITLES[state], detected_name)
			self.job.wait_for(15000)
		if helper.config.antiban_wait_to_go:
			hack_manager.stop()
			self.hacks_stopped = True

	def loop(self):
		global last_private_message_mode
		try:
			if helper.config.antiban_wait_to_go and self.hacks_stopped and hack_manager.stopped:
				hack_manager.resume()
				self.hacks_stopped = False
			main_instance = b0t.main_instance()
			if main_instance and helper.config.antiban:
				if self.is_turned_on_once:
					hook.hook((game.GameWindow, 'OnRecvWhisper'), OnRecvWhisper)
					self.is_turned_on_once = False

				result = self.is_any_state_triggered()
				if result != 0:
					self.trigger(result)
			elif self.is_turned_on_once == False:
				hook.unhook((game.GameWindow, 'OnRecvWhisper'))
				last_private_message_mode = None
				self.is_turned_on_once = True

		except Exception as error:
			import error_manager as err
			err.push(error)

script = load()