#!/bin/env python3
# Repository:   https://github.com/PyFundamentals
# File Name:    test/test_exceptions_extended.py
# Description:  extended tests for exceptions to improve coverage
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

from fundamentals.exceptions import BaseScriptError, StringUtilError, ExtendedEnumError


class ExtendedExceptionsTests(unittest.TestCase):

    def test_BaseScriptError_inheritance(self):
        # Test that BaseScriptError inherits from Exception
        e = BaseScriptError()
        self.assertIsInstance(e, Exception)
        self.assertIsInstance(e, BaseScriptError)

    def test_BaseScriptError_with_message(self):
        message = "Test error message"
        e = BaseScriptError(message)
        self.assertEqual(e.message, message)
        self.assertEqual(str(e), message)

    def test_BaseScriptError_with_empty_message(self):
        e = BaseScriptError("")
        self.assertEqual(e.message, "")
        self.assertEqual(str(e), "")

    def test_BaseScriptError_with_none_message(self):
        e = BaseScriptError(None)
        self.assertEqual(e.message, "")
        self.assertEqual(str(e), "")

    def test_BaseScriptError_with_special_characters(self):
        message = "Error with special chars: !@#$%^&*()"
        e = BaseScriptError(message)
        self.assertEqual(e.message, message)

    def test_BaseScriptError_with_unicode(self):
        message = "Error with unicode: αβγ δεζ"
        e = BaseScriptError(message)
        self.assertEqual(e.message, message)

    def test_BaseScriptError_with_long_message(self):
        message = "A" * 1000
        e = BaseScriptError(message)
        self.assertEqual(e.message, message)

    def test_StringUtilError_inheritance(self):
        # Test that StringUtilError inherits from BaseScriptError
        e = StringUtilError()
        self.assertIsInstance(e, BaseScriptError)
        self.assertIsInstance(e, StringUtilError)
        self.assertIsInstance(e, Exception)

    def test_StringUtilError_with_message(self):
        message = "String utility error"
        e = StringUtilError(message)
        self.assertEqual(e.message, message)
        self.assertEqual(str(e), message)

    def test_StringUtilError_with_empty_message(self):
        e = StringUtilError("")
        self.assertEqual(e.message, "")
        self.assertEqual(str(e), "")

    def test_StringUtilError_with_none_message(self):
        e = StringUtilError(None)
        self.assertEqual(e.message, "")
        self.assertEqual(str(e), "")

    def test_StringUtilError_with_special_characters(self):
        message = "String error with special chars: \n\t\r"
        e = StringUtilError(message)
        self.assertEqual(e.message, message)

    def test_StringUtilError_with_unicode(self):
        message = "String error with unicode: 测试错误"
        e = StringUtilError(message)
        self.assertEqual(e.message, message)

    def test_StringUtilError_with_long_message(self):
        message = "String error: " + "X" * 500
        e = StringUtilError(message)
        self.assertEqual(e.message, message)

    def test_ExtendedEnumError_inheritance(self):
        # Test that ExtendedEnumError inherits from BaseScriptError
        e = ExtendedEnumError()
        self.assertIsInstance(e, BaseScriptError)
        self.assertIsInstance(e, ExtendedEnumError)
        self.assertIsInstance(e, Exception)

    def test_ExtendedEnumError_with_message(self):
        message = "Extended enum error"
        e = ExtendedEnumError(message)
        self.assertEqual(e.message, message)
        self.assertEqual(str(e), message)

    def test_ExtendedEnumError_with_empty_message(self):
        e = ExtendedEnumError("")
        self.assertEqual(e.message, "")
        self.assertEqual(str(e), "")

    def test_ExtendedEnumError_with_none_message(self):
        e = ExtendedEnumError(None)
        self.assertEqual(e.message, "")
        self.assertEqual(str(e), "")

    def test_ExtendedEnumError_with_special_characters(self):
        message = "Enum error with special chars: []{}()"
        e = ExtendedEnumError(message)
        self.assertEqual(e.message, message)

    def test_ExtendedEnumError_with_unicode(self):
        message = "Enum error with unicode: αβγ"
        e = ExtendedEnumError(message)
        self.assertEqual(e.message, message)

    def test_ExtendedEnumError_with_long_message(self):
        message = "Extended enum error: " + "Y" * 1000
        e = ExtendedEnumError(message)
        self.assertEqual(e.message, message)

    def test_exception_raising_and_catching(self):
        # Test raising and catching BaseScriptError
        try:
            raise BaseScriptError("Test error")
        except BaseScriptError as e:
            self.assertEqual(e.message, "Test error")
        
        # Test raising and catching StringUtilError
        try:
            raise StringUtilError("String error")
        except StringUtilError as e:
            self.assertEqual(e.message, "String error")
        except BaseScriptError as e:
            # Should also catch as BaseScriptError due to inheritance
            self.assertEqual(e.message, "String error")
        
        # Test raising and catching ExtendedEnumError
        try:
            raise ExtendedEnumError("Enum error")
        except ExtendedEnumError as e:
            self.assertEqual(e.message, "Enum error")
        except BaseScriptError as e:
            # Should also catch as BaseScriptError due to inheritance
            self.assertEqual(e.message, "Enum error")

    def test_exception_chaining(self):
        # Test exception chaining
        try:
            try:
                raise ValueError("Original error")
            except ValueError as e:
                raise BaseScriptError("Wrapped error") from e
        except BaseScriptError as e:
            self.assertEqual(e.message, "Wrapped error")
            self.assertIsInstance(e.__cause__, ValueError)
            self.assertEqual(str(e.__cause__), "Original error")

    def test_exception_with_args(self):
        # Test exception with args
        e = BaseScriptError("Test message")
        self.assertEqual(len(e.args), 1)
        self.assertEqual(e.args[0], "Test message")

    def test_exception_str_representation(self):
        # Test string representation
        e1 = BaseScriptError()
        self.assertEqual(str(e1), "")
        
        e2 = BaseScriptError("Error message")
        self.assertEqual(str(e2), "Error message")
        
        e3 = StringUtilError("String error")
        self.assertEqual(str(e3), "String error")
        
        e4 = ExtendedEnumError("Enum error")
        self.assertEqual(str(e4), "Enum error")

    def test_exception_repr(self):
        # Test repr representation
        e1 = BaseScriptError()
        self.assertIn("BaseScriptError", repr(e1))
        
        e2 = BaseScriptError("Test")
        self.assertIn("BaseScriptError", repr(e2))
        self.assertIn("Test", repr(e2))

    def test_exception_comparison(self):
        # Test that exceptions with same message are equal
        e1 = BaseScriptError("Same message")
        e2 = BaseScriptError("Same message")
        self.assertNotEqual(e1, e2)  # Exceptions are not equal even with same message
        
        # But messages should be equal
        self.assertEqual(e1.message, e2.message)

    def test_exception_hash(self):
        # Test that exceptions are hashable (they are by default in Python)
        e = BaseScriptError("Test")
        # Exceptions should be hashable
        hash_value = hash(e)
        self.assertIsInstance(hash_value, int)

    def test_exception_context(self):
        # Test exception context
        try:
            try:
                raise BaseScriptError("First error")
            except BaseScriptError:
                raise StringUtilError("Second error")
        except StringUtilError as e:
            self.assertEqual(e.message, "Second error")
            self.assertIsInstance(e.__context__, BaseScriptError)
            self.assertEqual(e.__context__.message, "First error")

    def test_exception_with_traceback(self):
        # Test that exceptions have traceback
        import traceback
        
        try:
            raise BaseScriptError("Test traceback")
        except BaseScriptError as e:
            self.assertIsNotNone(e.__traceback__)
            tb_str = traceback.format_tb(e.__traceback__)
            self.assertIsInstance(tb_str, list)
            self.assertGreater(len(tb_str), 0)

    def test_exception_inheritance_hierarchy(self):
        # Test the full inheritance hierarchy
        e = StringUtilError("Test")
        self.assertIsInstance(e, Exception)
        self.assertIsInstance(e, BaseScriptError)
        self.assertIsInstance(e, StringUtilError)
        
        e2 = ExtendedEnumError("Test")
        self.assertIsInstance(e2, Exception)
        self.assertIsInstance(e2, BaseScriptError)
        self.assertIsInstance(e2, ExtendedEnumError)

    def test_exception_message_modification(self):
        # Test that message can be modified
        e = BaseScriptError("Original")
        self.assertEqual(e.message, "Original")
        
        e.message = "Modified"
        self.assertEqual(e.message, "Modified")

    def test_exception_with_multiple_lines(self):
        # Test with multi-line messages
        message = "Line 1\nLine 2\nLine 3"
        e = BaseScriptError(message)
        self.assertEqual(e.message, message)

    def test_exception_with_formatting(self):
        # Test with formatted messages
        name = "test"
        value = 42
        message = f"Error with {name} = {value}"
        e = BaseScriptError(message)
        self.assertEqual(e.message, message)

    def test_exception_performance(self):
        # Test that creating exceptions is reasonably fast
        import time
        
        start_time = time.time()
        for _ in range(1000):
            BaseScriptError("Test")
        end_time = time.time()
        
        # Should be very fast (less than 1 second for 1000 exceptions)
        self.assertLess(end_time - start_time, 1.0)

    def test_exception_memory_usage(self):
        # Test that exceptions don't use excessive memory
        import sys
        
        e = BaseScriptError("Test message")
        memory_size = sys.getsizeof(e)
        
        # Should be reasonable size (less than 1KB)
        self.assertLess(memory_size, 1024)


if __name__ == '__main__':
    unittest.main()