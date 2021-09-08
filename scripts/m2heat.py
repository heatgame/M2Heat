#try:
import sys
sys.dont_write_bytecode = True

import logger
logger.trace("hello from M2Heat :)")

try:
	import script_manager
except Exception as error:
	import error_manager as err
	err.push(error)
