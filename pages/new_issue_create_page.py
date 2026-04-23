from playwright.sync_api import Page


class NewIssueCreatePage:
    def __init__(self, page:Page):
        self.page = page

    def get_create_issue_title_field(self):
        return self.page.get_by_text('Create new issue')

    def get_create_more_checkbox(self):
        return self.page.get_by_test_id("create-more-check")

    def click_create_more_checkbox(self):
        create_more_checkbox = self.get_create_more_checkbox()
        create_more_checkbox.click()

    def get_create_more_text(self):
        return self.page.get_by_label("Create more")

    def get_cancel_button(self):
        return self.page.get_by_role("button", name="Cancel")

    def click_cancel_button(self):
        cancel_button = self.get_cancel_button()
        cancel_button.click()

    def get_create_issue_button(self):
        return  self.page.get_by_test_id('create-issue-button')

    def click_create_issue_button(self):
        create_issue_button = self.get_create_issue_button()
        create_issue_button.click()
