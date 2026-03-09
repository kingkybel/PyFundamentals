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
# @date: 2026-03-09
# @author: Dieter J Kybelksties

import unittest
import socket
from unittest.mock import patch, MagicMock

from fundamentals.bash import get_effective_user, get_logged_in_user, number_of_cores, hostname, get_ip, is_tool_installed, \
    assert_is_root, get_external_ip, assert_tools_installed


class BashTests(unittest.TestCase):

    def test_get_effective_user(self):
        user = get_effective_user()
        self.assertIsInstance(user, str)
        self.assertGreater(len(user), 0)

    def test_get_logged_in_user(self):
        user = get_logged_in_user()
        self.assertIsInstance(user, str)

    @patch('os.getlogin')
    @patch('os.popen')
    def test_get_logged_in_user_file_not_found(self, mock_popen, mock_getlogin):
        # Test fallback to whoami when os.getlogin() fails
        mock_getlogin.side_effect = FileNotFoundError()
        mock_process = MagicMock()
        mock_process.read.return_value = "whoami_user\n"
        mock_popen.return_value = mock_process
        
        user = get_logged_in_user()
        self.assertEqual(user, "whoami_user")
        mock_popen.assert_called_once_with("whoami")

    @patch('os.getlogin')
    @patch('os.popen')
    def test_get_logged_in_user_fallback(self, mock_popen, mock_getlogin):
        # Test fallback to whoami when os.getlogin() fails
        mock_getlogin.side_effect = OSError()
        mock_process = MagicMock()
        mock_process.read.return_value = "whoami_user\n"
        mock_popen.return_value = mock_process
        
        user = get_logged_in_user()
        self.assertEqual(user, "whoami_user")
        mock_popen.assert_called_once_with("whoami")

    def test_assert_is_root(self):
        with patch('fundamentals.bash.get_effective_user', return_value="root"):
            # Should not raise
            assert_is_root()
        
        with patch('fundamentals.bash.get_effective_user', return_value="not_root"):
            with self.assertRaises(SystemExit):
                with patch('builtins.print'):  # suppress print
                    assert_is_root()

    def test_number_of_cores(self):
        cores = number_of_cores()
        self.assertIsInstance(cores, int)
        self.assertGreater(cores, 0)

    def test_hostname(self):
        hn = hostname()
        self.assertIsInstance(hn, str)
        self.assertGreater(len(hn), 0)

    def test_get_ip(self):
        ip = get_ip()
        self.assertIsInstance(ip, str)
        # Should be a valid IP
        try:
            socket.inet_aton(ip)
        except socket.error:
            self.fail("get_ip returned invalid IP")

    @patch('socket.socket')
    def test_get_ip_error(self, mock_socket):
        mock_s = MagicMock()
        mock_s.connect.side_effect = socket.error()
        mock_socket.return_value = mock_s
        
        ip = get_ip()
        self.assertEqual(ip, "127.0.0.1")

    @patch('urllib.request.urlopen')
    def test_get_external_ip(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = b"1.2.3.4"
        mock_urlopen.return_value = mock_response
        
        ip = get_external_ip()
        self.assertEqual(ip, "1.2.3.4")

    def test_is_tool_installed(self):
        # Test a common tool
        self.assertTrue(is_tool_installed("python") or is_tool_installed("python3"))
        self.assertFalse(is_tool_installed("nonexistent_tool_12345"))

    def test_assert_tools_installed(self):
        with patch('fundamentals.bash.is_tool_installed', return_value=True):
            # Should not raise
            assert_tools_installed("ls")
            assert_tools_installed(["ls", "cat"])
            
        with patch('fundamentals.bash.is_tool_installed', return_value=False):
            with self.assertRaises(SystemExit):
                with patch('builtins.print'):  # suppress print
                    assert_tools_installed("nonexistent_tool")


if __name__ == '__main__':
    unittest.main()
