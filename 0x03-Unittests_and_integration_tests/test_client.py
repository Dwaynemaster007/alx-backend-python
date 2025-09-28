#!/usr/bin/env python3
"""Unit tests for client module.

This module contains unit tests for the GithubOrgClient class
in the client module, testing org, public_repos_url, public_repos, and has_license.
"""
import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient class."""

    @parameterized.expand([
        ("google", {"payload": True}),
        ("abc", {"payload": False}),
    ])
    @patch('utils.get_json')
    def test_org(self, org_name, expected_response, mock_get):
        """Test GithubOrgClient.org returns correct value."""
        mock_get.return_value = expected_response
        client = GithubOrgClient(org_name)
        result = client.org
        self.assertEqual(result, expected_response)
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get.assert_called_once_with(expected_url)

    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url returns correct URL."""
        test_payload = {"repos_url": "http://example.com/repos"}
        with patch('client.GithubOrgClient.org', new=PropertyMock) as mock_org:
            mock_org.return_value = test_payload
            client = GithubOrgClient("test_org")
            result = client._public_repos_url
            self.assertEqual(result, test_payload["repos_url"])
            mock_org.assert_called_once()

    @patch('utils.get_json')
    def test_public_repos(self, mock_get):
        """Test GithubOrgClient.public_repos returns correct repo names."""
        test_repos = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]
        test_url = "http://example.com/repos"
        mock_get.return_value = test_repos
        with patch('client.GithubOrgClient._public_repos_url',
                   new=PropertyMock) as mock_url:
            mock_url.return_value = test_url
            client = GithubOrgClient("test_org")
            result = client.public_repos()
            self.assertEqual(result, ["repo1", "repo2"])
            mock_url.assert_called_once()
            mock_get.assert_called_once_with(test_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license returns correct boolean."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Set up class by mocking requests.get with fixture payloads."""
        def side_effect(url):
            if url == GithubOrgClient.ORG_URL.format(cls.org_payload["name"]):
                return Mock(**{"json.return_value": cls.org_payload})
            if url == cls.org_payload["repos_url"]:
                return Mock(**{"json.return_value": cls.repos_payload})
            raise ValueError(f"Unexpected URL: {url}")

        cls.get_patcher = patch('requests.get', side_effect=side_effect)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repos from fixtures."""
        client = GithubOrgClient(self.org_payload["name"])
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos with apache-2.0 license returns expected repos."""
        client = GithubOrgClient(self.org_payload["name"])
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)


if __name__ == '__main__':
    unittest.main()