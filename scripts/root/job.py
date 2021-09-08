import timer
import error_manager

class job():
	def __init__(self, _class):
		self._class = _class
		self.id = id(_class)
		self.tick = self.get_time() - self._class.interval
		
	def get_time(self):
		return timer.get_epoch_ms()
		
	def is_wait_over(self):
		if self.get_time() - self.tick > self._class.interval:
			self.tick = self.get_time()
			return True
		else:
			return False
	
	def wait_for(self, ms):
		self.tick = self.get_time() + ms

	def call(self):
		try:
			self._class.loop()
		except Exception as error:
			import error_manager as err
			err.push(error)
