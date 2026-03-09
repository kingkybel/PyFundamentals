#!/bin/env python3
# Repository:   https://github.com/PyFundamentals
# File Name:    test/test_thread_with_return_extended.py
# Description:  extended tests for thread with return to improve coverage
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
import time
import threading
from concurrent.futures import ThreadPoolExecutor

from fundamentals.thread_with_return import ReturningThread


class ExtendedThreadWithReturnTests(unittest.TestCase):

    def test_returning_thread_with_exception(self):
        def func_with_exception():
            raise ValueError("Test exception")

        t = ReturningThread(target=func_with_exception)
        t.start()
        result = t.join()
        # The thread should capture the exception and return it
        self.assertIsInstance(result, ValueError)
        self.assertEqual(str(result), "Test exception")

    def test_returning_thread_with_complex_function(self):
        def complex_func(x, y=10, *args, **kwargs):
            time.sleep(0.1)  # Simulate some work
            result = x + y + sum(args) + sum(kwargs.values())
            return result

        t = ReturningThread(target=complex_func, args=(5,), kwargs={'y': 20, 'extra': 5})
        t.start()
        result = t.join()
        self.assertEqual(result, 30)  # 5 + 20 + 5

    def test_returning_thread_with_multiple_args(self):
        def multi_arg_func(a, b, c, d, e):
            return a * b * c * d * e

        t = ReturningThread(target=multi_arg_func, args=(1, 2, 3, 4, 5))
        t.start()
        result = t.join()
        self.assertEqual(result, 120)

    def test_returning_thread_with_keyword_args(self):
        def keyword_func(name, age, city="Unknown"):
            return f"{name} is {age} years old and lives in {city}"

        t = ReturningThread(target=keyword_func, kwargs={'name': 'Alice', 'age': 30, 'city': 'New York'})
        t.start()
        result = t.join()
        self.assertEqual(result, "Alice is 30 years old and lives in New York")

    def test_returning_thread_with_none_return(self):
        def none_func():
            return None

        t = ReturningThread(target=none_func)
        t.start()
        result = t.join()
        self.assertIsNone(result)

    def test_returning_thread_with_list_return(self):
        def list_func():
            return [1, 2, 3, 4, 5]

        t = ReturningThread(target=list_func)
        t.start()
        result = t.join()
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_returning_thread_with_dict_return(self):
        def dict_func():
            return {'a': 1, 'b': 2, 'c': 3}

        t = ReturningThread(target=dict_func)
        t.start()
        result = t.join()
        self.assertEqual(result, {'a': 1, 'b': 2, 'c': 3})

    def test_returning_thread_with_string_return(self):
        def string_func():
            return "Hello, World!"

        t = ReturningThread(target=string_func)
        t.start()
        result = t.join()
        self.assertEqual(result, "Hello, World!")

    def test_returning_thread_with_boolean_return(self):
        def bool_func():
            return True

        t = ReturningThread(target=bool_func)
        t.start()
        result = t.join()
        self.assertTrue(result)

    def test_returning_thread_with_float_return(self):
        def float_func():
            return 3.14159

        t = ReturningThread(target=float_func)
        t.start()
        result = t.join()
        self.assertEqual(result, 3.14159)

    def test_returning_thread_with_large_return_value(self):
        def large_func():
            return list(range(10000))

        t = ReturningThread(target=large_func)
        t.start()
        result = t.join()
        self.assertEqual(len(result), 10000)
        self.assertEqual(result[0], 0)
        self.assertEqual(result[-1], 9999)

    def test_returning_thread_timing(self):
        def timing_func():
            time.sleep(0.5)
            return "done"

        start_time = time.time()
        t = ReturningThread(target=timing_func)
        t.start()
        result = t.join()
        end_time = time.time()
        
        self.assertEqual(result, "done")
        self.assertGreaterEqual(end_time - start_time, 0.5)

    def test_returning_thread_multiple_threads(self):
        def worker(n):
            time.sleep(0.1)
            return n * 2

        threads = []
        for i in range(5):
            t = ReturningThread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        results = []
        for t in threads:
            results.append(t.join())

        self.assertEqual(results, [0, 2, 4, 6, 8])

    def test_returning_thread_with_daemon(self):
        def daemon_func():
            time.sleep(0.1)
            return "daemon result"

        t = ReturningThread(target=daemon_func, daemon=True)
        t.start()
        result = t.join()
        self.assertEqual(result, "daemon result")

    def test_returning_thread_with_group(self):
        def group_func():
            return "group result"

        t = ReturningThread(group=None, target=group_func)
        t.start()
        result = t.join()
        self.assertEqual(result, "group result")

    def test_returning_thread_with_name(self):
        def named_func():
            return "named result"

        t = ReturningThread(name="TestThread", target=named_func)
        t.start()
        result = t.join()
        self.assertEqual(result, "named result")
        self.assertEqual(t.name, "TestThread")

    def test_returning_thread_with_args_and_kwargs(self):
        def mixed_func(a, b, c=10, d=20):
            return a + b + c + d

        t = ReturningThread(target=mixed_func, args=(1, 2), kwargs={'c': 30})
        t.start()
        result = t.join()
        self.assertEqual(result, 53)  # 1 + 2 + 30 + 20

    def test_returning_thread_with_lambda(self):
        t = ReturningThread(target=lambda x: x * 2, args=(5,))
        t.start()
        result = t.join()
        self.assertEqual(result, 10)

    def test_returning_thread_with_method(self):
        class TestClass:
            def method(self, x):
                return x * 3

        obj = TestClass()
        t = ReturningThread(target=obj.method, args=(4,))
        t.start()
        result = t.join()
        self.assertEqual(result, 12)

    def test_returning_thread_with_class_method(self):
        class TestClass:
            @classmethod
            def class_method(cls, x):
                return x * 4

        t = ReturningThread(target=TestClass.class_method, args=(5,))
        t.start()
        result = t.join()
        self.assertEqual(result, 20)

    def test_returning_thread_with_static_method(self):
        class TestClass:
            @staticmethod
            def static_method(x):
                return x * 5

        t = ReturningThread(target=TestClass.static_method, args=(6,))
        t.start()
        result = t.join()
        self.assertEqual(result, 30)

    def test_returning_thread_with_generator(self):
        def generator_func():
            yield 1
            yield 2
            yield 3

        t = ReturningThread(target=generator_func)
        t.start()
        result = t.join()
        # Generators return generator objects
        self.assertTrue(hasattr(result, '__iter__'))
        self.assertTrue(hasattr(result, '__next__'))

    def test_returning_thread_with_recursive_function(self):
        def factorial(n):
            if n <= 1:
                return 1
            return n * factorial(n - 1)

        t = ReturningThread(target=factorial, args=(5,))
        t.start()
        result = t.join()
        self.assertEqual(result, 120)

    def test_returning_thread_with_exception_in_thread(self):
        def exception_func():
            time.sleep(0.1)
            raise RuntimeError("Thread exception")

        t = ReturningThread(target=exception_func)
        t.start()
        result = t.join()
        self.assertIsInstance(result, RuntimeError)
        self.assertEqual(str(result), "Thread exception")

    def test_returning_thread_with_multiple_exceptions(self):
        def exception_func1():
            raise ValueError("First exception")

        def exception_func2():
            raise TypeError("Second exception")

        t1 = ReturningThread(target=exception_func1)
        t2 = ReturningThread(target=exception_func2)
        
        t1.start()
        t2.start()
        
        result1 = t1.join()
        result2 = t2.join()
        
        self.assertIsInstance(result1, ValueError)
        self.assertIsInstance(result2, TypeError)
        self.assertEqual(str(result1), "First exception")
        self.assertEqual(str(result2), "Second exception")

    def test_returning_thread_with_timeout(self):
        def slow_func():
            time.sleep(1)
            return "slow result"

        t = ReturningThread(target=slow_func)
        t.start()
        result = t.join(timeout=0.5)  # Shorter than function execution time
        # Should return None if timeout occurs before completion
        self.assertIsNone(result)
        
        # Wait for thread to complete
        result = t.join()
        self.assertEqual(result, "slow result")

    def test_returning_thread_with_concurrent_futures(self):
        def worker(n):
            time.sleep(0.1)
            return n * n

        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = []
            for i in range(5):
                t = ReturningThread(target=worker, args=(i,))
                futures.append(executor.submit(t.run))
            
            results = [future.result() for future in futures]
        
        self.assertEqual(results, [0, 1, 4, 9, 16])

    def test_returning_thread_with_shared_state(self):
        shared_data = []

        def shared_func(data, value):
            data.append(value)
            return len(data)

        t = ReturningThread(target=shared_func, args=(shared_data, 42))
        t.start()
        result = t.join()
        
        self.assertEqual(result, 1)
        self.assertEqual(shared_data, [42])

    def test_returning_thread_performance(self):
        def quick_func():
            return sum(range(1000))

        start_time = time.time()
        threads = []
        
        for _ in range(100):
            t = ReturningThread(target=quick_func)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
        
        end_time = time.time()
        
        # Should complete 100 threads quickly (less than 1 second)
        self.assertLess(end_time - start_time, 1.0)

    def test_returning_thread_with_nested_threads(self):
        def nested_func():
            def inner_func():
                return "inner"
            
            t = ReturningThread(target=inner_func)
            t.start()
            return t.join()

        t = ReturningThread(target=nested_func)
        t.start()
        result = t.join()
        self.assertEqual(result, "inner")

    def test_returning_thread_with_thread_local_data(self):
        import threading
        
        thread_local = threading.local()

        def thread_func(value):
            thread_local.data = value
            return thread_local.data

        t = ReturningThread(target=thread_func, args=(123,))
        t.start()
        result = t.join()
        self.assertEqual(result, 123)

    def test_returning_thread_with_context_manager(self):
        class ContextManager:
            def __enter__(self):
                return "entered"
            
            def __exit__(self, *args):
                return False

        def context_func():
            with ContextManager() as cm:
                return cm

        t = ReturningThread(target=context_func)
        t.start()
        result = t.join()
        self.assertEqual(result, "entered")

    def test_returning_thread_with_async_function(self):
        import asyncio

        async def async_func():
            await asyncio.sleep(0.1)
            return "async result"

        def sync_wrapper():
            return asyncio.run(async_func())

        t = ReturningThread(target=sync_wrapper)
        t.start()
        result = t.join()
        self.assertEqual(result, "async result")


if __name__ == '__main__':
    unittest.main()