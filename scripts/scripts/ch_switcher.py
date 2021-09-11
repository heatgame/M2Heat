# -*- coding:utf-8 -*-
import logger
import helper
import playerm2g2 as player, m2netm2g as net, serverInfo
import utility
from utility import hook
import b0t
from auto_login import auto_login

class load():
	def __init__(self):
		self.channels = {}
		self.current_channel = 0
		self.port_diff = 0
		self.port = 0

	def __del2__(self):
		pass

	def get_region_id(self):
		return 0

	def get_server_id(self, region_id):
		server_name = net.GetServerInfo()
		server_name = server_name.split(',', 1)[0]
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

	def get_channel_count(self):
		return len(self.channels)

	def connect_to_channel(self, id):
		auto_login.job.wait_for(5000)
		b0t.network.set_direct_enter_mode(0)
		net.ConnectTCP(self.channels[id]['ip'], self.channels[id]['port'] - self.port_diff)

	def get_next_channel(self):
		self.current_channel = self.get_curr_channel()
		if self.current_channel >= self.get_channel_count():
			return 1

		return self.current_channel + 1

	def get_curr_channel(self):
		return min(range(1, self.get_channel_count() + 1), key = lambda i: abs(self.channels[i]['port'] - self.port))

	def on_connect(self, ip, port):
		if b0t.network.phase() == 'OffLine':
			return

		self.get_channel_info()

		self.port = port
		self.current_channel = self.get_curr_channel()
		self.port_diff = self.channels[self.current_channel]['port'] - port
		

script = load()
ch_switcher = script