#!/bin/env python3
# Repository:   https://github.com/PyFundamentals
# File Name:    test/test_overrides_extended.py
# Description:  extended tests for overrides to improve coverage
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
from unittest.mock import patch

from fundamentals.overrides import OverrideChecker, overrides


class ExtendedOverrideCheckerTests(unittest.TestCase):

    def test_init_with_complex_method(self):
        def complex_method(self, a, b, *args, **kwargs):
            return a + b + sum(args) + sum(kwargs.values())

        checker = OverrideChecker(complex_method)
        self.assertEqual(checker.method, complex_method)
        self.assertIsNone(checker.interface_class)
        self.assertIsNone(checker.name)
        self.assertIsNone(checker.owner)

    def test_set_name_with_interface_class_complex(self):
        class Interface:
            def complex_method(self, a, b, *args, **kwargs):
                pass

        class Implementation:
            @overrides(Interface)
            def complex_method(self, a, b, *args, **kwargs):
                return a + b + sum(args) + sum(kwargs.values())

        impl = Implementation()
        # The descriptor should be set up correctly
        self.assertTrue(hasattr(impl, 'complex_method'))

    def test_set_name_without_interface_class_complex(self):
        class Interface:
            def complex_method(self, a, b, *args, **kwargs):
                pass

        class Implementation(Interface):
            @overrides
            def complex_method(self, a, b, *args, **kwargs):
                return a + b + sum(args) + sum(kwargs.values())

        impl = Implementation()
        # The descriptor should be set up correctly
        self.assertTrue(hasattr(impl, 'complex_method'))

    def test_set_name_with_default_parameters(self):
        class Interface:
            def method_with_defaults(self, a, b=10, c="default"):
                pass

        class Implementation:
            @overrides(Interface)
            def method_with_defaults(self, a, b=10, c="default"):
                return a + b

        impl = Implementation()
        self.assertTrue(hasattr(impl, 'method_with_defaults'))

    def test_set_name_missing_default_parameter(self):
        with self.assertRaises(AssertionError) as cm:
            class Interface:
                def method_with_defaults(self, a, b=10, c="default"):
                    pass

            class Implementation(Interface):
                @overrides
                def method_with_defaults(self, a, b=10):  # Missing parameter c
                    pass

            impl = Implementation()
        self.assertIn("Method method_with_defaults missing parameter c", str(cm.exception))

    def test_set_name_extra_parameter(self):
        with self.assertRaises(AssertionError) as cm:
            class Interface:
                def method(self, a, b):
                    pass

            class Implementation(Interface):
                @overrides
                def method(self, a, b, c):  # Extra parameter
                    pass

            impl = Implementation()
        self.assertIn("Method method extra parameter c", str(cm.exception))

    def test_set_name_parameter_type_mismatch(self):
        # Note: The current implementation doesn't check types
        # This test documents that type mismatches are allowed
        class Interface:
            def method(self, a: int, b: str):
                pass

        class Implementation(Interface):
            @overrides
            def method(self, a: str, b: int):  # Type mismatch
                pass

        impl = Implementation()
        # The method should be allowed since type checking is not implemented
        self.assertTrue(hasattr(impl, 'method'))

    def test_set_name_positional_only_parameters(self):
        with self.assertRaises(AssertionError) as cm:
            class Interface:
                def method(self, a, b, /):  # Positional-only parameters
                    pass

            class Implementation(Interface):
                @overrides
                def method(self, a, b):  # Not positional-only
                    pass

            impl = Implementation()
        # Note: The current implementation might not handle positional-only parameters correctly

    def test_set_name_keyword_only_parameters(self):
        with self.assertRaises(AssertionError) as cm:
            class Interface:
                def method(self, a, *, b, c):  # Keyword-only parameters
                    pass

            class Implementation(Interface):
                @overrides
                def method(self, a, b, c):  # Not keyword-only
                    pass

            impl = Implementation()
        # Note: The current implementation might not handle keyword-only parameters correctly

    def test_get_instance_method_complex(self):
        class Interface:
            def complex_method(self, a, b, *args, **kwargs):
                pass

        class Implementation(Interface):
            @overrides
            def complex_method(self, a, b, *args, **kwargs):
                return f"result: {a + b + sum(args) + sum(kwargs.values())}"

        impl = Implementation()
        result = impl.complex_method(1, 2, 3, 4, x=5, y=6)
        self.assertEqual(result, "result: 21")

    def test_overrides_decorator_with_class_complex(self):
        class Interface:
            def method1(self):
                pass

            def method2(self, a, b):
                pass

            def method3(self, *args, **kwargs):
                pass

        class Implementation:
            @overrides(Interface)
            def method1(self):
                return "method1"

            @overrides(Interface)
            def method2(self, a, b):
                return f"method2: {a + b}"

            @overrides(Interface)
            def method3(self, *args, **kwargs):
                return f"method3: {args}, {kwargs}"

        impl = Implementation()
        self.assertEqual(impl.method1(), "method1")
        self.assertEqual(impl.method2(1, 2), "method2: 3")
        self.assertEqual(impl.method3(1, 2, 3, x=4, y=5), "method3: (1, 2, 3), {'x': 4, 'y': 5}")

    def test_overrides_decorator_without_parens_complex(self):
        class Interface:
            def method1(self):
                pass

            def method2(self, a, b):
                pass

        class Implementation(Interface):
            @overrides
            def method1(self):
                return "method1"

            @overrides
            def method2(self, a, b):
                return f"method2: {a + b}"

        impl = Implementation()
        self.assertEqual(impl.method1(), "method1")
        self.assertEqual(impl.method2(1, 2), "method2: 3")

    def test_overrides_new_with_callable_complex(self):
        def dummy_method(self, a, b, *args, **kwargs):
            return a + b + sum(args) + sum(kwargs.values())

        result = overrides(dummy_method)
        self.assertIsInstance(result, OverrideChecker)
        self.assertEqual(result.method, dummy_method)

    def test_overrides_new_with_type_complex(self):
        result = overrides(str)
        self.assertIsInstance(result, overrides)
        self.assertEqual(result.interface_class, str)

    def test_override_checker_error_messages(self):
        with self.assertRaises(AssertionError) as cm:
            class Interface:
                def method(self, a, b):
                    pass

            class Implementation(Interface):
                @overrides
                def method(self, a):  # Missing parameter b
                    pass

            impl = Implementation()
        
        error_message = str(cm.exception)
        self.assertIn("Method method missing parameter b", error_message)

    def test_override_checker_with_various_parameter_kinds(self):
        with self.assertRaises(AssertionError) as cm:
            class Interface:
                def method(self, a, *args, **kwargs):
                    pass

            class Implementation(Interface):
                @overrides
                def method(self, a, **kwargs):  # Missing *args
                    pass

            impl = Implementation()
        
        error_message = str(cm.exception)
        self.assertIn("Method method missing parameter args", error_message)

    def test_override_checker_with_complex_signature_mismatch(self):
        with self.assertRaises(AssertionError) as cm:
            class Interface:
                def complex_method(self, a, b=10, *args, c=20, **kwargs):
                    pass

            class Implementation(Interface):
                @overrides
                def complex_method(self, a, b=10, *args, **kwargs):  # Missing c parameter
                    pass

            impl = Implementation()
        
        error_message = str(cm.exception)
        self.assertIn("Method complex_method missing parameter c", error_message)


if __name__ == '__main__':
    unittest.main()