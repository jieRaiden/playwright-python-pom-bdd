import pytest
from pytest_bdd import when
import requests

from api.orders_api import OrdersApi
from ultilities.jsonReader import JsonReader


@pytest.fixture(scope="session")
def orders_api(api_base_url: str, api_session: requests.Session) -> OrdersApi:
    return OrdersApi(base_url=api_base_url, session=api_session)

@pytest.mark.ordersapi
@when('I buy a product and verify')
def test_addtocarts_api(orders_api: OrdersApi, userApi_Cred) -> None:
    token = userApi_Cred.token
    credentials = JsonReader().get_orders_item()
    response = orders_api.creatOrder(token, credentials["orders"])
    print(f"respon boday: {response}")
    assert response.message