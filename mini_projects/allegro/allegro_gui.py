#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import traceback
import tkinter as tk
from collections import namedtuple
from allegro_api import AllegroUser
from allegro_api import AllegroUserItems

logger = logging.getLogger(__name__)
Entry = namedtuple('Entry', ['name', 'text', 'default_value'])


class LoggerHandler(logging.Handler):
    """
    Klasa służąca do logowana komunikatów w konsoli.
    """

    def __init__(self, console):
        logging.Handler.__init__(self)
        self.console = console
        self.console.config(state='disabled')
        self.console.tag_config("INFO", foreground="black")
        self.console.tag_config("DEBUG", foreground="grey")
        self.console.tag_config("WARNING", foreground="orange")
        self.console.tag_config("ERROR", foreground="red")
        self.console.tag_config("CRITICAL", foreground="red", underline=1)

        # Loggger settings
        self.set_logging(__name__, logging.DEBUG)
        self.set_logging('allegro_api', logging.DEBUG)

    def set_logging(self, name, level):
        log_element = logging.getLogger(name)
        log_element.setLevel(level)
        log_element.addHandler(self)

    def emit(self, record):
        msg = self.format(record)
        tag = record.levelname
        def append():
            self.console.configure(state='normal')
            self.console.insert(tk.END, msg+'\n', tag)
            self.console.configure(state='disabled')
            self.console.yview(tk.END)
        self.console.after(0, append)


class AllegroGui:
    """
    Klasa zawierająca panel do obsługi transakcji w serwisie allegro.
    Lewa strona panelu zawiera panel nawigacyjna, a lewa strona konsolę
    wyświetlającą komunikaty z serwisu.
    """

    def __init__(self):
        self.top = tk.Tk()
        self.control = tk.Frame(width=400, height=500, master=self.top)
        self.control.pack(side=tk.LEFT)
        self.build_control_page()
        self.console = tk.Text(width=400, height=500, master=self.top)
        self.console.pack(side=tk.RIGHT)
        self.logger = LoggerHandler(self.console)

    def add_entry(self, entry_text='', default_value=''):
        entry_value = tk.StringVar()
        tk.Label(self.control, text=entry_text).pack()
        tk.Entry(self.control, bd=5, textvariable=entry_value).pack()
        entry_value.set(default_value)
        return entry_value

    def add_checkbox(self, checkbox_name='', default_value=True):
        checkbox_variable = tk.BooleanVar()
        tk.Checkbutton(self.control,
            text=checkbox_name,
            variable = checkbox_variable,
            onvalue=True,
            offvalue=False,
        ).pack()
        checkbox_variable.set(default_value)
        return checkbox_variable

    def add_button(self, text, command):
        tk.Button(self.control, text=text, command=command).pack()

    def build_control_page(self):
        entries = {}
        entries_input = [
            Entry('login', "Login:", "login"),
            Entry('pasword', "Hasło:", "password"),
            Entry('webkey', "Klucz Allegro WebAPI:", "webkey"),
            Entry('change_percent', "Zmiana o: [%]", "0.0"),
            Entry('change_from', "Dla cen od: [zł]", "1"),
            Entry('change_to', "do: [zł]", "100000"),
        ]

        for entrie_input in entries_input:
            entries[entrie_input.name] = self.add_entry(
                entry_text=entrie_input.text,
                default_value=entrie_input.default_value,
            )

        entries['round_price'] = self.add_checkbox("Zaokraglij")

        change_price_callback = self._change_price_callback(
            login=entries['login'],
            password=entries['pasword'],
            webkey=entries['webkey'],
            change_percent=entries['change_percent'],
            chage_from=entries['change_from'],
            change_to=entries['change_to'],
            round_price=entries['round_price'],
        )

        self.add_button('Zmien ceny', change_price_callback)
        self.add_button('Wyjdz', self.top.destroy)

    @staticmethod
    def _change_price_callback(login, password, webkey, change_percent,
            chage_from, change_to, round_price):
        return lambda: AllegroCallbacks.change_price(
            login=str(login.get()),
            password=str(password.get()),
            webkey=str(webkey.get()),
            change_percent=float(change_percent.get()),
            chage_from=float(chage_from.get()),
            change_to=float(change_to.get()),
            round_price=bool(round_price.get()),
        )


class AllegroCallbacks:
    """
    Zbiór funkcji wywoływanych w serwisie.
    """

    @staticmethod
    def change_price(login, password, webkey, change_percent, chage_from,
            change_to, round_price):
        try:
            user = AllegroUser(
                login=login,
                password=password,
                web_api_key=webkey,
            )
            user.get_login_parameters()
            user_items = AllegroUserItems(user)
            user_items.update_user_sell_items_price(
                lover_filter_bandwidth=chage_from,
                higher_filter_bandwidth=change_to,
                change_percent=change_percent,
                round_price=round_price,
            )
        except Exception as e:
            logger.warning(traceback.format_exc())
            logger.error(e)


gui = AllegroGui()
gui.top.mainloop()
