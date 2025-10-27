#!/bin/env python3
# Repository:   https://github.com/PyFundamentals
# File Name:    test/test_bash.py
# Description:  test bash utilities
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
import socket

from fundamentals.bash import get_effective_user, get_logged_in_user, number_of_cores, hostname, get_ip, is_tool_installed


class BashTests(unittest.TestCase):

    def test_get_effective_user(self):
        user = get_effective_user()
        self.assertIsInstance(user, str)
        self.assertTrue(len(user) > 0)

    def test_get_logged_in_user(self):
        user = get_logged_in_user()
        self.assertIsInstance(user, str)
        self.assertTrue(len(user) > 0)

    def test_number_of_cores(self):
        cores = number_of_cores()
        self.assertIsInstance(cores, int)
        self.assertGreater(cores, 0)

    def test_hostname(self):
        hn = hostname()
        self.assertIsInstance(hn, str)
        self.assertTrue(len(hn) > 0)

    def test_get_ip(self):
        ip = get_ip()
        self.assertIsInstance(ip, str)
        # Should be a valid IP
        try:
            socket.inet_aton(ip)
        except socket.error:
            self.fail("get_ip returned invalid IP")

    def test_is_tool_installed(self):
        # Test a common tool
        self.assertTrue(is_tool_installed("python") or is_tool_installed("python3"))
        self.assertFalse(is_tool_installed("nonexistent_tool_12345"))


if __name__ == '__main__':
    unittest.main()
