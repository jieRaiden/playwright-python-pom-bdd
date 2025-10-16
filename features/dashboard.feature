Feature: Dashboard related features

Background:
    Given I am in login page

    @dashboard
  Scenario: check loggedin in dashboard page
    Given I open the login page and verify
    When I verify logged in and land on dashboard page

    @dashboard @menubar
  Scenario: navigate to different pages
    Given I open the login page and verify
    When I navigate to "ORDERS" page
    When I navigate to "Cart" page
    When I navigate to "HOME" page

     @dashboard @detail
  Scenario: verify item to detail page
    Given I open the login page and verify
    When I click each item and verify in detail page

