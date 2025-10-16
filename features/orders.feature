Feature: Orders related features

Background:
    Given I am in login page

    @orders
Scenario: check loggedin in dashboard page
    Given I open the login page and verify
    When I navigate to "Orders" page
    # Then I verify Orders page with empty order