from dataclasses import dataclass
import os
from typing import Any, Dict, Optional
import requests

from ultilities.jsonReader import JsonReader

@dataclass(frozen=True)
class AddtocartResponse:
    """Typed structure for the addtocart endpoint response."""

    message: Optional[str] = None

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "AddtocartResponse":
        return cls(
            message=payload.get("message"),
        )
    
class CartsAPI:

    def __init__(
        self,
        base_url: Optional[str] = None,
        session: Optional[requests.Session] = None,
        timeout: float = 15.0,
    ) -> None:
        self._base_url = (base_url or os.getenv("API_BASE_URL", "https://rahulshettyacademy.com")).rstrip("/")
        self._session = session or requests.Session()
        self._timeout = timeout

    def addtoCart(self, token: str, userid: str, product:dict) -> AddtocartResponse:
        """
        Authenticate with the API and return the structured response.

        Raises:
            requests.HTTPError: if the API responds with a non-success status code.
            KeyError: if expected keys are missing from the response payload.
        """
        endpoint = f"{self._base_url}/api/ecom/user/add-to-cart"
        headers = {"Authorization": token}
        payload = {"_id": userid, "product": product}
        response = self._session.post(endpoint, json=payload, headers=headers, timeout=self._timeout)
        response.raise_for_status()
        data = response.json()
        return AddtocartResponse.from_dict(data)