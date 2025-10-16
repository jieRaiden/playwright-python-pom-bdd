# pages/login_page.py — 登录页 Page Object

import time
from playwright.sync_api import expect
from .base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)  # 初始化基类
        # 定位器定义：尽量语义化（label/role），退而求其次 data-testid / CSS

        self.emailusername = self.page.locator("#userEmail")
        self.password = self.page.locator("#userPassword")
        self.loginBtn = self.page.locator("#login")

        self.toastMessage = self.page.locator("#toast-container")


    def open(self):
        """打开登录页"""
        # self.goto("")

    def verifyTitle(self):
        self.expect_title_contains("Swagger UI")

    def verifyHyperLinks(self):
        self.click_and_verify_title(self.sampleLink1, "API Documentation & Design Tools for Teams | Swagger")
        self.click_and_verify_title(self.sampleLink2, "Swagger Support")
        self.click_and_verify_title(self.sampleLink3, "Swagger Support")
        self.click_and_verify_title(self.tosLink, "Terms of Use | SmartBear Software")
        # self.click_and_verify_title(self.contactDevLink, "API Documentation & Design Tools for Teams | Swagger")
        self.click_and_verify_title(self.apacheLink, "Apache License, Version 2.0 | Apache Software Foundations")
        self.click_and_verify_title(self.fomLink, "API Documentation & Design Tools for Teams | Swagger")

    def selectSchemes(self):
        self.schemesDropdown.select_option("http")
        self.schemesDropdown.select_option("https")


    def login(self, user: str, pwd: str):
        """执行登录动作"""
        print(user + ", " + pwd)
        self.emailusername.fill(user)
        self.password.fill(pwd)
        self.loginBtn.click()

    def assert_error_visible(self):
        """断言：错误提示可见（失败场景）"""
        expect(self.error).to_be_visible()

    def assert_logged_in(self, who: str):
        """断言：成功进入 Dashboard 并出现欢迎语（示例）"""
        self.wait_for_url_contains("/dashboard")
        expect(self.page.get_by_text(f"Welcome, {who}")).to_be_visible()

    def clearLoginCreInput(self):
        self.clearInput(self.emailusername)
        self.clearInput(self.password)
    
    def verifyToastMessage(self):
        expect(self.toastMessage).to_be_visible()




    
