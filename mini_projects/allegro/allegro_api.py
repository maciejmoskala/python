#!/usr/bin/env python

"""
Problem: Make program to change prices on allegro.pl.
"""

from suds.client import Client


class AllegroApi():

    url = "https://webapi.allegro.pl/service.php?wsdl"
    client = Client(url)


class AllegroUser(AllegroApi):

    country_code = 1

    def __init__(self, login = '', password = '', web_api_key = ''):
        self.login = login
        self.password = password
        self.web_api_key = web_api_key

    @property
    def verification_key(self):
        allegro_response = self.client.service.doQuerySysStatus(
            2,
            self.country_code,
            self.web_api_key)
        return allegro_response['verKey']

    def get_login_parameters(self):
        login_status = self.client.service.doLogin(
            self.login,
            self.password,
            self.country_code,
            self.web_api_key,
            self.verification_key)
        self.session_handle = login_status['sessionHandlePart']
        self.user_id = login_status['userId']
        self.service_time = login_status['serverTime']


class AllegroUserItems():

    def __init__(self, user = AllegroUser()):
        self.user = user

    def get_user_sell_items_information(self, lover_filter_bandwidth = float(0),
            higher_filter_bandwidth = float(0), page_size = 1000,
            page_number = 0):
        sell_items = user.client.service.doGetMySellItems(
            user.session_handle,
            {'sortType': 2, 'sortOrder': 1},
            {'filterPrice':
                {'filterPriceFrom': lover_filter_bandwidth,
                'filterPriceTo': higher_filter_bandwidth}},
            None,
            None,
            None,
            page_size,
            page_number)

        self.items_counter = sell_items['sellItemsCounter']
        items = sell_items['sellItemsList']['item'] or []
        return items

    def get_all_user_sell_items(self, lover_filter_bandwidth = float(0),
            higher_filter_bandwidth = float(0), page_size = 1000):
        self.items = self.get_user_sell_items_information(
            lover_filter_bandwidth,
            higher_filter_bandwidth,
            page_size)

        if self.items_counter > page_size:
            for page_number in xrange(1, ((self.items_counter-1)//page_size)+1):
                self.items += self.get_user_sell_items_information(
                    lover_filter_bandwidth,
                    higher_filter_bandwidth,
                    page_size,
                    page_number)

    @staticmethod
    def get_new_item_price(item_price = float(0), change_percent = float(0),
            round_price = True):
        item_price = float(item_price)
        change_percent = float(change_percent)

        if round_price == True:
            new_item_price = round(round(item_price*(1 + change_percent/100), 1)-0.01, 2)
        else:
            new_item_price = round(item_price*(1 + change_percent/100), 2)

        if new_item_price < 1:
            return 1.0
        return new_item_price

    @staticmethod
    def item_price_can_change(item_price = float(0), new_item_price = float(0)):
        return (item_price != new_item_price and new_item_price >= 1)

    def change_item_price(self, item_id, new_item_price = float()):
        try:
            user.client.service.doChangePriceItem(
                self.user.session_handle,
                item_id,
                None,
                None,
                new_item_price)
        except ValueError as e:
            print e
        else:
            print "Dla produktu %d cena zostala zaktualizowana na %.2f." % (
                item_id, new_item_price)

    def update_user_sell_items_price(self, lover_filter_bandwidth = float(0),
            higher_filter_bandwidth = float(0), change_percent = float(0),
            round_price = True):
        if change_percent == 0:
            print 'Change procent is not set'
            return False

        self.get_all_user_sell_items(lover_filter_bandwidth,
            higher_filter_bandwidth)

        print self.items

        for item in self.items:
            item_id = item['itemId']
            item_price = item['itemPrice']['item'][0]['priceValue']
            new_item_price = self.get_new_item_price(
                item_price, change_percent, round_price)

            if self.item_price_can_change(item_price, new_item_price):
                self.change_item_price(item_id, new_item_price)

        return True


if __name__ == '__main__':
    user = AllegroUser(
        login = 'user or email',
        password = 'password',
        web_api_key = 'you can generate it on allegro.pl website')
    user.get_login_parameters()

    user_items = AllegroUserItems(user)

    # Get all user items
    user_items.get_all_user_sell_items()
    print len(user_items.items)

    # Change price for items with price from 2 to 10 PLN by -5 procent and round 
    # price to finish with 9.
    user_items.update_user_sell_items_price(
        lover_filter_bandwidth = 2,
        higher_filter_bandwidth = 10,
        change_percent = -5)
