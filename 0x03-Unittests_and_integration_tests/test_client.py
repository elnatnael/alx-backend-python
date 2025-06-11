#!/usr/bin/env python3
"""
Integration tests for the GithubOrgClient.public_repos method.
Tests that public_repos returns the expected repository names,
and correctly filters by license when specified.
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized_class
from typing import List, Dict, Any

from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


@parameterized_class(
    [
        {
            "org_payload": org_payload,
            "repos_payload": repos_payload,
            "expected_repos": expected_repos,
            "apache2_repos": apache2_repos
        }
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for GithubOrgClient.public_repos method.

    Uses patched 'get_json' method to simulate API calls.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Start patching 'get_json' before tests.
        """
        cls.get_patcher = patch('client.get_json')
        cls.mock_get_json = cls.get_patcher.start()

        def side_effect(url: str) -> Any:
            """
            Side effect function for mock_get_json to return
            different fixture data based on URL called.
            """
            if url == "https://api.github.com/orgs/google":
                return cls.org_payload
            if url == cls.org_payload["repos_url"]:
                return cls.repos_payload
            return None

        cls.mock_get_json.side_effect = side_effect

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Stop patching 'get_json' after tests.
        """
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """
        Test that public_repos returns the expected list of repository names.
        """
        client = GithubOrgClient("google")
        result: List[str] = client.public_repos()
        self.assertEqual(result, self.expected_repos)

        # Check that get_json was called for org and repos URLs
        self.mock_get_json.assert_any_call("https://api.github.com/orgs/google")
        self.mock_get_json.assert_any_call(self.org_payload["repos_url"])

    def test_public_repos_with_license(self) -> None:
        """
        Test that public_repos returns only repositories with the specified license.
        """
        client = GithubOrgClient("google")
        result: List[str] = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)

        # Check that get_json was called for org and repos URLs
        self.mock_get_json.assert_any_call("https://api.github.com/orgs/google")
        self.mock_get_json.assert_any_call(self.org_payload["repos_url"])


if __name__ == "__main__":
    unittest.main()
