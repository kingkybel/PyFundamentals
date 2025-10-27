# Repository:   https://github.com/Python-utilities
# File Name:    dkybutils/exceptions.py
# Description:  exception classes derived from Exception to handle exception in this library
#
# Copyright (C) 2024 Dieter J Kybelksties <github@kybelksties.com>
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
# @date: 2024-07-13
# @author: Dieter J Kybelksties

from __future__ import annotations


class BaseScriptError(Exception):
    def __init__(self, message: str = None):
        if message is None:
            message = ""
        self.message = message
        super().__init__(message)


class StringUtilError(BaseScriptError):
    def __init__(self, message: str = None):
        if message is None:
            message = ""
        self.message = message
        super().__init__(message)


class ExtendedEnumError(BaseScriptError):
    def __init__(self, message: str = None):
        if message is None:
            message = ""
        self.message = message
        super().__init__(message)
