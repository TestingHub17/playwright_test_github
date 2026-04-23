class LoginPage:
    def __init__(self, page):
        self.page = page

    login_link = 'https://github.com/login'

    def navigate_to_login_page(self):
        self.page.goto(self.login_link, wait_until='load')

    def get_username_field(self):
        return self.page.locator('#login_field')

    def get_password_field(self):
        return self.page.locator('#password')

    def get_sign_in_button(self):
        return self.page.locator('[data-signin-label="Sign in"]')

    def enter_username(self, username):
        self.get_username_field().fill(username)

    def enter_password(self, password):
        self.get_password_field().fill(password)

    def click_sign_in(self):
        self.get_sign_in_button().click()

