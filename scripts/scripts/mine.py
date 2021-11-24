import utility
import b0t
import timer

class c_mine():

    def __init__(self):
        self.state = self.walk
        self.main_instance = None
        self.mine_data = None
        self.check_tick = 0

    def __del2__(self):
        pass

    def walk(self):
        main_position = self.main_instance.position()
        target_position = self.mine_data.position()

        if b0t.distance(main_position, target_position) < 400:
            self.state = self.mining
            return True

        if utility.block_control(main_position, target_position):
            self.main_instance.move(target_position)
            return True

        return False

    def mining(self):
        b0t.network.on_click(self.mine_data.vid())
        self.check_tick = timer.get_epoch_ms()
        self.state = self.check
        return True

    def check(self):
        if self.main_instance.motion() == 12:# TYPE_NUM
            self.check_tick = timer.get_epoch_ms()
        elif timer.get_epoch_ms() - self.check_tick > 3000:
            self.state = self.mining

        return True

    def reset(self, main_instance, mine_data):
        self.main_instance = main_instance
        self.mine_data = mine_data
        self.state = self.walk

    def loop(self, main_instance, mine_data):
        if self.mine_data == None or self.mine_data.vid() != mine_data.vid():
            self.reset(main_instance, mine_data)
        return self.state()

mine = c_mine()
script = mine