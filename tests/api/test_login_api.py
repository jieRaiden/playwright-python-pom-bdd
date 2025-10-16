import os

import pytest
from pytest_bdd import given
import requests

from api.login_api import LoginAPI
from ultilities.jsonReader import JsonReader


# @pytest.fixture(scope="session")
# def api_base_url() -> str:
#     return os.getenv("API_BASE_URL", "https://rahulshettyacademy.com")


# @pytest.fixture(scope="session")
# def api_session() -> requests.Session:
#     session = requests.Session()
#     yield session
#     session.close()


@pytest.fixture(scope="session")
def login_api(api_base_url: str, api_session: requests.Session) -> LoginAPI:
    return LoginAPI(base_url=api_base_url, session=api_session)


# @pytest.mark.api
# @given('I have a valid auth token', target_fixture="userApi_Cred")
# def login_api_returns_token(login_api: LoginAPI):
#     credentials = JsonReader().get_user_credentials()
#     response = login_api.login(credentials["login_email"], credentials["login_password"])
#     print("Token: " + response.token)
#     print("User_id: " + response.user_id)
#     assert response.token
#     assert response.user_id
#     return response

@pytest.mark.loginapi
@given('I put wrong credential to login')
def test_login_api_with_wrong_cred(login_api: LoginAPI):
    with pytest.raises(requests.HTTPError) as exc_info:
        login_api.login("wrong@example.com", "badpass")

    error = exc_info.value
    response = error.response  # requests.HTTPError 会挂载原始 Response
    print("Status code:", response.status_code)
    print("Message:", response.text)