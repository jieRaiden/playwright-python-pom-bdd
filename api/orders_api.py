from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


@dataclass(frozen=True)
class OrdersResponse:
    """Typed structure for the orders endpoint response."""
    orders: List[str]
    productOrderId: List[str]
    message: Optional[str] = None

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "OrdersResponse":
        orders = payload.get("orders") or []
        productOrderId = payload.get("productOrderId") or []
        return cls(
            orders=orders,
            productOrderId=productOrderId,
            message=payload.get("message"),
        )
    
class OrdersApi:

    def __init__(
        self,
        base_url: Optional[str] = None,
        session: Optional[requests.Session] = None,
        timeout: float = 15.0,
    ) -> None:
        self._base_url = (base_url or os.getenv("API_BASE_URL", "https://rahulshettyacademy.com")).rstrip("/")
        self._session = session or requests.Session()
        self._timeout = timeout

    def creatOrder(self, token: str, order: List[Dict[str, Any]]) -> OrdersResponse:
        """
        Authenticate with the API and return the structured response.

        Raises:
            requests.HTTPError: if the API responds with a non-success status code.
            KeyError: if expected keys are missing from the response payload.
        """
        endpoint = f"{self._base_url}/api/ecom/order/create-order"
        headers = {"Authorization": token}
        payload = {"orders": order}
        response = self._session.post(endpoint, json=payload, headers=headers, timeout=self._timeout)
        response.raise_for_status()
        data = response.json()
        return OrdersResponse.from_dict(data)