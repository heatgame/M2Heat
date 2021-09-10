# -*- coding:utf-8 -*-
from root import job_manager
import logger, timer
import config
import helper
import playerm2g2 as player
import b0t
from hack_manager import hack_manager

class load():
    def __init__(self):
        self.interval = 0
        self.job = job_manager.job_manager.add_job(self)
        self.last_pos = None
        self.last_wait_tick = 0
        self.last_move_tick = 0
        self.move_counter = 0

    def __del2__(self):
        job_manager.job_manager.del_job(self)

    def loop(self):
        main_instance = b0t.main_instance()
        if main_instance == None or helper.config.move_speed == 0:
            return

        main_instance_position = main_instance.position()
        if self.last_pos == None:
            self.last_pos = main_instance_position

        curr_motion = main_instance.motion()
        curr_tick = timer.get_epoch_ms()

        if b0t.distance(self.last_pos, main_instance_position) < 1:
            return

        if curr_motion == 1:
            if self.last_wait_tick + 100 <= timer.get_epoch_ms():
                b0t.network.state(main_instance_position, 0, 0, 0)
                self.last_pos = main_instance_position
                self.last_wait_tick = curr_tick
        elif curr_motion == 2:
            if self.last_move_tick + 100 <= timer.get_epoch_ms():
                
                if self.move_counter != 2:
                    b0t.network.state(main_instance_position, 0, 1, 0)
                    self.move_counter += 1
                else:
                    b0t.network.state(main_instance_position, 0, 0, 0)
                    self.move_counter = 0

                self.last_pos = main_instance_position

                self.last_move_tick = curr_tick

script = load()
