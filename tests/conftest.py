import os

import pytest
from playwright.sync_api import Browser, Playwright, expect

from common.config_handler import Config
from core.endpoint import APIClient
from pages.login_page import LoginPage

config = Config().get()

@pytest.fixture(scope="session")
def api_context(base_url, playwright:Playwright) :
    clients = []
    def _api(headers=None):
        client = APIClient(playwright, base_url=base_url, headers=headers)
        clients.append(client)
        return client
    yield _api
    for cl in clients:
        cl.close()


# @pytest.fixture(scope="session")
# def browser_context(api_context, browser:Browser):
#     api_context()._context.storage_state('storage_state.json')
#     browser_context = browser.new_context(storage_state='storage_state.json')
#     yield browser_context
#     browser_context.close()

@pytest.fixture(scope="session")
def browser_context(browser:Browser, get_github_user, get_github_password):

    # create fresh context
    context = browser.new_context()
    page = context.new_page()

    login_page = LoginPage(page)
    login_page.navigate_to_login_page()

    expect(login_page.get_username_field()).to_be_visible()

    login_page.enter_username(get_github_user)
    login_page.enter_password(get_github_password)
    login_page.click_sign_in()

    # optional: wait for successful login indicator
    page.wait_for_url("https://github.com/")

    yield context

    context.close()

@pytest.fixture(scope="session")
def browser_with_storage_state(browser:Browser, browser_context):
    storage = browser_context.storage_state()
    yield browser_context

@pytest.fixture(scope="session")
def page(browser:Browser):
    browser_page = browser.new_context(storage_state="auth.json").new_page()
    yield  browser_page
    browser_page.close()

@pytest.fixture(scope="session")
def get_github_user():
    github_user = os.getenv('GITHUB_USER')
    if github_user is None:
        return config['staging']['github_user']
    else:
        return github_user

@pytest.fixture(scope="session")
def get_github_repo():
    github_repo = os.getenv('GITHUB_REPO')
    if github_repo is None:
        return config['staging']['github_repo']
    else:
        return github_repo

@pytest.fixture(scope="session")
def get_github_password():
    github_password = os.getenv('GITHUB_PASSWORD')
    if github_password is None:
        return config['staging']['github_password']
    else:
        return github_password

@pytest.fixture(scope="session")
def base_url():
    return config['staging']['base_url']