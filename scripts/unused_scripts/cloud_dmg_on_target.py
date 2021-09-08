# -*- coding:utf-8 -*-
from root import job_manager
import logger
import config
import helper
import playerm2g2 as player
from utility import finder
from utility import pos
import b0t

class load():
    def __init__(self):
        self.interval = 100
        job_manager.job_manager.add_job(self)

    def __del2__(self):
        job_manager.job_manager.del_job(self)
        
    def find_mob_by_vid(self, vid):
        for mob in b0t.mobs(1, 20000):
            mob_data = mob.data()
            if mob_data:
                if mob_data.vid() == vid:
                    return mob_data

    def loop(self):
        main_instance = b0t.main_instance()
        if main_instance == None:
            return

        target_vid = player.GetTargetVID()
        if target_vid == 0:
            return

        target_data = self.find_mob_by_vid(target_vid)
        if target_data == None:
            return        

        for i in range(50):
            b0t.network.add_fly_targeting(target_data.vid(), target_data.position())
            b0t.network.shoot(35)

script = load()

