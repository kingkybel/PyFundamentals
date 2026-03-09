#!/bin/env python3
# Repository:   https://github.com/PyFundamentals
# File Name:    test/test_string_utils_extended.py
# Description:  extended tests for string utilities to improve coverage
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
import re
import unittest
from unittest.mock import patch

from fundamentals.string_utils import FALSE_STRINGS, TRUE_STRINGS, input_value, squeeze_chars, remove_control_chars, \
    matches_any, replace_all, normalise_sentence, get_random_string, \
    contains_at_least_n_of, is_cpp_id, identify_case, snake_to_camel, camel_to_snake, make_cpp_id, \
    split_text_into_chunks, is_utf8_ascii, is_roman_numeral, roman_to_integer


class ExtendedStringUtilsTests(unittest.TestCase):

    def test_input_value_edge_cases(self):
        # Test with empty regex and constraint
        with patch('fundamentals.string_utils.__get_user_input') as mock_input:
            mock_input.return_value = "test"
            result = input_value("var", "help", regex_str="", constraint=None)
            self.assertEqual(result, "test")

    def test_input_value_bool_edge_cases(self):
        with patch('fundamentals.string_utils.__get_user_input') as mock_input:
            # Test all false strings
            for false_str in FALSE_STRINGS:
                mock_input.return_value = false_str
                self.assertFalse(input_value("var", "help", var_type=bool))
            
            # Test all true strings
            for true_str in TRUE_STRINGS:
                mock_input.return_value = true_str
                self.assertTrue(input_value("var", "help", var_type=bool))

    def test_input_value_range_edge_cases(self):
        with patch('fundamentals.string_utils.__get_user_input') as mock_input:
            # Test boundary values
            mock_input.return_value = "10"
            self.assertEqual(input_value("var", "help", var_type=int, constraint=range(10, 20)), 10)
            
            mock_input.return_value = "19"
            self.assertEqual(input_value("var", "help", var_type=int, constraint=range(10, 20)), 19)

    def test_squeeze_chars_edge_cases(self):
        # Test with empty squeeze_set
        self.assertEqual(squeeze_chars("test", ""), "test")
        
        # Test with single character
        self.assertEqual(squeeze_chars("aaa", "a"), "")
        
        # Test with multiple squeeze characters
        self.assertEqual(squeeze_chars("aabbcc", "abc"), "")
        
        # Test with no matching characters
        self.assertEqual(squeeze_chars("xyz", "abc"), "xyz")

    def test_remove_control_chars_edge_cases(self):
        # Test with no control chars
        self.assertEqual(remove_control_chars("hello"), "hello")
        
        # Test with only control chars
        self.assertEqual(remove_control_chars("\n\t\r"), "   ")
        
        # Test with mixed content
        self.assertEqual(remove_control_chars("hello\nworld"), "hello world")

    def test_matches_any_edge_cases(self):
        # Test with None patterns
        self.assertTrue(matches_any("test", None))
        
        # Test with empty string
        self.assertTrue(matches_any("", ""))
        self.assertFalse(matches_any("", "test"))
        
        # Test with multiple patterns including None
        self.assertTrue(matches_any("test", ["", "test"]))
        self.assertFalse(matches_any("test", ["abc", "def"]))

    def test_replace_all_edge_cases(self):
        # Test with empty replacements dict
        self.assertEqual(replace_all("test", {}), "test")

        # Test with empty string
        self.assertEqual(replace_all("", {"a": "b"}), "")

    def test_normalise_sentence_edge_cases(self):
        # Test with empty string
        self.assertEqual(normalise_sentence(""), "")
        
        # Test with only punctuation
        self.assertEqual(normalise_sentence("...!?"), '. . . ! ?')
        
        # Test with custom expected_non_al_nums
        result = normalise_sentence("test@#$%", expected_non_al_nums=["@"])
        self.assertIn("@", result)
        
        # Test with very long squeeze_set
        long_squeeze = " " * 100
        result = normalise_sentence("test" + long_squeeze + "test")
        self.assertEqual(result, "test test")

    def test_get_random_string_edge_cases(self):
        # Test with length 0
        self.assertEqual(get_random_string(0), "")
        
        # Test with custom letters
        result = get_random_string(10, "abc")
        self.assertEqual(len(result), 10)
        for char in result:
            self.assertIn(char, "abc")
        
        # Test with special characters
        result = get_random_string(5, "!@#$%")
        self.assertEqual(len(result), 5)
        for char in result:
            self.assertIn(char, "!@#$%")

    def test_contains_at_least_n_of_edge_cases(self):
        # Test with empty text
        self.assertFalse(contains_at_least_n_of("", ["word"], 1))
        
        # Test with minimum 0
        self.assertTrue(contains_at_least_n_of("test", ["word"], 0))
        
        # Test with empty specified_words
        self.assertFalse(contains_at_least_n_of("test", [], 1))
        
        # Test with overlapping words (this should count each occurrence)
        self.assertTrue(contains_at_least_n_of("test test", ["test"], 2))

    def test_is_cpp_id_edge_cases(self):
        # Test with empty string
        self.assertFalse(is_cpp_id(""))
        
        # Test with single character
        self.assertTrue(is_cpp_id("a"))
        self.assertTrue(is_cpp_id("_"))
        self.assertFalse(is_cpp_id("1"))
        
        # Test with keywords
        self.assertFalse(is_cpp_id("if"))
        self.assertFalse(is_cpp_id("for"))
        self.assertFalse(is_cpp_id("while"))
        
        # Test with special characters
        self.assertFalse(is_cpp_id("test-var"))
        self.assertFalse(is_cpp_id("test.var"))
        self.assertFalse(is_cpp_id("test var"))

    def test_identify_case_edge_cases(self):
        # Test with empty string
        self.assertEqual(identify_case(""), identify_case.NO_IDENTIFIER)
        
        # Test with single character
        self.assertEqual(identify_case("a"), identify_case.SNAKE)
        self.assertEqual(identify_case("A"), identify_case.CONSTANT)
        self.assertEqual(identify_case("_"), identify_case.MIXED)
        
        # Test with numbers
        self.assertEqual(identify_case("test123"), identify_case.MIXED)
        self.assertEqual(identify_case("Test123"), identify_case.MIXED)
        
        # Test with invalid characters
        self.assertEqual(identify_case("test-var"), identify_case.NO_IDENTIFIER)
        self.assertEqual(identify_case("test var"), identify_case.NO_IDENTIFIER)

    def test_snake_to_camel_edge_cases(self):
        # Test with empty string
        self.assertEqual(snake_to_camel(""), "_")
        
        # Test with single underscore
        self.assertEqual(snake_to_camel("_"), "_")
        
        # Test with numbers
        self.assertEqual(snake_to_camel("test_123"), "test123")
        self.assertEqual(snake_to_camel("test_123_test"), "test123Test")

        # Test with leading underscore
        self.assertEqual(snake_to_camel("_test"), "test")

    def test_camel_to_snake_edge_cases(self):
        # Test with empty string
        self.assertEqual(camel_to_snake(""), "")
        
        # Test with single character
        self.assertEqual(camel_to_snake("a"), "a")
        self.assertEqual(camel_to_snake("A"), "a")
        
        # Test with numbers
        self.assertEqual(camel_to_snake("test123"), "test123")
        self.assertEqual(camel_to_snake("test123Test"), "test123_test")
        
        # Test with acronyms
        self.assertEqual("get_u_r_l", camel_to_snake("getURL"))
        self.assertEqual("x_m_l_parser", camel_to_snake("XMLParser") )

    def test_make_cpp_id_edge_cases(self):
        # Test with empty string
        self.assertEqual(make_cpp_id("", identify_case.SNAKE), "_")
        
        # Test with special characters
        self.assertEqual(make_cpp_id("test-var", identify_case.SNAKE), "test_var")
        self.assertEqual(make_cpp_id("test.var", identify_case.SNAKE), "test_var")
        
        # Test with numbers at start
        self.assertEqual(make_cpp_id("123test", identify_case.SNAKE), "_123_test")
        
        # Test with mixed case to snake
        self.assertEqual(make_cpp_id("CamelCase", identify_case.SNAKE), "camel_case")
        
        # Test with snake to camel
        self.assertEqual(make_cpp_id("snake_case", identify_case.CAMEL), "snakeCase")
        
        # Test with snake to class
        self.assertEqual(make_cpp_id("snake_case", identify_case.CLASS), "SnakeCase")
        
        # Test with snake to constant
        self.assertEqual(make_cpp_id("snake_case", identify_case.CONSTANT), "SNAKE_CASE")

    def test_split_text_into_chunks_edge_cases(self):
        # Test with empty string
        self.assertEqual(split_text_into_chunks("", 10), [""])
        
        # Test with single word longer than max_chunk_size
        result = split_text_into_chunks("verylongword", 5)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "verylongword")
        
        # Test with max_chunk_size 1
        result = split_text_into_chunks("a. b.", 1)
        self.assertEqual(len(result), 2)  # "a. ", "b. "

    def test_is_utf8_ascii_edge_cases(self):
        # Test with empty string
        self.assertTrue(is_utf8_ascii(""))
        
        # Test with ASCII characters
        self.assertTrue(is_utf8_ascii("hello"))
        self.assertTrue(is_utf8_ascii("!@#$%^&*()"))
        
        # Test with non-ASCII characters
        self.assertFalse(is_utf8_ascii("héllo"))
        self.assertFalse(is_utf8_ascii("café"))
        self.assertFalse(is_utf8_ascii("naïve"))

    def test_is_roman_numeral_edge_cases(self):
        # Test with empty string
        self.assertFalse(is_roman_numeral(""))
        
        # Test with lowercase
        self.assertTrue(is_roman_numeral("xiv"))
        self.assertTrue(is_roman_numeral("xlviii"))
        
        # Test with invalid characters
        self.assertFalse(is_roman_numeral("abc"))
        self.assertFalse(is_roman_numeral("123"))
        self.assertFalse(is_roman_numeral("x y"))
        
        # Test with very long roman numerals
        self.assertTrue(is_roman_numeral("MMMCMXCIX"))  # 3999

    def test_roman_to_integer_edge_cases(self):
        # Test with invalid roman numerals
        self.assertEqual(roman_to_integer("abc"), -1)
        self.assertEqual(roman_to_integer(""), -1)
        self.assertEqual(roman_to_integer("IIII"), -1)  # Invalid repetition
        
        # Test with valid edge cases
        self.assertEqual(roman_to_integer("I"), 1)
        self.assertEqual(roman_to_integer("V"), 5)
        self.assertEqual(roman_to_integer("X"), 10)
        self.assertEqual(roman_to_integer("L"), 50)
        self.assertEqual(roman_to_integer("C"), 100)
        self.assertEqual(roman_to_integer("D"), 500)
        self.assertEqual(roman_to_integer("M"), 1000)
        
        # Test with subtractive notation
        self.assertEqual(roman_to_integer("IV"), 4)
        self.assertEqual(roman_to_integer("IX"), 9)
        self.assertEqual(roman_to_integer("XL"), 40)
        self.assertEqual(roman_to_integer("XC"), 90)
        self.assertEqual(roman_to_integer("CD"), 400)
        self.assertEqual(roman_to_integer("CM"), 900)

    def test_squeeze_chars_with_special_characters(self):
        # Test with Unicode characters
        self.assertEqual(squeeze_chars("café café", "é"), "caf caf")
        
        # Test with emoji
        self.assertEqual(squeeze_chars(" 😀😀 test", "😀", replace_with='😀'), " 😀 test")
        
        # Test with mixed whitespace
        self.assertEqual(squeeze_chars("test\n\t\r test", "\n\t\r "), "test test")

    def test_remove_control_chars_unicode(self):
        # Test with Unicode control characters
        unicode_control = "\u200b\u200c\u200d"  # Zero-width characters
        result = remove_control_chars("test" + unicode_control + "test")
        self.assertEqual(result, "testtest")

    def test_matches_any_with_complex_patterns(self):
        # Test with complex regex patterns
        self.assertTrue(matches_any("test123", r"\w+\d+"))
        self.assertTrue(matches_any("test_case", r"\w+_\w+"))
        self.assertFalse(matches_any("test-case", r"\w+_\w+"))
        
        # Test with case sensitivity
        self.assertFalse(matches_any("Test", "test", flags=0))  # Case sensitive
        self.assertTrue(matches_any("Test", "test", flags=re.IGNORECASE))  # Case insensitive

    def test_normalise_sentence_with_custom_punctuation(self):
        # Test with custom squeeze_set
        result = normalise_sentence("test...test", squeeze_set=".")
        self.assertEqual(result, "test test")
        
        # Test with custom expected_non_al_nums
        result = normalise_sentence("test@#$test", squeeze_set="$", expected_non_al_nums=["@", "#"])
        self.assertIn("@", result)
        self.assertIn("#", result)
        self.assertNotIn("$", result)

    def test_get_random_string_with_unicode(self):
        # Test with Unicode characters
        unicode_chars = "αβγδε"
        result = get_random_string(5, unicode_chars)
        self.assertEqual(len(result), 5)
        for char in result:
            self.assertIn(char, unicode_chars)

    def test_contains_at_least_n_of_with_regex(self):
        # Test with regex patterns in specified_words
        text = "The quick brown fox jumps over the lazy dog"
        words = [r"\b\w{4}\b", r"\b\w{3}\b"]  # 4-letter and 3-letter words
        # This tests that the function works with regex patterns
        self.assertTrue(contains_at_least_n_of(text, words, 5))

    def test_is_cpp_id_with_unicode(self):
        # Test with Unicode identifiers (should be invalid for C++)
        self.assertFalse(is_cpp_id("αβγ"))  # Greek letters
        self.assertFalse(is_cpp_id("测试"))  # Chinese characters
        
        # Test with valid Unicode that's ASCII-compatible
        self.assertFalse(is_cpp_id("test_α"))  # Mix of ASCII and Unicode

    def test_identify_case_with_unicode(self):
        # Test with Unicode characters
        self.assertEqual(identify_case("αβγ"), identify_case.NO_IDENTIFIER)
        self.assertEqual(identify_case("test_αβγ"), identify_case.NO_IDENTIFIER)

    def test_snake_to_camel_with_unicode(self):
        # Test with Unicode in snake_case
        result = snake_to_camel("test_αβγ")
        self.assertEqual(result, "testΑβγ")  # Greek letters should be capitalized

    def test_camel_to_snake_with_unicode(self):
        # Test with Unicode in camelCase
        self.assertEqual("test_αβγ", camel_to_snake("testΑβγ"))

    def test_make_cpp_id_with_special_cases(self):
        # Test with very long identifiers
        long_id = "a" * 100
        result = make_cpp_id(long_id, identify_case.SNAKE)
        self.assertEqual(result, long_id)
        
        # Test with mixed special characters
        mixed = "test-@#$%^&*()_+="
        result = make_cpp_id(mixed, identify_case.SNAKE)
        self.assertEqual("test", result)

        mixed = "te-@#$%^&*()_+=st"
        result = make_cpp_id(mixed, identify_case.SNAKE)
        self.assertEqual("te_st", result)

    def test_split_text_into_chunks_with_unicode(self):
        # Test with Unicode text
        unicode_text = "αβγ δεζ ηθι κλμ νξο"
        result = split_text_into_chunks(unicode_text, 10)
        self.assertGreater(len(result), 1)
        
        # Test with emojis
        emoji_text = "😀😁😂😃😄 😅😆😇😈😉"
        result = split_text_into_chunks(emoji_text, 5)
        self.assertGreater(len(result), 1)

    def test_is_utf8_ascii_with_edge_cases(self):
        # Test with mixed ASCII and non-ASCII
        mixed = "hello αβγ"
        self.assertFalse(is_utf8_ascii(mixed))
        
        # Test with extended ASCII (should be ASCII)
        extended_ascii = "hello \x7f"
        self.assertTrue(is_utf8_ascii(extended_ascii))

    def test_roman_to_integer_with_edge_cases(self):
        # Test with maximum valid roman numeral
        self.assertEqual(roman_to_integer("MMMCMXCIX"), 3999)
        
        # Test with minimum
        self.assertEqual(roman_to_integer("I"), 1)
        
        # Test with complex combinations
        self.assertEqual(roman_to_integer("MCMXC"), 1990)  # 1000 + 900 + 90
        self.assertEqual(roman_to_integer("MMXXI"), 2021)  # 2000 + 20 + 1


if __name__ == '__main__':
    unittest.main()