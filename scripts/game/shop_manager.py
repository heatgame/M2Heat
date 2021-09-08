import helper
import logger
import timer

# from data import data_convertor as data

class shop_manager_t():
    def __init__(self):
        self.jobs = list()
        self.job_index = 0
        self.cd = 1000
        self.tick = 0
        self.is_glass_open = False
        self.slot_of_glass = -1
        self.curr_page = 0
        self.result_index = 0
        self.result_count = 0
        self.results = list()

    def del_job(self, job):
        self.jobs.remove(job)

    def add_job(self, job):
        self.jobs.append(job)

    def clear(self):
        self.curr_page = 0
        self.result_index = 0
        self.result_count = 0
        del self.results[:]

    def open_glass(self):
        if self.slot_of_glass == -1:
            self.slot_of_glass = self.find_trading_glass()
        logger.trace('opening trading glass')
        helper.network.send_item_use(self.slot_of_glass)
        helper.status.script_using_glass = True
        self.is_glass_open = True

    def close_glass(self):
        logger.trace('closing trading glass')
        helper.network.send_shop_search_close()
        helper.status.script_using_glass = False
        self.is_glass_open = False

    def find_trading_glass(self):
        logger.trace('searching trading glass')
        for i in range(90):
            if helper.player.get_item_index(i) == 60005:
                return i
        return -1

    def search(self, name, min_yang_price, max_yang_price, min_won_price, max_won_price):
        if self.is_glass_open == False:
            self.open_glass()
        logger.trace('searching ' + name)
        item = data.items[name]
        if item:
            helper.network.send_shop_search_info_by_vnum(item.vnum, item.char_type, min_yang_price, max_yang_price, min_won_price, max_won_price)

    def on_shop_search_result(self, result):
        try:
            logger.trace('search_result count: ' + str(result.get_result_count()))

            items = result.get_items()
            for index in range(result.get_result_count_in_page()):
                self.results.insert(self.result_index, items[index])
                self.result_index += 1
            
            self.result_count = result.get_result_count()
            self.curr_page = result.get_curr_page()

            go_to_next_page = self.result_count > 10 and self.result_count % (self.curr_page * 10) > 0 and self.result_count % (self.curr_page * 10) != self.result_count
            if go_to_next_page:
                helper.network.send_shop_search_info_sub(self.curr_page + 1)
            else:
                self.jobs[self.job_index].on_shop_search_over(self.results)
                self.clear()

                self.job_index += 1
                if self.job_index == len(self.jobs):
			        self.job_index = 0                    
			        self.tick = timer.get_epoch_ms()		        
			        self.close_glass()

        except Exception as error:
            import error_manager as err
            err.push(error)
            self.clear()
            job_index = 0

    def loop(self):
        if self.is_glass_open:
            return
        
        if self.tick + self.cd < timer.get_epoch_ms():
            self.jobs[self.job_index].search()

    

shop_manager = shop_manager_t()