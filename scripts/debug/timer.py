import time, os

def get_epoch_ms():
	return round(time.time() * 1000)
	
def get_mtime(file_name):
	return os.stat(file_name).st_mtime