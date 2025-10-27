# Repository:   https://github.com/PyFundamentals
# File Name:    fundamentals/basic_functions.py
# Description:  basic utilities
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

from __future__ import annotations

from datetime import datetime


def is_empty_string(string: str = None):
    return string is None or string == ""


def now_string() -> str:
    return datetime.now(tz=None).strftime("%Y%m%d-%H:%M:%S.%f")


def now_string_short() -> str:
    return datetime.now(tz=None).strftime("%Y%m%d-%H:%M")


def now_date() -> str:
    return datetime.now(tz=None).strftime("%Y-%m-%d")


def now_year() -> str:
    return datetime.now(tz=None).strftime("%Y")
