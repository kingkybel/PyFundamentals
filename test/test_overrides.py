#!/bin/env python3
# Repository:   https://github.com/PyFundamentals
# File Name:    test/test_overrides.py
# Description:  test overrides
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
# @date: 2025-10-21
# @author: Dieter J Kybelksties

import unittest

from fundamentals.overrides import OverrideChecker, overrides


class TestOverrideChecker(unittest.TestCase):

    def test_init(self):
        def dummy_method():
            pass

        checker = OverrideChecker(dummy_method)
        self.assertEqual(checker.method, dummy_method)
        self.assertIsNone(checker.interface_class)
        self.assertIsNone(checker.name)
        self.assertIsNone(checker.owner)

    def test_set_name_with_interface_class(self):
        class Interface:
            def method(self, a, b):
                pass

        class Implementation:
            @overrides(Interface)
            def method(self, a, b):
                pass

        impl = Implementation()
        # The descriptor should be set up correctly
        self.assertTrue(hasattr(impl, 'method'))

    def test_set_name_without_interface_class(self):
        class Interface:
            def method(self, a, b):
                pass

        class Implementation(Interface):
            @overrides
            def method(self, a, b):
                pass

        impl = Implementation()
        # The descriptor should be set up correctly
        self.assertTrue(hasattr(impl, 'method'))

    def test_set_name_no_interface_found(self):
        with self.assertRaises(RuntimeError) as cm:
            class Implementation:
                @overrides
                def method(self, a, b):
                    pass

            impl = Implementation()
        # Check that the cause is AssertionError with the expected message
        cause = cm.exception.__cause__
        self.assertIsInstance(cause, AssertionError)
        self.assertIn("No interface class found for method method", str(cause))

    def test_set_name_missing_parameter(self):
        with self.assertRaises(RuntimeError) as cm:
            class Interface:
                def method(self, a, b):
                    pass

            class Implementation(Interface):
                @overrides
                def method(self, a):  # Missing parameter b
                    pass

            impl = Implementation()

    def test_set_name_parameter_kind_mismatch(self):
        with self.assertRaises(RuntimeError) as cm:
            class Interface:
                def method(self, a, *args):
                    pass

            class Implementation(Interface):
                @overrides
                def method(self, a, **kwargs):  # *args vs **kwargs
                    pass

            impl = Implementation()
        # Check that the cause is AssertionError with the expected message
        cause = cm.exception.__cause__
        self.assertIsInstance(cause, AssertionError)
        self.assertIn("Method method missing parameter args", str(cause))

    def test_set_name_var_keyword_missing(self):
        with self.assertRaises(RuntimeError) as cm:
            class Interface:
                def method(self, a, **kwargs):
                    pass

            class Implementation(Interface):
                @overrides
                def method(self, a):  # Missing **kwargs
                    pass

            impl = Implementation()
        # Check that the cause is AssertionError with the expected message
        cause = cm.exception.__cause__
        self.assertIsInstance(cause, AssertionError)
        self.assertIn("Method method must have **kwargs since interface does", str(cause))

    def test_get_instance_method(self):
        class Interface:
            def method(self):
                pass

        class Implementation(Interface):
            @overrides
            def method(self):
                return "instance"

        impl = Implementation()
        result = impl.method()
        self.assertEqual(result, "instance")

    def test_get_class_method(self):
        class Interface:
            def method(self):
                pass

        class Implementation(Interface):
            @overrides
            def method(self):
                return "instance"

        result = Implementation.method
        self.assertTrue(callable(result))

    def test_call_direct(self):
        def dummy_method():
            return "called"

        checker = OverrideChecker(dummy_method)
        result = checker()
        self.assertEqual(result, "called")

    def test_overrides_decorator_with_class(self):
        class Interface:
            def method(self):
                pass

        class Implementation:
            @overrides(Interface)
            def method(self):
                pass

        impl = Implementation()
        self.assertTrue(hasattr(impl, 'method'))

    def test_overrides_decorator_without_parens(self):
        class Interface:
            def method(self):
                pass

        class Implementation(Interface):
            @overrides
            def method(self):
                pass

        impl = Implementation()
        self.assertTrue(hasattr(impl, 'method'))

    def test_overrides_new_with_callable(self):
        def dummy_method():
            pass

        result = overrides(dummy_method)
        self.assertIsInstance(result, OverrideChecker)
        self.assertEqual(result.method, dummy_method)

    def test_overrides_new_with_type(self):
        result = overrides(str)
        self.assertIsInstance(result, overrides)
        self.assertEqual(result.interface_class, str)


if __name__ == "__main__":
    unittest.main()
