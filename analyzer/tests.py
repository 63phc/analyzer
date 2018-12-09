import unittest
# from .api import Commit
from ap.analyzer.analyzer import analysis_commits


class TestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)

    # def test_test(self, repo_urls=None):
    #     self.assertEqual(self.get_repo_url('google/material-design-icons'),
    #                      "https://api.github.com/repos/google/material-design-icons")
    #     analysis_commits(repo_urls.get_commits(sha=args.branch, since=args.since, until=args.until))
#
