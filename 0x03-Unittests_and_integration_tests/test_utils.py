#!/usr/bin/env python3
"""Unit tests for utils.access_nested_map"""

import unittest
from parameterized import parameterized
from utils import access_nested_map
from typing import Any, Dict, Tuple


class TestAccessNestedMap(unittest.TestCase):
    """Test class for access_nested_map function"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self,
                               nested_map: Dict[str, Any],
                               path: Tuple[str, ...],
                               expected: Any) -> None:
        """Test that access_nested_map returns the correct value"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), 'b'),
    ])
    def test_access_nested_map_exception(self,
                                         nested_map: Dict[str, Any],
                                         path: Tuple[str, ...],
                                         expected_key: str) -> None:
        """Test that access_nested_map raises KeyError with the correct message"""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{expected_key}'")

