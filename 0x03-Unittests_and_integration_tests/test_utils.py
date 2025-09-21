#!/usr/bin/env python3
"""Module for testing utils.py
"""
import unittest
from parameterized import parameterized
from .utils import access_nested_map # Use relative import to fix ModuleNotFoundError

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

    @parameterized.expand([ # Add the decorator here
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that access_nested_map raises a KeyError."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), f"'{path[-1]}'")