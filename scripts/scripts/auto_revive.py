# -*- coding:utf-8 -*-
from root import job_manager
import logger
import config
import helper
import playerm2g2 as player, m2netm2g as net
import b0t

class load():
    def __init__(self):
        self.interval = 1000
        job_manager.job_manager.add_job(self)

    def __del2__(self):
        job_manager.job_manager.del_job(self)

    def loop(self):
        main_instance = b0t.main_instance()
        if main_instance:
            main_instance = b0t.main_instance()
            if main_instance.dead() == False:
                return

            net.SendCommandPacket(net.PLAYER_CMD_RESTART, 1)

script = load()
