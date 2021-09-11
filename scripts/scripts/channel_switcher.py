# -*- coding:utf-8 -*-
from root import job_manager
import logger
import helper
import playerm2g2 as player, m2netm2g as net, serverInfo
import utility
from utility import hook
import b0t

class load():
	def __init__(self):
		self.interval = 5000
		self.job = job_manager.job_manager.add_job(self)
		self.channels = {}
		self.current_channel = 0

		self.channel_changed = False

	def __del2__(self):
		job_manager.job_manager.del_job(self)

	def get_region_id(self):
		return 0

	def get_server_id(self, region_id):
		server_name = net.GetServerInfo()
		server_name = server_name.split(',', 1)[0]
		logger.trace(server_name)
		for server in serverInfo.REGION_DICT[region_id].keys():
			if serverInfo.REGION_DICT[region_id][server]['name'] == server_name:
				return server
		
		return 0

	def get_channel_info(self):
		self.channels = {}

		region_id = self.get_region_id()
		server_id = self.get_server_id(region_id)

		channels = serverInfo.REGION_DICT[region_id][server_id]['channel']

		for channel_id, channel_data in channels.items():
			self.channels[channel_id] = {
				'id': channel_id,
				'name': channel_data['name'],
				'ip': channel_data['ip'],
				'port': channel_data['tcp_port'],
				'acc_ip' : serverInfo.REGION_AUTH_SERVER_DICT[region_id][server_id]['ip'],
				'acc_port' : serverInfo.REGION_AUTH_SERVER_DICT[region_id][server_id]['port']
			}

	def connect_to_channel(self, id):
		ip = self.channels[id]["ip"]
		port = self.channels[id]["port"]
		logger.trace(ip + ' ' + str(port))
		net.ConnectTCP(ip, port)
		b0t.network.set_direct_enter_mode(0)
		
	def loop(self):
		# b0t.network.set_login_phase()
		# main_instance = b0t.main_instance()
		# if main_instance == None or self.channel_changed == True:
		# 	return
		
		self.get_channel_info()

		self.connect_to_channel(6)

		self.channel_changed = True

		

script = load()
ch_switcher = script