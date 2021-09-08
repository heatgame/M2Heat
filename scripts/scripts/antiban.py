# -*- coding:utf-8 -*-
from root import job_manager
import logger
import config
import helper
import game
from utility import hook
import b0t
import m2netm2g as net, app

last_private_message_mode = None

def OnRecvWhisper(self, mode, name, line):
	global last_private_message_mode
	last_private_message_mode = mode

class load():
	PLAYER_DETECT = 1
	GM_DETECT =     2
	PM_DETECT =     3
	GMS_PM_DETECT = 4

	def __init__(self):
		self.interval = 50
		self.job = job_manager.job_manager.add_job(self)
		self.is_turned_on_once = True

	def __del2__(self):
		job_manager.job_manager.del_job(self)

	def player_around(self, look_for_gm = False):
		for mob in b0t.mobs(8, 9999999999):
			mob_data = mob.data()
			if mob_data:
				if mob.data().vid() and (look_for_gm == False or mob.data().name().find('[') != -1):
					return True
		return False

	def is_any_state_triggered(self):
		global last_private_message_mode
		if helper.config.antiban_trigger_player:# catch any player
			if self.player_around():
				return self.PLAYER_DETECT
		if helper.config.antiban_trigger_gm:# catch gm
			if self.player.around(True):
				return self.GM_DETECT
		if helper.config.antiban_trigger_pm and last_private_message_mode != None:# catch any private message
			last_private_message_mode = None
			return self.PM_DETECT
		if helper.config.antiban_trigger_gms_pm and last_private_message_mode == 5:# catch gm's private message
			last_private_message_mode = None
			return self.GMS_PM_DETECT
		return 0

	def trigger(self, state):
		# if state == self.PLAYER_DETECT:
		# 	logger.trace('player detected')
		# elif state == self.GM_DETECT:
		# 	logger.trace('gm detect')
		# elif state == self.PM_DETECT:
		# 	logger.trace('pm detect')
		# elif state == self.GMS_PM_DETECT:
		# 	logger.trace("gm's pm detect")
		# else:
		# 	logger.trace("undetected state: " + str(state))
		if helper.config.antiban_logout:
			net.LogOutGame()
		if helper.config.antiban_stop_hacks:
			helper.config.botting = False
			helper.config.picking = False
			helper.config.move_speed = 0
		if helper.config.antiban_exit_game:
			app.Abort()
		self.job.wait_for(15000)

	def loop(self):
		global last_private_message_mode
		try:
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

