#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from unittest.mock import patch
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value"""
        # Setup mock return value
        mock_get_json.return_value = {"fake": "data"}

        # Instantiate GithubOrgClient
        client = GithubOrgClient(org_name)

        # Call the org property
        result = client.org

        # Assert get_json was called once with the expected URL
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

        # Assert org returns the mock value
        self.assertEqual(result, mock_get_json.return_value)
