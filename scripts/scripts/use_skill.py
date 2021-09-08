# -*- coding:utf-8 -*-
from root import job_manager
import logger
import config
import helper
import playerm2g2 as player
import b0t

class load():
    def __init__(self):
        self.interval = 1000
        self.counter = 0
        self.reset = False
        job_manager.job_manager.add_job(self)

    def __del2__(self):
        job_manager.job_manager.del_job(self)

    def loop(self):
        main_instance = b0t.main_instance()
        if main_instance and helper.config.botting:
            if self.reset == True:
                self.counter = 25
                self.reset = False
            
            if self.counter == 25:
                b0t.network.use_skill(35, 0)
                self.counter = 0
            else:
                self.counter += 1
        else:
            self.reset = True

script = load()

