# features/login.feature — Gherkin 功能文件（业务可读）

Feature: Login
  # 业务价值描述（可选）：方便 PO/BA/Dev/QA 对齐理解
  #As a user of the web app
  #I want to sign in
  #So that I can access my dashboard

  Background:
    Given I am in login page

  @login
  Scenario: navigate to home page
    Given I open the login page and verify
    When I verify logged in and land on dashboard page
    # When I login with username "wrong_user" and password "wrong_pass"
    # Then I should see a login error


