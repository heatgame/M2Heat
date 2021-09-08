# -*- coding:utf-8 -*-
from root import job_manager
import logger
import config
import helper
import b0t, timer
import m2netm2g as net, playerm2g2 as player

class load():
    def __init__(self):
        self.interval = 100
        self.job = job_manager.job_manager.add_job(self)
        self.logged_in_once = False
        self.pk_enabled = False
        self.last_online_tick = 0

    def __del2__(self):
        job_manager.job_manager.del_job(self)

    def loop(self):
        main_instance = b0t.main_instance()
        if main_instance:
            self.logged_in_once = True
            self.last_online_tick = timer.get_epoch_ms()
            if self.pk_enabled == False:
                net.SendCommandPacket(net.PLAYER_CMD_PKMODE, 0, '1')
                self.pk_enabled = True
        else:
            self.pk_enabled = False

        if self.logged_in_once:
            phase = b0t.network.phase()
            if phase == 'OffLine' and helper.config.auto_login:
                net.DirectEnter(0, 0)
                self.job.wait_for(2000)
            elif phase != 'Game' and self.last_online_tick + 15000 <= timer.get_epoch_ms():
                logger.trace('PHASE STUCK')
                b0t.network.set_login_phase()
                self.last_online_tick = timer.get_epoch_ms()


script = load()

