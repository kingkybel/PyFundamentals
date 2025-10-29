#!/bin/env python3
# Repository:   https://github.com/PyFundamentals
# File Name:    test/test_thread_with_return.py
# Description:  test thread with return
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

from fundamentals.thread_with_return import ReturningThread


def func_to_test(x, y=10):
    return x + y


class ThreadWithReturnTests(unittest.TestCase):

    def test_returning_thread(self):
        t = ReturningThread(target=func_to_test, args=(5,))
        t.start()
        result = t.join()
        self.assertEqual(result, 15)

        t = ReturningThread(target=func_to_test, args=(3,), kwargs={'y': 7})
        t.start()
        result = t.join()
        self.assertEqual(result, 10)

    def test_no_target(self):
        t = ReturningThread()
        t.start()
        result = t.join()
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
