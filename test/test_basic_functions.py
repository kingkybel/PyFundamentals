#!/bin/env python3
# Repository:   https://github.com/PyFundamentals
# File Name:    test/test_basic_functions.py
# Description:  test basic functions
#
# Copyright (C) 2025 Dieter J Kybelksties <github@kybelksties.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# @date: 2025-10-27
# @author: Dieter J Kybelksties

import unittest
import re

from fundamentals.basic_functions import is_empty_string, now_string, now_string_short, now_date, now_year


class BasicFunctionsTests(unittest.TestCase):

    def test_is_empty_string(self):
        self.assertTrue(is_empty_string(None))
        self.assertTrue(is_empty_string(""))
        self.assertFalse(is_empty_string(" "))
        self.assertFalse(is_empty_string("\n"))
        self.assertFalse(is_empty_string("hello"))

    def test_now_string(self):
        result = now_string()
        self.assertIsInstance(result, str)
        self.assertRegex(result, r'\d{8}-\d{2}:\d{2}:\d{2}\.\d{6}')

    def test_now_string_short(self):
        result = now_string_short()
        self.assertIsInstance(result, str)
        self.assertRegex(result, r'\d{8}-\d{2}:\d{2}')

    def test_now_date(self):
        result = now_date()
        self.assertIsInstance(result, str)
        self.assertRegex(result, r'\d{4}-\d{2}-\d{2}')

    def test_now_year(self):
        result = now_year()
        self.assertIsInstance(result, str)
        self.assertRegex(result, r'\d{4}')


if __name__ == '__main__':
    unittest.main()
