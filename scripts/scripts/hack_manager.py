from root import job_manager
import helper
import logger

class hack_manager_t():
    def __init__(self):
        self.reset()
        self.stopped = False
        self.interval = 1000
        job_manager.job_manager.add_job(self)

    def __del2__(self):
        job_manager.job_manager.del_job(self)

    def loop(self):
        if self.stopped == False:
            self.botting = helper.config.botting
            self.picking = helper.config.picking

    def reset(self):
        self.botting = False
        self.picking = False

    def stop(self):
        self.reset()
        self.stopped = True
        logger.trace('hacks stopped')

    def resume(self):
        self.stopped = False
        logger.trace('hacks resumed')

script = hack_manager_t()
hack_manager = script