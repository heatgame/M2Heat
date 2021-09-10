# -*- coding:utf-8 -*-
from root import job_manager
import logger
import helper
import playerm2g2 as player, m2netm2g as net
import b0t

class load():
    def __init__(self):
        self.interval = 4000
        self.job = job_manager.job_manager.add_job(self)

    def __del2__(self):
        job_manager.job_manager.del_job(self)
    
    def loop(self):
        main_instance = b0t.main_instance()
        if main_instance == None or helper.config.anti_exp == False:
            return
        
        exp = player.GetStatus(player.EXP)
        next_exp = player.GetStatus(player.NEXT_EXP)

        if exp > (next_exp / 100 * 10):
            net.SendGuildOfferPacket(exp)

script = load()