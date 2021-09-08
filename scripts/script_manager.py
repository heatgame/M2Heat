import sys, os
sys.path.insert(0, 'root')

if __name__ == '__main__':
    sys.dont_write_bytecode = True
    sys.path.insert(0, 'debug')
    sys.path.insert(0, 'game')
    import config
    config.loaded_in_game = False

import logger
from root import job_manager
import config
import timer

class loader():

    def __init__(self):
        self.script_folder = __file__.replace('script_manager.py', 'scripts')
        self.interval = 2000
        self.cache = list()
        self.job_manager = job_manager.job_manager
        job_manager.job_manager.add_job(self)

    def get_script_list(self):
        l = os.listdir(self.script_folder)
        l.remove('__init__.py')
        return l

    def unload(self, script):
        module = self.import_module(script)
        module.script.__del2__()
        del module.script
        del sys.modules[script.replace('.py', '')]
        del module

    def load(self, script):
        module = self.import_module(script)

    def reload(self, script):
        self.unload(script)
        self.load(script)

    def import_module(self, module_name):
        sys.path.insert(0, self.script_folder)
        module = __import__(module_name.replace('.py', ''))
        sys.path.pop(0)
        return module

    def loop(self):
        for script in self.get_script_list():
            mtime = timer.get_mtime(self.script_folder + "\\" + script)
            first_or_default = next((x for x in self.cache if x[0] == script and x[1] != mtime), None)
            
            if first_or_default is not None:
                self.reload(script)
                self.cache.remove(first_or_default)
                self.cache.insert(0, (script, mtime))
                logger.trace('reloaded: ' + script)
            first_or_default = next((x for x in self.cache if x[0] == script), None)
            if first_or_default is None:
                self.load(script)
                self.cache.insert(0, (script, timer.get_mtime(self.script_folder + "\\" + script)))
                logger.trace('loaded: ' + script)
        for _file in self.cache:
            if os.path.exists(self.script_folder + "\\" + _file[0]) is False:
                self.unload(_file[0])
                self.cache.remove(_file)
                logger.trace('unloaded: ' + _file[0])

if config.loaded_in_game:
    try:
        l = loader()
    except Exception as error:
        import error_manager as err
        err.push(error)
else:
    l = loader()
    while True:
        l.job_manager.loop()
