from datetime import datetime

import conf


class Commit:
    """
    Git commit.
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class AnalyzerBase:
    """
    Base class
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.created_at = datetime.strptime(self.created_at, conf.ISO_FORMAT)
        self.closed_at = self.closed_at and datetime.strptime(self.closed_at, conf.ISO_FORMAT)


class Pull(AnalyzerBase):
    """
    Pull requests
    """
    pass


class Issue(AnalyzerBase):
    """
    Issues
    """
    pass
