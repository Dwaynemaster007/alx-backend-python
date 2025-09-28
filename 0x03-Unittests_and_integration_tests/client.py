#!/usr/bin/env python3
import unittest
from typing import Dict
from unittest.mock import patch, PropertyMock as pm
from client import GithubOrgClient
from parameterized import parameterized


<<<<<<< HEAD
class GithubOrgClient:
    """A Githib org client
    """
    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name: str) -> None:
        """Init method of GithubOrgClient"""
        self._org_name = org_name

    @memoize
    def org(self) -> Dict:
        """Memoize org"""
        return get_json(self.ORG_URL.format(org=self._org_name))

    @property
    def _public_repos_url(self) -> str:
        """Public repos URL"""
        return self.org["repos_url"]

    @memoize
    def repos_payload(self) -> Dict:
        """Memoize repos payload"""
        return get_json(self._public_repos_url)

    def public_repos(self, license: str = None) -> List[str]:
        """Public repos"""
        json_payload = self.repos_payload
        public_repos = [
            repo["name"] for repo in json_payload
            if license is None or self.has_license(repo, license)
        ]

        return public_repos

    @staticmethod
    def has_license(repo: Dict[str, Dict], license_key: str) -> bool:
        """Static: has_license"""
        assert license_key is not None, "license_key cannot be None"
        try:
            has_license = access_nested_map(repo, ("license", "key")) == license_key
        except KeyError:
            return False
        return has_license
=======
class TestGithubOrgClient(unittest.TestCase):
    """Tests for Github client orgs"""
    @parameterized.expand([
        ('google', {'payload': True}),
        ('abc', {'payload': False}),
    ])
    @patch('client.get_json')
    def test_org(self, name, response, get_json):
        """Test cases"""
        get_json.return_value = response
        client = GithubOrgClient(name)

        json = client.org

        get_json.assert_called_once_with(client.ORG_URL.format(org=name))
        self.assertEqual(json, response)

    @parameterized.expand([
        ('google',),
        ('abc',),
    ])
    def test_public_repos_url(self, name):
        """Tests"""
        github_client = GithubOrgClient(name)
        with patch('client.GithubOrgClient.org', new_callable=pm) as mocked:
            mocked.return_value = {'repos_url': 'some public repos'}
            _repos = github_client._public_repos_url

        self.assertEqual(_repos, 'some public repos')

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "", False)
    ])
    def test_has_license(self, repo, _license, _bool):
        """Test case for has_license method"""
        self.assertIsNotNone(_license)
        self.assertIsInstance(repo, Dict)
        self.assertIs(GithubOrgClient.has_license(repo, _license), _bool)
>>>>>>> bf9ad1c350160b44a7a1221330ed717f0bcff4cb
