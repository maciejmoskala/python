#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from zeep import Client

logger = logging.getLogger(__name__)


class AllegroApi():

    url = "https://webapi.allegro.pl/service.php?wsdl"
    client = Client(url)


class AllegroUser(AllegroApi):
    """
    Klasa bazowa do obsługi sesji użytkownika w serwisie Allego.
    """

    COUNTRY_CODE = 1

    def __init__(self, login='', password='', web_api_key=''):
        self.login = login
        self.password = password
        self.web_api_key = web_api_key

    @property
    def verification_key(self):
        allegro_response = self.client.service.doQuerySysStatus(
            2,
            self.COUNTRY_CODE,
            self.web_api_key,
        )
        return allegro_response['verKey']

    def get_login_parameters(self):
        login_status = self.client.service.doLogin(
            self.login,
            self.password,
            self.COUNTRY_CODE,
            self.web_api_key,
            self.verification_key,
        )
        self.session_handle = login_status['sessionHandlePart']
        self.user_id = login_status['userId']
        self.service_time = login_status['serverTime']


class AllegroUserItems():
    """
    Klasa służąca do obsługi posidanych tranzakcji w serwisie Allegro,
    a zwłaszcza zmiany cen poszczególnych produktów o określony procent.
    """

    def __init__(self, user=AllegroUser()):
        self.user = user
        self.items = []

    def get_user_sell_items_information(self, lover_filter_bandwidth=0,
            higher_filter_bandwidth=0, page_size=1000, page_number=0):
        sort_property = {'sortType': 2, 'sortOrder': 1}
        filter_property = {
            'filterPrice': {
                'filterPriceFrom': float(lover_filter_bandwidth),
                'filterPriceTo': float(higher_filter_bandwidth),
            }
        }
        sell_items = self.user.client.service.doGetMySellItems(
            self.user.session_handle,
            sort_property,
            filter_property,
            None,
            None,
            None,
            page_size,
            page_number
        )

        self.items_counter = sell_items.sellItemsCounter or 0
        items = sell_items.sellItemsList['item'] or []
        return items

    def get_all_user_sell_items(self, lover_filter_bandwidth=0,
            higher_filter_bandwidth=0, page_size=1000):
        self.items = self.get_user_sell_items_information(
            lover_filter_bandwidth=lover_filter_bandwidth,
            higher_filter_bandwidth=higher_filter_bandwidth,
            page_size=page_size,
        )

        if self.items_counter > page_size:
            for page_number in range(1, ((self.items_counter-1)//page_size)+1):
                self.items += self.get_user_sell_items_information(
                    lover_filter_bandwidth=lover_filter_bandwidth,
                    higher_filter_bandwidth=higher_filter_bandwidth,
                    page_size=page_size,
                    page_number=page_number,
                )

    @staticmethod
    def get_new_item_price(item_price=0, change_percent=0, round_price=True):
        item_price = float(item_price)
        change_percent = float(change_percent)

        if round_price:
            new_item_price = round(round(item_price*(1 + change_percent/100), 1)-0.01, 2)
        else:
            new_item_price = round(item_price*(1 + change_percent/100), 2)

        if new_item_price < 1:
            return 1.0
        return new_item_price

    @staticmethod
    def item_price_can_change(item_price, new_item_price):
        return (item_price != new_item_price and new_item_price >= 1)

    def change_item_price(self, item_id, new_item_price):
        try:
            self.user.client.service.doChangePriceItem(
                self.user.session_handle,
                item_id,
                None,
                None,
                new_item_price)
        except ValueError as e:
            logger.warning("Dla produktu {0} wystąpił błąd: {1}!".format(item_id, e))
        else:
            logger.info("Dla produktu %d cena zostala zaktualizowana na %.2f." % (
                item_id, new_item_price))

    def update_user_sell_items_price(self, lover_filter_bandwidth=0,
            higher_filter_bandwidth=0, change_percent=0, round_price=True):
        if change_percent == 0:
            logger.warning('Nieprawidłowe ustawienie zmiany ceny!')
            return False

        self.get_all_user_sell_items(
            lover_filter_bandwidth=lover_filter_bandwidth,
            higher_filter_bandwidth=higher_filter_bandwidth,
        )

        for item in self.items:
            item_id = item['itemId']
            item_prices = item['itemPrice']
            for item_price in item_prices['item']:
                if item_price['priceType'] == 1:
                    new_item_price = self.get_new_item_price(
                        item_price.priceValue,
                        change_percent,
                        round_price,
                    )
                    if self.item_price_can_change(item_price, new_item_price):
                        self.change_item_price(item_id, new_item_price)

        return True


class AllegroUserFeedbacks():
    """
    Klasa do obsługi komentarzy w serwisie allegro.
    """

    def __init__(self, user=AllegroUser()):
        self.user = user
        self.feedbacks = []

    def get_waiting_feedbacks_count(self):
        feedbacks_count = self.user.client.service.doGetWaitingFeedbacksCount(
            self.user.session_handle,
        )
        return feedbacks_count


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    user = AllegroUser(
        login='user or email',
        password='password',
        web_api_key='you can generate it on allegro.pl website',
    )
    user.get_login_parameters()

    user_feedbacks = AllegroUserFeedbacks(user)
    feedbacks_count = user_feedbacks.get_waiting_feedbacks_count()
    print(feedbacks_count)

    user_items = AllegroUserItems(user)

    # Get all user items
    user_items.get_all_user_sell_items()
    logger.info("User Items: {}".format(len(user_items.items)))

    # Change price for items with price from 2 to 10 PLN by -5 procent and round 
    # price to finish with 9.
    user_items.update_user_sell_items_price(
        lover_filter_bandwidth=2,
        higher_filter_bandwidth=100,
        change_percent=-1,
    )
