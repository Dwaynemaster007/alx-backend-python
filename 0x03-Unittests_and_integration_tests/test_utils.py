# test_utils.py

#!/usr/bin/env python3
"""Module for testing utils.py
"""
import unittest
from parameterized import parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    """Class to test access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns the expected output."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    def test_access_nested_map_exception(self):
        """Test that access_nested_map raises a KeyError."""
        test_cases = [
            ({}, ("a",), 'a'),
            ({"a": 1}, ("a", "b"), 'b')
        ]
        for nested_map, path, expected_key in test_cases:
            with self.assertRaises(KeyError) as cm:
                access_nested_map(nested_map, path)
            self.assertEqual(str(cm.exception), f"'{expected_key}'")