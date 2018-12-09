import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from typing import List


from model import Issue, Pull, Commit
import conf


class AnalyzerApi:
    """
    Repository API bindings.
    :git_url: string. URL of Github.
    :api_url: string. URL of Github API.
    """
    git_url = 'github.com/'
    api_url = 'https://api.github.com'

    def __init__(self, url=None, owner=None, name=None):
        """
        Init AnalysisRepo object.
        :param url: Full or short URL of Github repo. Format urls: https://github.com/owner/name or owner/name
        :param owner: Repo owner.
        :param name: Repo name.
        :raise TypeError: If not enough args given.
        """
        if not (self.git_url or (owner and name)):
            raise TypeError('Needs url or owner and name')

        if self.git_url in url:
            _, url = url.split(self.git_url)

        path = url.split('/')

        # if len(path) < 2:
        #     raise ValueError('Invalid repository name')
        if not all([owner, name]):
            try:
                owner, name = path
            except ValueError:
                print('Invalid repository name')
                exit()

        self.path = f'/repos/{owner}/{name}/'

    @staticmethod
    def get_token() -> str:
        """
        Read the file to get the token.
        :return: Token authenticate github for higher rate limit.
        """
        env_file = Path('.env')
        if env_file.is_file():
            with open(env_file) as f:
                token = f.read().rstrip()
            return f'token {token}'

    def get_url(self, path: str, **kwargs) -> str:
        """
        :param path: Path to resource to get.
        :param kwargs: URL parameters.
        :return: Formed url from parameters.
        """
        parameters = urlencode([*filter(lambda x: x[1], kwargs.items())])
        return f'{self.api_url}{path}?' + parameters

    def get_data(self, path: str) -> List:
        """
        Get response to request sent to given URL path.
        :param path: Path to resource to get.
        :return: All results from one page.
        """
        request = Request(path)
        token = self.get_token()

        if token:
            request.add_header("Authorization", token)

        try:
            response = urlopen(request)
            return json.loads(response.read())
        except HTTPError:
            print('Not found repo or branch')
            exit()
        except URLError:
            print('Check that you have a consistent internet connection')
            exit()
        except Exception as e:
            print(e)

    def get_result(self, path: str, **kwargs) -> List:
        """
        Get all items from paginated response.
        :param path: Path to resource to get.
        :param kwargs: URL parameters.
        :return: All results from all pages.
        """
        result = list()
        page = 1

        while True:
            kwargs['page'] = page
            url = self.get_url(path, **kwargs)
            response = self.get_data(url)

            if not response:
                return result
            result += response
            page += 1

    def get_commits(self, sha=None, since=None, until=None) -> List:
        """
        :param sha: Commit or target branch name.
        :param since: Start date of analysis.
        :param until: End date of analysis.
        :return: Commits.
        """
        return [Commit(**d) for d in self.get_result(self.path + conf.COMMITS, sha=sha, since=since, until=until)]

    def get_issues(self, state='open') -> List:
        """
        :param state: Issue state: 'open', 'closed', 'all'.
        :return: Issues.
        """
        return [Issue(**d) for d in self.get_result(self.path + conf.ISSUES, state=state)]

    def get_pull_requests(self, state='open') -> List:
        """
        :param state: Pull Requests state: 'open', 'closed', 'all'.
        :return: Pull requests.
        """
        return [Pull(**d) for d in self.get_result(self.path + conf.PULLS, state=state)]
