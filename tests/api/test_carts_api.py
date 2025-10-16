

import pytest
from pytest_bdd import when
import requests
from api.carts_api import CartsAPI
from ultilities.jsonReader import JsonReader

@pytest.fixture(scope="session")
def cart_api(api_base_url: str, api_session: requests.Session) -> CartsAPI:
    return CartsAPI(base_url=api_base_url, session=api_session)

@pytest.mark.api
@when('I add product with quantity 1 and verify')
def test_addtocarts_api(cart_api: CartsAPI, userApi_Cred) -> None:
    userId = userApi_Cred.user_id
    token = userApi_Cred.token
    credentials = JsonReader().get_addtocart_item()
    response = cart_api.addtoCart(token, userId, credentials)
    print("respon boday: " + response.message)
    assert response.message
    