# -*- coding:utf-8 -*-
from root import job_manager
import logger
import config
import helper
import playerm2g2 as player, skill
import b0t

class load():
    DEFAULT_TIME = 1000 * 1000

    def __init__(self):
        self.interval = 500
        self.elapsed_time = self.DEFAULT_TIME
        self.reset = False
        job_manager.job_manager.add_job(self)

    def __del2__(self):
        job_manager.job_manager.del_job(self)

    def loop(self):
        main_instance = b0t.main_instance()
        if main_instance:
            if helper.config.botting:
                skill_level = player.GetSkillLevel(5)
                cool_time = skill.GetSkillCoolTime(35, skill_level)
                if cool_time != 0.0 and cool_time < (self.elapsed_time / 2):
                    b0t.network.use_skill(35, 0)
                    self.elapsed_time = 0
                    return
                elif cool_time == 0.0:
                    logger.error('skill time error! skill_level: {}, cool_time: {}'.format(skill_level, cool_time))
        else:
            self.elapsed_time = self.DEFAULT_TIME
        self.elapsed_time += 1
script = load()

