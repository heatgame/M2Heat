from root import job

class job_manager_t():
	def __init__(self):
		self.jobs = list()
		
	def add_job(self, _class):
		j = job.job(_class)
		self.jobs.insert(0, j)
		return j

	def del_job(self, _class):
		first_or_default = next((x for x in self.jobs if x.id == id(_class)), None)
		if first_or_default is not None:
			self.jobs.remove(first_or_default)
		else:
			import logger
			logger.error('job_manager delete error: not found')
		
	def loop(self):
		try:
			for w in self.jobs:
				if w.is_wait_over():
					w.call()
		except Exception as error:
			import error_manager as err
			err.push(error)

job_manager = job_manager_t()