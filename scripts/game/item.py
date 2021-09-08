import random

class item():
    def __init__(self):
        self.yang_price = 0
        self.won_price = 0
        self.vnum = 0
        self.amount = 0
        self.name = ''
        self.seller_name = ''
    def get_yang_price(self):
        return self.get_yang_price
    def get_won_price(self):
        return self.get_won_price
    def get_vnum(self):
        return self.get_vnum
    def get_amount(self):
        return self.get_amount
    def get_name(self):
        return self.name
    def get_seller_name(self):
        return self.seller_name

class result():
    def __init__(self):
        self.result_count = 0
        self.result_count_in_page = 0
        self.curr_page = 0
        self.items = list()
    
    def get_result_count(self):
        return self.result_count

    def get_result_count_in_page(self):
        return self.result_count_in_page

    def get_curr_page(self):
        return self.curr_page
    
    def get_items(self):
        return self.items

    def create_sample(self, results):
        r = result()
        r.result_count = random.randint(10, 500)
        r.result_count_in_page = 10
        r.curr_page = 0
        for index in range(r.result_count):
            i = item()
            i.yang_price = random.randint(0, 999999)
            i.won_price = random.randint(0, 999)
            i.vnum = random.randint(0, 0xffffffff)
            i.amount = random.randint(0, 100)
            i.name = 'name'
            i.seller_name = 'seller name'
            r.items.append(i)
        return r
