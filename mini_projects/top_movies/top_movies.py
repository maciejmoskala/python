#!/usr/bin/env python

"""
Problem: Make csv file with list of movies for imdb website.
"""

import urllib
import operator
from bs4 import BeautifulSoup
from csv import DictWriter
from operator import attrgetter
from collections import namedtuple

Move = namedtuple('Move', ['year', 'number', 'title'])

class TopMoveSelector(object):
    """
    TopMoveSelector is the class to download best movies for imdb website and
    preare this data in namedtuple.
    """

    top_movies = []

    def __init__(self, url, max_number_of_movies = 100):
        self.url = url
        self.html = urllib.urlopen(self.url).read()
        self.soup = BeautifulSoup(self.html, "html.parser")
        self.max_number_of_movies = max_number_of_movies

    def prepare_move_data(self, year, number, title):
        """
        Function to format move data.
        """
        year = int(str(year)[1:-1])
        number = int(" ".join(number.split())[:-1])
        title = " ".join(title.split()).encode('utf-8')
        return Move(year = year, number = number, title = title)

    def get_top_movies(self):
        """
        Function to download movies list. Movies are storied in title column
        on imdb website.
        """
        self.top_movies = []
        list_of_movies = self.soup.findAll("td", {"class": "titleColumn"})

        for index, move_content in enumerate(list_of_movies):
            move_data = self.prepare_move_data(
                move_content.contents[3].contents[0],
                move_content.contents[0],
                move_content.contents[1].contents[0])
            self.top_movies.append(move_data)
            if index >= self.max_number_of_movies-1:
                break

    def sort_movies_by_title(self, reversed = False):
        self.top_movies = sorted(self.top_movies, key=attrgetter('title'),
            reverse=reversed)

    def sort_movies_by_year(self, reversed = True):
        self.top_movies = sorted(self.top_movies, key=attrgetter('year'),
            reverse=reversed)

    def sort_movies_by_number(self, reversed = False):
        self.top_movies = sorted(self.top_movies, key=attrgetter('number'),
            reverse=reversed)


class CsvDataHandler(object):
    """
    This class is used for saving movied in csv data file.
    """

    def __init__(self, file_name = 'default'):
        self.file_name = file_name

    @staticmethod
    def _if_list_not_empty(list_name):
        return not list_name or not isinstance(list_name, list)

    def _prepare_columns_and_filed_names(self, field_names = []):
        move_fields = list(Move._fields)

        if self._if_list_not_empty(field_names):
            field_names = move_fields
        columns = []
        for field in field_names:
            columns.append(move_fields.index(field))
        return field_names, columns

    def _prepare_move_data_dict(self, move_data, field_names = [],
            columns = []):
        data = [move_data[column] for column in columns]
        return dict(zip(field_names, data))

    def save_data_to_csv(self, data_table, field_names = []):
        if self._if_list_not_empty(data_table):
            return

        with open("{}.csv".format(self.file_name), 'w') as csvfile:
            field_names, columns = self._prepare_columns_and_filed_names(
                field_names)

            csv_writer = DictWriter(csvfile, fieldnames = field_names)
            csv_writer.writeheader()

            for move_data in data_table:
                move_data_dict = self._prepare_move_data_dict(
                    move_data, field_names, columns)
                csv_writer.writerow(move_data_dict)


if __name__ == '__main__':
    url = "http://www.imdb.com/chart/top?ref=ft_250"
    top_moviesSelector = TopMoveSelector(url)
    top_moviesSelector.get_top_movies()

    top_moviesSelector.sort_movies_by_title()
    top_moviesSelector.sort_movies_by_year()

    csv = CsvDataHandler("for_title_and_year")
    csv.save_data_to_csv(top_moviesSelector.top_movies, ['title', 'year'])

    top_moviesSelector.sort_movies_by_year()
    top_moviesSelector.sort_movies_by_title()
    top_moviesSelector.sort_movies_by_number()

    csv = CsvDataHandler("for_all_data")
    csv.save_data_to_csv(top_moviesSelector.top_movies, ['number', 'title', 'year'])