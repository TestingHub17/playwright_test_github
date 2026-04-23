import logging

from playwright.sync_api import Page

logger = logging.getLogger(__name__)


class IssuesPage:
    def __init__(self, page:Page):
        self.page = page
        self.issues_page_url = ""

    issues_check_box = '//*[@data-listview-component="items-list"]//*[contains(@class, "Selection-module__container")]/input'

    def navigate_to_issues_page(self):
        self.page.goto(self.issues_page_url)

    def get_issues_checkbox_locator(self, index):
        return self.page.locator(f'{self.issues_check_box}').nth(index)

    def click_issues_check_box(self, index):
        checkbox_locator = self.get_issues_checkbox_locator(index)
        checkbox_locator.click()

    def get_set_milestone_button(self):
        return self.page.get_by_test_id("bulk-set-milestone-button")

    def click_set_milestone_button(self):
        set_milestone_button = self.get_set_milestone_button()
        set_milestone_button.click()

    def get_milestone_dropdown_search(self):
        return self.page.get_by_placeholder("Filter milestones")

    def get_add_to_project_button(self):
        return self.page.get_by_test_id("bulk-add-to-project-button")

    def click_add_to_project_button(self):
        add_to_project_button = self.get_add_to_project_button()
        add_to_project_button.click()

    def get_project_dropdown_search(self):
        return self.page.get_by_placeholder("Filter projects")

    def get_set_assignees_button(self):
        return self.page.get_by_test_id("bulk-set-assignee-button")

    def click_set_assignees_button(self):
        set_assignees_button = self.get_set_assignees_button()
        set_assignees_button.click()

    def get_set_labels_button(self):
        return self.page.get_by_test_id("bulk-set-label-button")

    def click_set_labels_button(self):
        set_labels_button = self.get_set_labels_button()
        set_labels_button.click()

    def get_mark_as_button(self):
        return self.page.locator('[data-action-bar-item="mark-as"]')

    def click_mark_as_button(self):
        mark_as_button = self.get_mark_as_button()
        mark_as_button.click()

    def get_issue_search_input(self):
        return self.page.locator('#repository-input')

    def get_mark_as_options(self):
        return self.page.get_by_role("menuitem")

    def get_new_issue_button(self):
        return self.page.get_by_text('New issue')

    def click_new_issue_button(self):
        new_issue_button = self.get_new_issue_button()
        new_issue_button.click()
