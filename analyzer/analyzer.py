from datetime import datetime, timedelta
from collections import Counter
from typing import List

from api import AnalyzerApi
import conf


def get_datetime_from_string(date: str) -> datetime:
    """
    :param date: Date format: '%Y-%m-%d' or '%Y-%m-%dT%H:%M:%SZ'
    :return: New datetime parsed from a string.
    """
    try:
        return datetime.strptime(date, conf.ISO_FORMAT)
    except ValueError:
        return datetime.strptime(date, conf.ISO_FORMAT_LITE)


def analysis_category(repo: AnalyzerApi, category: str, since: datetime,
                      until: datetime, within: timedelta) -> str:
    """
    Analysis issues or pull requests
    :param repo: AnalyzerApi. Class for analysis repo.
    :param category: Issue or pulls.
    :param since: Start date of analysis.
    :param until: End date of analysis.
    :param within: The period when the category is valid.
    :return: Result analysis issues and pull requests
    """
    since = since or datetime.min
    until = until or datetime.max

    # Type: issue or pulls?
    if category == conf.PULLS:
        category_type = repo.get_pull_requests(state='all')
    else:
        category_type = repo.get_issues(state='all')

    # Opened issues or pull request
    opened = set(filter(
        lambda x: since <= x.created_at < until,
        category_type
    ))
    # Closed issues or pull request
    closed = set(filter(
        lambda x: x.state == 'closed' and since <= x.closed_at < until,
        category_type
    ))
    # Within issues or pull request
    old = set(filter(
        lambda x: since <= x.created_at + within < until and (
                x.state == 'open' or x.closed_at >= until
        ),
        category_type
    ))

    result = (
        f'{len(opened)} opened {category:10}'
        f'{len(closed)} closed {category:10}'
        f'{len(old)} old {category:10}'
    )

    return result


def analysis_commits(commits: List) -> str:
    """
    Analysis commits
    :param commits: List of comment objects
    :return: Result analysis commits
    """
    print(commits)
    top_authors = Counter()
    for commit in commits:
        try:
            author_login = commit.author['login']
            top_authors.setdefault(author_login, 0)
            top_authors[author_login] += 1
        except TypeError:
            pass
        except KeyError:
            print('Key "login" not exist')

    top_authors = [(v, k) for k, v in top_authors.items()]
    top_authors.sort(reverse=True)
    top_authors = top_authors[:30]

    result = str()
    for commit_count, login in top_authors:
        result += f'{login:20}{commit_count:20d}\n'

    return result
