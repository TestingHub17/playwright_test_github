import os


class Header:

    _default_header = headers={
            "accept": "application/vnd.github+json",
            "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
            "X-GitHub-Api-Version": "2026-03-10"
        }

    def __new__(cls):
        return cls._default_header.copy()

    @classmethod
    def add(cls, **kwargs):
        h = cls._default_header.copy()
        h.update(kwargs)
        return h

    @classmethod
    def remove(cls, *keys):
        h = cls._default_header.copy()
        for key in keys:
            h.pop(key, None)
        return h