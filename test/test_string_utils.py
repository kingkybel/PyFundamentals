#!/bin/env python3
# Repository:   https://github.com/PyFundamentals
# File Name:    test/test_string_utils.py
# Description:  test string utilities
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
# @date: 2026-03-09
# @author: Dieter J Kybelksties

import unittest
from unittest.mock import patch

from fundamentals.string_utils import squeeze_chars, matches_any, normalise_sentence, roman_to_integer, is_roman_numeral, \
    identify_case, IdentifierStringCase, make_cpp_id, remove_control_chars, replace_all, get_random_string, is_cpp_id, \
    snake_to_camel, camel_to_snake, split_text_into_chunks, is_utf8_ascii, StringUtilError, input_value, contains_at_least_n_of


class BasicFunctionsTests(unittest.TestCase):

    def test_squeeze_chars_error(self):
        with self.assertRaises(StringUtilError):
            squeeze_chars("abc", "a", replace_with="XX")

    def test_input_value(self):
        with patch('fundamentals.string_utils.__get_user_input', return_value="test"):
            pass

    def test_contains_at_least_n_of(self):
        self.assertFalse(contains_at_least_n_of("text", None))
        self.assertTrue(contains_at_least_n_of("text", ["word"], minimum=0))
        self.assertTrue(contains_at_least_n_of("hello world", ["hello", "world"], minimum=2))
        self.assertFalse(contains_at_least_n_of("hello world", ["hello", "universe"], minimum=2))

    def test_split_text_into_chunks(self):
        text = "Sentence one. Sentence two? Sentence three."
        chunks = split_text_into_chunks(text, 15)
        self.assertTrue(len(chunks) >= 3)

    def test_input_value_mocked(self):
        with patch('fundamentals.string_utils.__get_user_input') as mock_input:
             # Test str
             mock_input.return_value = "hello"
             self.assertEqual(input_value("var", "help"), "hello")
             
             # Test int
             mock_input.return_value = "123"
             self.assertEqual(input_value("var", "help", var_type=int), 123)
             
             # Test bool
             mock_input.return_value = "true"
             self.assertTrue(input_value("var", "help", var_type=bool))
             
             # Test regex failure then success
             mock_input.side_effect = ["abc", "123"]
             with patch('builtins.print'):
                 self.assertEqual(input_value("var", "help", regex_str=r"\d+"), "123")
                 
             # Test range constraint failure then success
             mock_input.side_effect = ["20", "15"]
             with patch('builtins.print'):
                 self.assertEqual(input_value("var", "help", var_type=int, constraint=range(10, 20)), 15)

             # Test list constraint failure then success
             mock_input.side_effect = ["c", "a"]
             with patch('builtins.print'):
                 self.assertEqual(input_value("var", "help", constraint=["a", "b"]), "a")

    def test_input_value_value_error(self):
        with self.assertRaises(ValueError):
            input_value("var", "help", regex_str=".*", constraint=["a"])

    def test_squeeze_chars(self):
        self.assertEqual("", squeeze_chars(source="", squeeze_set="\n\t\r ", replace_with=" "))
        self.assertEqual("", squeeze_chars(source="  \n \n\t ", squeeze_set="\n\t\r ", replace_with=" "))
        self.assertEqual("some text with whitespace",
                         squeeze_chars(source="\t \nsome  \n \n\t text   \r with  whitespace \n",
                                       squeeze_set="\n\t\r ",
                                       replace_with=" "))

    def test_matches_any(self):
        self.assertTrue(matches_any("string to test"))
        self.assertTrue(matches_any("string to test", patterns=""))
        self.assertTrue(matches_any("string to test", patterns="s.*t"))
        self.assertTrue(matches_any("string to test", patterns="s.*to.*t"))
        self.assertFalse(matches_any("string to test", patterns="to"))
        self.assertFalse(matches_any("string to test", patterns="STRING to test"))
        self.assertTrue(matches_any("string to test", patterns=["STRING to test", "s.*"]))

    def test_clean_sentence_string(self):
        sentence = "This website! includes information ,about Project Gutenberg™ to hear about new eBooks."
        expected_clean_sentence = \
            "This website ! includes information , about Project Gutenberg™ to hear about new eBooks ."
        result = normalise_sentence(sentence=sentence)
        self.assertEqual(result, expected_clean_sentence)

    def test_is_roman_numeral(self):
        self.assertTrue(is_roman_numeral("XIV"))
        self.assertTrue(is_roman_numeral("lX"))  # True (case-insensitive)
        self.assertFalse(is_roman_numeral("abc"))

    def test_roman_to_integer(self):
        self.assertEqual(roman_to_integer("III"), 3)
        self.assertEqual(roman_to_integer("IX"), 9)
        self.assertEqual(roman_to_integer("LVIII"), 58)
        self.assertEqual(roman_to_integer("MCMXCIV"), 1994)

        self.assertEqual(roman_to_integer("abc"), -1)

    def test_identify_case(self):
        self.assertEqual(identify_case("snake_case"), IdentifierStringCase.SNAKE)
        self.assertEqual(identify_case("camelCase"), IdentifierStringCase.CAMEL)
        self.assertEqual(identify_case("CamelCase"), IdentifierStringCase.CLASS)
        self.assertEqual(identify_case("mixed_Case"), IdentifierStringCase.MIXED)
        self.assertEqual(identify_case("Mixed_Case"), IdentifierStringCase.MIXED)

    def test_constant_conversion(self):
        self.assertEqual(make_cpp_id("this_is_constant_case", IdentifierStringCase.CONSTANT),
                         "THIS_IS_CONSTANT_CASE")
        self.assertEqual(make_cpp_id("ThisIsConstantCase", IdentifierStringCase.CONSTANT),
                         "THIS_IS_CONSTANT_CASE")
        self.assertEqual(make_cpp_id("thisIsConstantCase", IdentifierStringCase.CONSTANT),
                         "THIS_IS_CONSTANT_CASE")
        self.assertEqual(make_cpp_id("thisIs_Constant_Case", IdentifierStringCase.CONSTANT),
                         "THIS_IS__CONSTANT__CASE")

    def test_no_identifier_conversion(self):
        self.assertEqual(make_cpp_id("This is not valid!", IdentifierStringCase.SNAKE), "this_is_not_valid")
        self.assertEqual(make_cpp_id("This is not valid!", IdentifierStringCase.CLASS), "ThisIsNotValid")
        self.assertEqual(make_cpp_id("This is not valid!", IdentifierStringCase.CONSTANT), "THIS_IS_NOT_VALID")
        self.assertEqual(make_cpp_id("This is not valid!", IdentifierStringCase.MIXED), "This_is_not_valid")
        self.assertEqual(make_cpp_id("This is not valid!", IdentifierStringCase.CAMEL), "thisIsNotValid")

    def test_empty_id_string(self):
        self.assertEqual(make_cpp_id("", IdentifierStringCase.SNAKE), "_")
        self.assertEqual(make_cpp_id("", IdentifierStringCase.CAMEL), "_")
        self.assertEqual(make_cpp_id("", IdentifierStringCase.CLASS), "_")
        self.assertEqual(make_cpp_id("", IdentifierStringCase.CONSTANT), "_")
        self.assertEqual(make_cpp_id("", IdentifierStringCase.MIXED), "_")

    def test_numbered_id_string(self):
        self.assertEqual(make_cpp_id("this is numbered 1234.341", IdentifierStringCase.SNAKE),
                         "this_is_numbered_1234_341")
        self.assertEqual(make_cpp_id("this is numbered 1234.341", IdentifierStringCase.CONSTANT),
                         "THIS_IS_NUMBERED_1234_341")
        self.assertEqual(make_cpp_id("This is Numbered 1234.341", IdentifierStringCase.MIXED),
                         "This_is_Numbered_1234_341")
        self.assertEqual(make_cpp_id("111this is numbered 1234.341", IdentifierStringCase.SNAKE),
                         "_111_this_is_numbered_1234_341")
        self.assertEqual(make_cpp_id("111this is numbered 1234.341", IdentifierStringCase.CLASS),
                         "_111ThisIsNumbered1234_341")

    def test_remove_control_chars(self):
        self.assertEqual(remove_control_chars("hello\x00world"), "hello world")
        self.assertEqual(remove_control_chars("test\n\t\r"), "test   ")

    def test_replace_all(self):
        self.assertEqual(replace_all("hello world", {" ": "_"}), "hello_world")
        self.assertEqual(replace_all("abc", {"a": "A", "c": "C"}), "AbC")

    def test_get_random_string(self):
        s = get_random_string(10)
        self.assertEqual(len(s), 10)
        self.assertIsInstance(s, str)

    def test_is_cpp_id(self):
        self.assertTrue(is_cpp_id("valid_id"))
        self.assertFalse(is_cpp_id("123invalid"))
        self.assertFalse(is_cpp_id("invalid-id"))

    def test_snake_to_camel(self):
        self.assertEqual(snake_to_camel("snake_case"), "snakeCase")
        self.assertEqual(snake_to_camel("test"), "test")

    def test_camel_to_snake(self):
        self.assertEqual(camel_to_snake("CamelCase"), "camel_case")
        self.assertEqual(camel_to_snake("test"), "test")



    def test_is_utf8_ascii(self):
        self.assertTrue(is_utf8_ascii("hello"))
        self.assertFalse(is_utf8_ascii("héllo"))


if __name__ == '__main__':
    unittest.main()
