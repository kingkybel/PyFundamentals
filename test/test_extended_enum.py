#!/bin/env python3
# Repository:   https://github.com/PyFundamentals
# File Name:    test/test_extended_enums.py
# Description:  test extended enums
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

import unittest
from enum import auto

from fundamentals.exceptions import ExtendedEnumError
from fundamentals.extended_enum import ExtendedEnum, EnumListType, ExtendedFlag, match_one_alternative, always_match


class ExtendedEnumTests(unittest.TestCase):

    def test_always_match(self):
        self.assertTrue(always_match(None))
        self.assertTrue(always_match(1))
        self.assertTrue(always_match("test"))

    def test_match_one_alternative_basic(self):
        # Test basic matching
        matched, reval, matches = match_one_alternative("abc", ["abc", "def", "ghi"])
        self.assertEqual(matched, "abc")
        self.assertEqual(reval, 0)
        self.assertEqual(matches, ["abc"])

        # Test no match
        matched, reval, matches = match_one_alternative("xyz", ["abc", "def", "ghi"])
        self.assertIsNone(matched)
        self.assertEqual(reval, -1)
        self.assertEqual(matches, [])

        # Test multiple matches
        matched, reval, matches = match_one_alternative("a", ["abc", "ade", "ghi"])
        self.assertIsNone(matched)
        self.assertEqual(reval, -1)
        self.assertEqual(matches, ["abc", "ade"])

    def test_match_one_alternative_consecutive(self):
        # Order suffices by default
        matched, reval, matches = match_one_alternative("ac", ["abc", "def"])
        self.assertEqual(matched, "abc")

        # Consecutive only
        matched, reval, matches = match_one_alternative("ac", ["abc", "def"], consecutive_only=True)
        self.assertIsNone(matched)
        self.assertEqual(reval, -1)

        matched, reval, matches = match_one_alternative("ab", ["abc", "def"], consecutive_only=True)
        self.assertEqual(matched, "abc")

    def test_match_one_alternative_delimiter(self):
        matched, reval, matches = match_one_alternative("abc", "abc|def|ghi", delimiter="|")
        self.assertEqual(matched, "abc")

    def test_match_one_alternative_predicate(self):
        def length_predicate(s) -> bool:
            return len(s) > 3

        matched, reval, matches = match_one_alternative("a", ["abc", "abcd"], predicate=length_predicate)
        self.assertEqual(matched, "abcd")

    def test_match_one_alternative_errors(self):
        with self.assertRaises(ValueError):
            match_one_alternative("", ["abc"])

        with self.assertRaises(ValueError):
            match_one_alternative("a", ["abc", ""])

    def test_create_enum(self):
        class SimpleEnum(ExtendedEnum):
            SIMPLE1 = 0
            SIMPLE2 = 1
            SIMPLE3 = 2

        self.assertListEqual(SimpleEnum.list(EnumListType.NAME), ["SIMPLE1", "SIMPLE2", "SIMPLE3"])
        self.assertListEqual(SimpleEnum.list(EnumListType.STR), ["SimpleEnum.SIMPLE1",
                                                                 "SimpleEnum.SIMPLE2",
                                                                 "SimpleEnum.SIMPLE3"])
        self.assertListEqual(SimpleEnum.list(EnumListType.VALUE), [0, 1, 2])
        self.assertListEqual(SimpleEnum.list(EnumListType.ITEM), [SimpleEnum.SIMPLE1,
                                                                  SimpleEnum.SIMPLE2,
                                                                  SimpleEnum.SIMPLE3])

    def test_create_flag(self):
        class SimpleFlag(ExtendedFlag):
            SIMPLE1 = auto()
            SIMPLE2 = auto()
            SIMPLE3 = auto()

        self.assertListEqual(SimpleFlag.list(EnumListType.NAME), ["SIMPLE1", "SIMPLE2", "SIMPLE3"])
        self.assertListEqual(SimpleFlag.list(EnumListType.STR), ["SimpleFlag.SIMPLE1",
                                                                 "SimpleFlag.SIMPLE2",
                                                                 "SimpleFlag.SIMPLE3"])
        self.assertListEqual(SimpleFlag.list(EnumListType.VALUE), [1, 2, 4])
        self.assertListEqual(SimpleFlag.list(EnumListType.ITEM), [SimpleFlag.SIMPLE1,
                                                                  SimpleFlag.SIMPLE2,
                                                                  SimpleFlag.SIMPLE3])

    def test_enum_from_string(self):
        class SimpleEnum(ExtendedEnum):
            SIMPLE1 = 0
            SIMPLE2 = 1
            SIMPLE3 = 2

            def __str__(self):
                match self:
                    case SimpleEnum.SIMPLE1:
                        return "aaa"
                    case SimpleEnum.SIMPLE2:
                        return "bbb"
                    case SimpleEnum.SIMPLE3:
                        return "ccc"

        self.assertEqual(SimpleEnum.SIMPLE1, SimpleEnum.from_string("1"))
        self.assertEqual(SimpleEnum.SIMPLE1, SimpleEnum.from_string("s1"))
        self.assertEqual(SimpleEnum.SIMPLE1, SimpleEnum.from_string("e1"))
        self.assertEqual(SimpleEnum.SIMPLE1, SimpleEnum.from_string("a"))
        self.assertEqual(SimpleEnum.SIMPLE1, SimpleEnum.from_string("aaa"))

    def test_flag_from_string(self):
        class SimpleFlag(ExtendedFlag):
            SIMPLE1 = auto()
            SIMPLE2 = auto()
            SIMPLE3 = auto()

            def __str__(self):
                match self:
                    case SimpleFlag.SIMPLE1:
                        return "aaa"
                    case SimpleFlag.SIMPLE2:
                        return "bbb"
                    case SimpleFlag.SIMPLE3:
                        return "ccc"

        self.assertEqual(SimpleFlag.SIMPLE1, SimpleFlag.from_string("1"))
        self.assertEqual(SimpleFlag.SIMPLE1, SimpleFlag.from_string("s1"))
        self.assertEqual(SimpleFlag.SIMPLE1, SimpleFlag.from_string("e1"))
        self.assertEqual(SimpleFlag.SIMPLE1, SimpleFlag.from_string("a"))
        self.assertEqual(SimpleFlag.SIMPLE1, SimpleFlag.from_string("aaa"))

    def test_enum_from_string_with_string_conversion(self):
        class SimpleEnum(ExtendedEnum):
            SIMPLE1 = "xxx"
            SIMPLE2 = "yyy"
            SIMPLE3 = "zzz"

            def __str__(self):
                match self:
                    case SimpleEnum.SIMPLE1:
                        return "aaa"
                    case SimpleEnum.SIMPLE2:
                        return "bbb"
                    case SimpleEnum.SIMPLE3:
                        return "ccc"

        self.assertEqual(SimpleEnum.SIMPLE1, SimpleEnum.from_string("a"))
        self.assertEqual(SimpleEnum.SIMPLE1, SimpleEnum.from_string("x"))
        self.assertEqual(SimpleEnum.SIMPLE1, SimpleEnum.from_string("1"))
        self.assertEqual(SimpleEnum.SIMPLE1, SimpleEnum.from_string("e1"))

    def test_enum_no_match(self):
        class SimpleEnum(ExtendedEnum):
            SIMPLE1 = "xxx"
            SIMPLE2 = "yyy"
            SIMPLE3 = "zzz"

            def __str__(self):
                match self:
                    case SimpleEnum.SIMPLE1:
                        return "aaa"
                    case SimpleEnum.SIMPLE2:
                        return "bbb"
                    case SimpleEnum.SIMPLE3:
                        return "ccc"

        with self.assertRaises(ExtendedEnumError):
            SimpleEnum.from_string("xy")

        with self.assertRaises(ExtendedEnumError):
            SimpleEnum.from_string("SIM")

    def test_flag_no_match(self):
        class SimpleFlag(ExtendedFlag):
            SIMPLE1 = auto()
            SIMPLE2 = auto()
            SIMPLE3 = auto()

            def __str__(self):
                match self:
                    case SimpleFlag.SIMPLE1:
                        return "aaa"
                    case SimpleFlag.SIMPLE2:
                        return "bbb"
                    case SimpleFlag.SIMPLE3:
                        return "ccc"

        with self.assertRaises(ExtendedEnumError):
            SimpleFlag.from_string("12")

        with self.assertRaises(ExtendedEnumError):
            SimpleFlag.from_string("SIM")

    def test_enum_or(self):
        class SimpleEnum(ExtendedEnum):
            S1 = 1
            S2 = 2
            S3 = 3

        result = SimpleEnum.S1 | SimpleEnum.S2
        self.assertEqual(result, SimpleEnum.S3)
        self.assertIsInstance(result, SimpleEnum)

        # Test NotImplemented
        self.assertEqual(SimpleEnum.S1.__or__(5), NotImplemented)
        self.assertEqual(SimpleEnum.S1.__ror__(5), NotImplemented)

    def test_flag_or(self):
        class SimpleFlag(ExtendedFlag):
            F1 = 1
            F2 = 2

        result = SimpleFlag.F1 | SimpleFlag.F2
        self.assertEqual(result.value, 3)
        self.assertIsInstance(result, SimpleFlag)

        # Test NotImplemented
        self.assertEqual(SimpleFlag.F1.__or__(5), NotImplemented)
        self.assertEqual(SimpleFlag.F1.__ror__(5), NotImplemented)


if __name__ == '__main__':
    unittest.main()
