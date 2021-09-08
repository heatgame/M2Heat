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
        return self.yang_price
    def get_won_price(self):
        return self.won_price
    def get_vnum(self):
        return self.vnum
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
    def create_result(self):
        def key(elem):
            return elem.won_price * 100000000 + elem.yang_price
        r = result()
        r.result_count = random.randint(10, 500)
        r.result_count_in_page = 10
        r.curr_page = r.result_count / 10
        for index in range(r.result_count):
            i = item()
            i.yang_price = random.randint(0, 750) * 100
            i.won_price = random.randint(0, 999)
            i.vnum = random.randint(1000, 3000)
            i.name = 'name'
            i.seller_name = 'seller_name'
            r.items.append(i)
        r.items.sort(key=key)
        return r
