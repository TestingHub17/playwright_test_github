from playwright.sync_api import Playwright

from core.header_handle import Header


class APIClient:
    def __init__(self, playwright:Playwright, base_url: str, headers=None):
        self._context = playwright.request.new_context(base_url=base_url,
                                                     extra_http_headers=headers or Header())

    def close(self):
        self._context.dispose()

    def get(self, url, **kwargs):
        return self._context.get(url, **kwargs)

    def post(self, url, **kwargs):
        return self._context.post(url, **kwargs)

    def put(self, url, **kwargs):
        return self._context.put(url, **kwargs)

    def delete(self, url, **kwargs):
        return self._context.delete(url, **kwargs)

    def fetch(self, url, **kwargs):
        return self._context.fetch(url, **kwargs)