#!/usr/bin/env python3
import unittest
from typing import Dict
from unittest.mock import patch, PropertyMock as pm
from client import GithubOrgClient
from parameterized import parameterized


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
