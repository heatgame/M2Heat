import ctypes

def LogBox(message, title = "dbg"):
	ctypes.windll.user32.MessageBoxW(0, message, title, 0)