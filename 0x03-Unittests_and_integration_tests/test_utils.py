#!/usr/bin/env python3
"""Unit tests for utils module.

This module contains unit tests for the utility functions
in the utils module, specifically testing access_nested_map function.
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test class for access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns expected results for various inputs."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        """Test access_nested_map raises KeyError for invalid paths."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{expected_key}'")


class TestGetJson(unittest.TestCase):
    """Test class for get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test get_json returns expected payload and calls requests.get once."""
        # Configure the mock to return a Mock object with json method
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Call the function
        result = get_json(test_url)

        # Assert the mock was called exactly once with the test_url
        mock_get.assert_called_once_with(test_url)

        # Assert the result equals the test_payload
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test class for memoize decorator."""

    def test_memoize(self):
        """Test that memoize decorator caches results and calls method only once."""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        # Create instance of TestClass
        test_instance = TestClass()

        # Mock the a_method
        with patch.object(test_instance, 'a_method', return_value=42) as \
                mock_method:
            # Call a_property twice
            result1 = test_instance.a_property
            result2 = test_instance.a_property

            # Assert both calls return the correct result
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Assert a_method was called only once due to memoization
            mock_method.assert_called_once()


if __name__ == '__main__':
    unittest.main()
# [Ensure there is one final blank line after this comment or the last line of code]
