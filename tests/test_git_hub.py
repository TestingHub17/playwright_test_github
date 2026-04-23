import logging
from time import sleep

from playwright.sync_api import Page, expect

from core.header_handle import Header
from pages.issues_page import IssuesPage
from pages.new_issue_create_page import NewIssueCreatePage

logger = logging.getLogger(__name__)

def test_should_create_bug(api_context, get_github_user, get_github_repo):
    data = {
        "title": "[Bug] report 1",
        "body": "Bug description",
    }
    new_issue = api_context().post(f"/repos/{get_github_user}/{get_github_repo}/issues", data=data)
    assert new_issue.ok

    issues = api_context().get(f"/repos/{get_github_user}/{get_github_repo}/issues")
    assert issues.ok
    issue_json = issues.json()
    issues = list(filter(lambda issue:issue['title'] == data['title'], issue_json))[0]
    assert issues['body'] == data['body']

def test_last_create_issue_should_be_first(api_context, get_github_user, get_github_repo, page:Page):
    def create_issue(title:str):
        data = {
            "title": title,
            "body": "Bug description",
        }
        new_issue = api_context().post(f"/repos/{get_github_user}/{get_github_repo}/issues", data=data)
        assert new_issue.ok

    create_issue("[Feature] report 1")
    create_issue("[Feature] report 2")
    page.goto(f"https://github.com/{get_github_user}/{get_github_repo}/issues", wait_until='load')
    expect(page.locator("//*[text()='Open']/following-sibling::span[1]")).not_to_have_text("", timeout=10000)
    sleep(20)
    issue_text = page.locator('[data-hovercard-type="issue"]').first
    assert issue_text.text_content() == "[Feature] report 2"

def test_without_authorization_token(api_context, get_github_repo, get_github_user):
    data = {
        "title": "[New Bug] report 1",
        "body": "Bug description",
    }
    response = api_context(headers=Header.remove("Authorization")).fetch(
        f"/repos/{get_github_user}/{get_github_repo}/issues",
        method="POST",
        data=data
    )
    assert response.status == 401

def test_select_bugs_and_check_verify_actions(page, get_github_repo, get_github_user):
    issue_page = IssuesPage(page)
    new_issue_page = NewIssueCreatePage(page)
    page.goto(f"https://github.com/{get_github_user}/{get_github_repo}/issues")
    expect(page.locator("//*[text()='Open']/following-sibling::span[1]")).not_to_have_text("", timeout=10000)
    timezone = page.evaluate("Intl.DateTimeFormat().resolvedOptions().timeZone")
    logger.info(f"{timezone} timezone of git")

    # check bug list is present
    expect(issue_page.get_issues_checkbox_locator(0)).to_be_visible()
    issue_page.click_issues_check_box(0)

    # verify checkbox is selected
    expect(issue_page.get_issues_checkbox_locator(0)).to_be_checked()

    # verify different filter option is available
    expect(issue_page.get_set_milestone_button()).to_be_visible()
    expect(issue_page.get_add_to_project_button()).to_be_visible()
    expect(issue_page.get_set_assignees_button()).to_be_visible()
    expect(issue_page.get_set_labels_button()).to_be_visible()
    expect(issue_page.get_mark_as_button()).to_be_visible()

    # click on filter option and verify the popup is visible
    issue_page.click_set_milestone_button()
    expect(issue_page.get_milestone_dropdown_search()).to_be_visible()
    issue_page.click_set_milestone_button()

    issue_page.click_add_to_project_button()
    expect(issue_page.get_project_dropdown_search()).to_be_visible()
    issue_page.click_add_to_project_button()

    issue_page.click_mark_as_button()
    expect(issue_page.get_mark_as_options()).to_have_count(3)
    issue_page.click_mark_as_button()

    expect(issue_page.get_issue_search_input()).to_have_value("is:issue state:open ")
    expect(page.get_by_test_id("created-at").locator('[data-hovercard-type="user"]',
                                                     has_text=get_github_user).first).to_be_visible()

    expect(issue_page.get_new_issue_button()).to_be_visible()
    issue_page.click_new_issue_button()
    expect(new_issue_page.get_create_issue_title_field()).to_be_visible()

    expect(new_issue_page.get_create_more_text()).to_be_visible()
    expect(new_issue_page.get_create_issue_button()).to_be_visible()
    expect(new_issue_page.get_cancel_button()).to_be_visible()

    new_issue_page.click_cancel_button()
    expect(issue_page.get_issues_checkbox_locator(0)).to_be_visible()
