import logger
import os, sys

def push(error, delay = 15.0):
	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	logger.trace(str(exc_type) + ", " + str(error) + ", " + str(fname) + ", " + str(exc_tb.tb_lineno))
	
	# try:
	# 	import time
	# 	time.sleep(delay)
	# except:
	# 	pass