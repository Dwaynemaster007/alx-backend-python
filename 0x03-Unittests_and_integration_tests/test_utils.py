#!/usr/bin/env python3
<<<<<<< HEAD
"""Unit tests for utils module.

This module contains unit tests for the utility functions
in the utils module, specifically testing access_nested_map function.
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Test class for access_nested_map function."""
=======
"""Parameterize a unit test"""
import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized, parameterized_class
from utils import (
    access_nested_map,
    memoize,
    get_json,
)


class TestAccessNestedMap(unittest.TestCase):
    """unit test for utils.access_nested_map"""
    @parameterized.expand([
        ({'a': 1}, ('a',), 1),
        ({'a': {'b': 2}}, ('a',), {'b': 2}),
        ({'a': {'b': 2}}, ('a', 'b'), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected_return):
        "Tests for access_nested_map function"
        self.assertEqual(access_nested_map(nested_map, path), expected_return)
>>>>>>> bf9ad1c350160b44a7a1221330ed717f0bcff4cb

    @parameterized.expand([
        ({}, ('a',), KeyError)
    ])
<<<<<<< HEAD
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns expected results for various inputs."""
        self.assertEqual(access_nested_map(nested_map, path), expected)


if __name__ == '__main__':
    unittest.main()
=======
    def test_access_nested_map_exception(self, nested_map, path, exception):
        """Tests for exception raised"""
        with self.assertRaises(exception):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Mocks HTTP calls"""
    @parameterized.expand([
        ('http://example.com', {"payload": True}),
        ('http://holberton.io', {"payload": False})
    ])
    def test_get_json(self, test_uri, params):
        """Test for get_json function"""
        with patch('utils.requests.get') as mocked:
            mock = Mock()
            mock.json.return_value = params
            mocked.return_value = mock

            response = utils.get_json(test_uri)
        mocked.assert_called_once_with(test_uri)
        self.assertEqual(response, params)


class TestMemoize(unittest.TestCase):
    """Tests for memoized method"""
    def test_memoize(self):
        """Test for memoized property"""
        class TestClass:
            """Test class"""
            def a_method(self):
                """a_method"""
                return 42

            @memoize
            def a_property(self):
                """memoized property"""
                return self.a_method()

        test_object = TestClass()

        with patch.object(test_object, 'a_method') as mocked_a:
            mock = Mock()
            mock.a_method.return_value = 42
            mocked_a.return_value = mock

            ret_value = test_object.a_property
            returned = test_object.a_property
        mocked_a.assert_called_once()
>>>>>>> bf9ad1c350160b44a7a1221330ed717f0bcff4cb
