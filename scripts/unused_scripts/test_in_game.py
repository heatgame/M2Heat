# -*- coding:utf-8 -*-
from root import job_manager
import shop_manager
import shop
import logger
import config
import helper

class data_t():
    def __init__(self, item, profit_rate):
        self.item = item
        self.profit_rate = profit_rate

class load():
	def __init__(self):
		self.interval = 1000
		job_manager.job_manager.add_job(self)
		self.search_list = (
			# item_name, maximum acceptable price in yang, profit rate in percentage
			('White Pearl', 250000000, 15)
		)
		self.search_index = 0
		shop_manager.shop_manager.add_job(self)
		self.buyable = list()

	def __del2__(self):
		job_manager.job_manager.del_job(self)
		shop_manager.shop_manager.del_job(self)

	def search(self):
		curr_item = self.search_list[self.search_index]
		shop_manager.shop_manager.search(curr_item[0], 0, 1999999999, 0, 999)

	def on_shop_search_over(self, results):
		data = self.calculate_profit_rates(results)

		for d in data:
			if d.profit_rate >= self.search_list[self.search_index][2]:
				if all(d.item.get_id() != bi.item.get_id() for bi in self.buyable):
					self.buyable.append(d)
					data.remove(d)
					logger.trace('name: {}, seller name: {}, won {}, yang {:,}, profit rate: %{}, amount {}'.format(d.item.get_name(), d.item.get_seller_name(), d.item.get_won_price(), d.item.get_yang_price(), d.profit_rate, d.item.get_amount()))
		
		for iwpr in self.buyable:
			second = False
			for item in data:
				profit_rate = item.profit_rate
				if iwpr.profit_rate - profit_rate < 5 and profit_rate > 0:
					if second is True:
						d = iwpr
						logger.trace('bunu alma mq : name: {}, seller name: {}, won {}, yang {:,}, profit rate: %{}, amount {}'.format(d.item.get_name(), d.item.get_seller_name(), d.item.get_won_price(), d.item.get_yang_price(), d.profit_rate, d.item.get_amount()))
						break
					else:
						second = True

		self.search_index += 1
		if self.search_index == len(self.search_list):
			self.search_index = 0

	def loop(self):
		# logger.trace('len ' + str(len(shop_manager.shop_manager.jobs)))
		if not helper.status.user_interacting and helper.status.is_ingame:
			shop_manager.shop_manager.loop()

	def get_real_price(self, item):
		return item.get_won_price() * 103000000 + item.get_yang_price()

	def calculate_profit_rates(self, items):
		price_sum = 0
		result_count = 0
		avg_price = 0

		for item in items:
			result_count += item.get_amount()
			price_sum += self.get_real_price(item)

		avg_price = price_sum / result_count

		item_wpr = list()
		for item in items:
			profit_rate = (avg_price - (self.get_real_price(item) / item.get_amount())) * 100 / avg_price
			# remove absurdly priced item from list
			if profit_rate < -100:
				items.remove(item)
				return self.calculate_profit_rates(items)

			item_wpr.append(data_t(item, profit_rate))
			items.remove(item)

		logger.trace('{} avg price: {:,}'.format(self.search_list[self.search_index][0], avg_price))
		return item_wpr

script = load()
