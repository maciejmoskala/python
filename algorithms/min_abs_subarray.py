#!/usr/bin/env python

"""
Problem: Find the lowest absolute sum of elements of a subarray
"""

import random
import time
import unittest

class Timeit(object):
    """
    Timeit class is used to calculate function time interval.
    """

    def __init__(self, f):
        self.func = f

    def __call__(self, *args, **kwargs):
        tstart = time.time()
        method_result = self.func(*args, **kwargs)
        tend = time.time()
        print 'Method: %r worked %2.3f sec' % (self.func.__name__, tend-tstart)

        return method_result

    def __get__(self, instance, owner):
        from functools import partial
        return partial(self.__call__, instance)


class MinAbsSubarray():
    """
    MinAbsSubarray class contains functions to find minimal absolute
    sum of a subarray.
    """
    def __init__(self, min_values_range = -10000, max_values_range = 10000):
        self.min_values_range = min_values_range
        self.max_values_range = max_values_range

    def input_list_is_valid(self, input_list):
        """
        This method checks if list elements are numbers between min and max
        value.
        """
        return all((self.min_values_range <= element <= self.max_values_range)
            and isinstance(element, int) for element in input_list)

    @Timeit
    def find_min_abs_subarray(self, input_list):
        """
        This is implementation of Saksow's algorithm with generators. This
        method is the fastest solution to find minimal absolute sum of a
        subarray.
        """
        def get_sum_list_values(input_list):
            sum_value = 0
            for element in input_list:
                sum_value += element
                yield sum_value

        if not self.input_list_is_valid(input_list):
            raise ValueError("Input list values are incorrect")
            return -1

        solution = previous_element = self.max_values_range
        sorted_sum_list = sorted(get_sum_list_values(input_list))

        for element in sorted_sum_list:
            solution = min(abs(element), abs(previous_element-element), solution)
            previous_element = element
            if solution == 0:
               break
        return solution

    @Timeit
    def slow_find_min_abs_subarray(self, input_list):
        """
        This method is the slow solution to find minimal absolute sum
        of a subarray.
        """
        if not self.input_list_is_valid(input_list):
            raise ValueError("Input list values are incorrect")
            return -1

        solution = self.max_values_range
        for index in xrange(len(input_list)):
            sum_of_elements = 0
            for element in input_list[index:]:
                sum_of_elements += element
                solution = min(abs(sum_of_elements), solution)
                if solution == 0:
                   return solution
        return solution

class TestStringMethods(unittest.TestCase):

    def test_randlist(self):
        values_list = [random.randrange(-10000, 10000) for _ in range(100000)]
        min_abs_subarray = MinAbsSubarray()
        mas = min_abs_subarray.find_min_abs_subarray(values_list)
        hcmas = min_abs_subarray.slow_find_min_abs_subarray(values_list)
        self.assertEqual(mas, hcmas)

    def test_same_values_list(self):
        values_list = [100] * 1000
        min_abs_subarray = MinAbsSubarray()
        mas = min_abs_subarray.find_min_abs_subarray(values_list)
        hcmas = min_abs_subarray.slow_find_min_abs_subarray(values_list)
        self.assertEqual(mas, hcmas)


if __name__ == '__main__':
    unittest.main()
