# tests/steps/test_login_steps.py — 步骤定义（Given/When/Then）
# 只表达业务意图，不写底层定位（交给 Page Object）

import time
import pytest
from pytest_bdd import given, when, then, parsers, scenarios
from pages.login_page import LoginPage
from ultilities.jsonReader import JsonReader

scenarios('../../features/login.feature')

@pytest.fixture
def user_creds():
    jr =  JsonReader()
    return jr.get_user_credentials()

@given("I am in login page", target_fixture="login_page")
def start_loginPage(page):
    lp = LoginPage(page)
    return lp

@given("I open the login page and verify")
def open_login(login_page: LoginPage, user_creds):
    """打开登录页，并返回 Page Object 供后续步骤复用"""
   
    login_page.login(user_creds["login_email"], user_creds["login_password"])
    time.sleep(3)

@when("I select different schemes")
def i_select_different_schemes(login_page: LoginPage):
    login_page.loginPage.selectSchemes()
    

@when(parsers.cfparse('I login with username "{username}" and password "{password}"'), )
def do_login(login_page: LoginPage, username: str, password: str):
    """执行登录动作（参数来自 Gherkin 场景）"""
    login_page.login(user_creds["login_email"], user_creds["login_password"])
