import os
from datetime import timedelta, datetime
from flask.app import Flask, request
from analyzer import analysis_commits, analysis_category, get_datetime_from_string
from api import AnalyzerApi

app = Flask(__name__)


@app.route('/')
def analyzer_run() -> str:
    # Parse args
    repo = request.args.get('repo')
    branch = request.args.get('branch', default='master')
    since = get_datetime_from_string(request.args.get('since', default=datetime.min))
    until = get_datetime_from_string(request.args.get('until', default=datetime.max))
    repo_urls = AnalyzerApi(repo)
    # Top author
    top_authors = analysis_commits(repo_urls.get_commits(sha=branch, since=since, until=until))
    # Issues
    issues = analysis_category(repo_urls, category='issues', since=since,
                               until=until, within=timedelta(days=14)
                               )
    # Pull requests
    pulls = analysis_category(repo_urls, category='pulls', since=since,
                              until=until, within=timedelta(days=30)
                              )
    # Return
    return f'Top authors repos:\n{top_authors}\n{issues}\n{pulls}'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv('PORT'))  # port 5000 is the default
