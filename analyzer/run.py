from argparse import ArgumentParser
from datetime import timedelta

from analyzer import analysis_commits, analysis_category, get_datetime_from_string
from api import AnalyzerApi


def parse_args():
    """
    Parse argument of command line
    :return: object: Parsed args
    """
    parser = ArgumentParser(description='Program for analysis GitHub repository.')
    parser.add_argument('url', help='URL repository')
    parser.add_argument('-b', '--branch', default='master', help='Branch for analysis.')
    parser.add_argument('-s', '--since', default=None, type=get_datetime_from_string, help='Start date of analysis.')
    parser.add_argument('-u', '--until', default=None, type=get_datetime_from_string, help='End date of analysis.')
    return parser.parse_args()


def run():
    """ Run function """
    print('Running...')
    args = parse_args()
    repo_urls = AnalyzerApi(args.url)

    # Top author
    top_authors = analysis_commits(repo_urls.get_commits(sha=args.branch, since=args.since, until=args.until))

    # Issues
    issues = analysis_category(repo_urls, category='issues', since=args.since,
                               until=args.until, within=timedelta(days=14)
                               )
    # Pull requests
    pulls = analysis_category(repo_urls,
                              category='pulls', since=args.since,
                              until=args.until, within=timedelta(days=30)
                              )
    # Print stdout
    print(f'Top authors repos:\n{top_authors}\n{issues}\n{pulls}')
    print('Complete')


if __name__ == '__main__':
    run()
