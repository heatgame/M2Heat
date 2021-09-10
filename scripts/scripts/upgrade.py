# -*- coding:utf-8 -*-
from root import job_manager
import logger
import helper
import playerm2g2 as player, m2netm2g as net, game
import utility
from utility import hook
import b0t

class load():
    def __init__(self):
        self.interval = 10
        self.job = job_manager.job_manager.add_job(self)

    def __del2__(self):
        job_manager.job_manager.del_job(self)
    
    def h(self):
        hook.hook((game.GameWindow, 'PopupMessage'), lambda self, msg: None, False)
        self.job.wait_for(5000)

    def u(self):
        hook.unhook((game.GameWindow, 'PopupMessage'))

    def on_upgrade(self, index):
        self.h()
        net.SendRefinePacket(index, 0)

    def on_upgrade_dt(self, index):
        self.h()
        net.SendRefinePacket(index, 4)

    def loop(self):
        main_instance = b0t.main_instance()
        if main_instance == None:
            return
        if ((game.GameWindow, 'PopupMessage') in hook.hooked_functions) == True:
            self.u()

script = load()
upgrade = script