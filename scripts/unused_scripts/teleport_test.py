# -*- coding:utf-8 -*-
from root import job_manager
import logger
import config
import helper
import playerm2g2 as player, m2netm2g as net
import b0t

class load():
    def __init__(self):
        self.interval = 0
        self.index = 0
        self.path = None
        self.teleported_once = False
        self.send_direct_enter = False
        self.job = job_manager.job_manager.add_job(self)

    def __del2__(self):
        job_manager.job_manager.del_job(self)

    def loop(self):
        if self.send_direct_enter:
            net.DirectEnter(0, 0)
            self.teleported_once = True
            self.send_direct_enter = False

        if self.teleported_once == True:
            return

        main_instance = b0t.main_instance()
        if main_instance == None:
            return

        main_instance_position = main_instance.position()
        path = helper.astar.find_path(main_instance_position, b0t.pos(81200, 11700, 0), 10000, 1) #b0t.pos(81200, 11700, 0) #b0t.pos(53900, 142400, 0)

        for p in path:
            b0t.network.state(p, 0, 0, 0)

        self.job.wait_for(200)
        self.send_direct_enter = True


script = load()

