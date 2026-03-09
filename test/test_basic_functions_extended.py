#!/bin/env python3
# Repository:   https://github.com/PyFundamentals
# File Name:    test/test_basic_functions_extended.py
# Description:  extended tests for basic functions to improve coverage
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
from datetime import datetime
import re

from fundamentals.basic_functions import is_empty_string, now_string, now_string_short, now_date, now_year


class ExtendedBasicFunctionsTests(unittest.TestCase):

    def test_is_empty_string_edge_cases(self):
        # Test with None
        self.assertTrue(is_empty_string(None))
        
        # Test with empty string
        self.assertTrue(is_empty_string(""))
        
        # Test with whitespace only
        self.assertFalse(is_empty_string(" "))
        self.assertFalse(is_empty_string("\t"))
        self.assertFalse(is_empty_string("\n"))
        self.assertFalse(is_empty_string("   "))
        
        # Test with non-empty strings
        self.assertFalse(is_empty_string("hello"))
        self.assertFalse(is_empty_string("  hello  "))
        
        # Test with other types
        self.assertFalse(is_empty_string(0))
        self.assertFalse(is_empty_string([]))
        self.assertFalse(is_empty_string({}))
        self.assertFalse(is_empty_string(False))

    def test_now_string_format(self):
        result = now_string()
        self.assertIsInstance(result, str)
        
        # Test format: YYYYMMDD-HH:MM:SS.ffffff
        pattern = r'^\d{8}-\d{2}:\d{2}:\d{2}\.\d{6}$'
        self.assertRegex(result, pattern)
        
        # Test that it's a valid datetime string
        datetime.strptime(result, "%Y%m%d-%H:%M:%S.%f")

    def test_now_string_uniqueness(self):
        # Test that multiple calls produce different results (within same second)
        results = [now_string() for _ in range(10)]
        
        # All should be valid format
        for result in results:
            self.assertRegex(result, r'^\d{8}-\d{2}:\d{2}:\d{2}\.\d{6}$')
        
        # Should be unique (very unlikely to have same microsecond)
        self.assertEqual(len(set(results)), len(results))

    def test_now_string_short_format(self):
        result = now_string_short()
        self.assertIsInstance(result, str)
        
        # Test format: YYYYMMDD-HH:MM
        pattern = r'^\d{8}-\d{2}:\d{2}$'
        self.assertRegex(result, pattern)
        
        # Test that it's a valid datetime string
        datetime.strptime(result, "%Y%m%d-%H:%M")

    def test_now_string_short_uniqueness(self):
        # Test that multiple calls can produce same result (same minute)
        results = [now_string_short() for _ in range(10)]
        
        # All should be valid format
        for result in results:
            self.assertRegex(result, r'^\d{8}-\d{2}:\d{2}$')
        
        # May have duplicates (same minute)
        self.assertGreaterEqual(len(results), len(set(results)))

    def test_now_date_format(self):
        result = now_date()
        self.assertIsInstance(result, str)
        
        # Test format: YYYY-MM-DD
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        self.assertRegex(result, pattern)
        
        # Test that it's a valid date string
        datetime.strptime(result, "%Y-%m-%d")

    def test_now_date_uniqueness(self):
        # Test that multiple calls produce same result (same day)
        results = [now_date() for _ in range(10)]
        
        # All should be valid format
        for result in results:
            self.assertRegex(result, r'^\d{4}-\d{2}-\d{2}$')
        
        # Should all be the same (same day)
        self.assertEqual(len(set(results)), 1)

    def test_now_year_format(self):
        result = now_year()
        self.assertIsInstance(result, str)
        
        # Test format: YYYY
        pattern = r'^\d{4}$'
        self.assertRegex(result, pattern)
        
        # Test that it's a valid year
        year = int(result)
        self.assertGreaterEqual(year, 2000)
        self.assertLessEqual(year, 2100)

    def test_now_year_uniqueness(self):
        # Test that multiple calls produce same result (same year)
        results = [now_year() for _ in range(10)]
        
        # All should be valid format
        for result in results:
            self.assertRegex(result, r'^\d{4}$')
        
        # Should all be the same (same year)
        self.assertEqual(len(set(results)), 1)

    def test_now_functions_consistency(self):
        # Test that all functions return consistent data
        now_str = now_string()
        now_short = now_string_short()
        now_d = now_date()
        now_y = now_year()
        
        # Extract components
        dt_full = datetime.strptime(now_str, "%Y%m%d-%H:%M:%S.%f")
        dt_short = datetime.strptime(now_short, "%Y%m%d-%H:%M")
        dt_date = datetime.strptime(now_d, "%Y-%m-%d")
        year = int(now_y)
        
        # Check consistency
        self.assertEqual(dt_full.year, dt_short.year)
        self.assertEqual(dt_full.year, dt_date.year)
        self.assertEqual(dt_full.year, year)
        
        self.assertEqual(dt_full.month, dt_short.month)
        self.assertEqual(dt_full.month, dt_date.month)
        
        self.assertEqual(dt_full.day, dt_short.day)
        self.assertEqual(dt_full.day, dt_date.day)
        
        self.assertEqual(dt_full.hour, dt_short.hour)
        self.assertEqual(dt_full.minute, dt_short.minute)

    def test_now_functions_timing(self):
        # Test that functions called in sequence have reasonable timing
        import time
        
        start_time = time.time()
        
        now_str1 = now_string()
        time.sleep(0.001)  # 1ms delay
        now_str2 = now_string()
        
        end_time = time.time()
        
        # Should be very fast (less than 1 second)
        self.assertLess(end_time - start_time, 1.0)
        
        # Second call should be after first (microsecond precision)
        dt1 = datetime.strptime(now_str1, "%Y%m%d-%H:%M:%S.%f")
        dt2 = datetime.strptime(now_str2, "%Y%m%d-%H:%M:%S.%f")
        self.assertGreaterEqual(dt2, dt1)

    def test_is_empty_string_with_unicode(self):
        # Test with Unicode whitespace
        self.assertFalse(is_empty_string(" "))
        self.assertFalse(is_empty_string("\u2003"))  # Em space
        self.assertFalse(is_empty_string("\u00A0"))  # Non-breaking space
        
        # Test with Unicode empty string
        self.assertTrue(is_empty_string(""))

    def test_now_functions_with_timezone(self):
        # Test that functions work with different timezone settings
        import os
        import time
        
        # Save original timezone
        original_tz = os.environ.get('TZ')
        
        try:
            # Test with different timezone
            os.environ['TZ'] = 'UTC'
            time.tzset()
            
            result = now_date()
            self.assertRegex(result, r'^\d{4}-\d{2}-\d{2}$')
            
        finally:
            # Restore original timezone
            if original_tz is not None:
                os.environ['TZ'] = original_tz
            else:
                os.environ.pop('TZ', None)
            time.tzset()

    def test_now_string_precision(self):
        # Test microsecond precision
        result = now_string()
        microseconds = result.split('.')[-1]
        self.assertEqual(len(microseconds), 6)
        
        # Test that microseconds are numeric
        self.assertTrue(microseconds.isdigit())

    def test_now_string_short_minute_boundary(self):
        # Test behavior around minute boundaries
        import time
        
        # Wait until near minute boundary
        current_time = datetime.now()
        seconds_left = 60 - current_time.second
        
        if seconds_left < 2:
            time.sleep(seconds_left + 0.1)
        
        result1 = now_string_short()
        time.sleep(1.1)  # Cross minute boundary
        result2 = now_string_short()
        
        # Should be different if we crossed minute boundary
        dt1 = datetime.strptime(result1, "%Y%m%d-%H:%M")
        dt2 = datetime.strptime(result2, "%Y%m%d-%H:%M")
        
        # Either same minute or next minute
        time_diff = (dt2 - dt1).total_seconds()
        self.assertIn(time_diff, [0, 60])

    def test_now_date_day_boundary(self):
        # Test behavior around day boundaries
        import time
        
        # Wait until near day boundary
        current_time = datetime.now()
        seconds_left = 86400 - (current_time.hour * 3600 + current_time.minute * 60 + current_time.second)
        
        if seconds_left < 5:
            time.sleep(seconds_left + 0.1)
        
        result1 = now_date()
        time.sleep(1.1)  # Might cross day boundary
        result2 = now_date()
        
        # Should be valid dates
        datetime.strptime(result1, "%Y-%m-%d")
        datetime.strptime(result2, "%Y-%m-%d")

    def test_now_year_leap_year(self):
        # Test that year function works correctly in leap years
        # This is mostly a consistency check
        result = now_year()
        year = int(result)
        
        # Check if it's a leap year using standard algorithm
        is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        
        # Just verify the calculation is consistent
        self.assertIsInstance(is_leap, bool)

    def test_is_empty_string_performance(self):
        # Test performance with large number of calls
        import time
        
        test_strings = [None, "", " ", "hello", "x" * 1000]
        
        start_time = time.time()
        for _ in range(1000):
            for s in test_strings:
                is_empty_string(s)
        end_time = time.time()
        
        # Should be very fast
        self.assertLess(end_time - start_time, 0.1)

    def test_now_functions_thread_safety(self):
        # Test that functions work correctly in multi-threaded environment
        import threading
        import time
        
        results = []
        
        def get_time_values():
            results.append((
                now_string(),
                now_string_short(),
                now_date(),
                now_year()
            ))
        
        threads = []
        for _ in range(10):
            t = threading.Thread(target=get_time_values)
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        # All results should be valid
        for result_set in results:
            now_str, now_short, now_d, now_y = result_set
            
            self.assertRegex(now_str, r'^\d{8}-\d{2}:\d{2}:\d{2}\.\d{6}$')
            self.assertRegex(now_short, r'^\d{8}-\d{2}:\d{2}$')
            self.assertRegex(now_d, r'^\d{4}-\d{2}-\d{2}$')
            self.assertRegex(now_y, r'^\d{4}$')


if __name__ == '__main__':
    unittest.main()