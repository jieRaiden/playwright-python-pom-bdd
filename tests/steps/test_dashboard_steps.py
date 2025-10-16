import pytest
from playwright.sync_api import Page
from pytest_bdd import scenarios, when, parsers

from pages.dashboard_page import DashboardPage



scenarios("../../features/dashboard.feature")
scenarios("../../features/orders.feature")

pytest_plugins = [
    "tests.steps.test_login_steps",
]


@pytest.fixture
def dashboard_page(page: Page) -> DashboardPage:
    return DashboardPage(page)


@when("I verify logged in and land on dashboard page")
def verify_user_lands_on_dashboard(dashboard_page: DashboardPage) -> None:
    dashboard_page.verifyUserLoggedin()

@when(parsers.parse('I navigate to "{pageTitle}" page'))
def navigate_to_pages(dashboard_page: DashboardPage, pageTitle) -> None:
    dashboard_page.navigateTo(pageTitle)

@when("I click each item and verify in detail page")
def click_and_check_detail_page(dashboard_page: DashboardPage) -> None:
    # dashboard_page.verifyCartNumber()
    dashboard_page.verifyItem_Dashboard_To_Detail()
