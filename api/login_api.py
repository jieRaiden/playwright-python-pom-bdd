from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class LoginResponse:
    """Typed structure for the login endpoint response."""

    token: str
    user_id: str
    message: Optional[str] = None

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "LoginResponse":
        return cls(
            token=payload["token"],
            user_id=payload["userId"],
            message=payload.get("message"),
        )


class LoginAPI:
    """Client wrapper around the Rahul Shetty Academy login endpoint."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        session: Optional[requests.Session] = None,
        timeout: float = 15.0,
    ) -> None:
        self._base_url = (base_url or os.getenv("API_BASE_URL", "https://rahulshettyacademy.com")).rstrip("/")
        self._session = session or requests.Session()
        self._timeout = timeout

    @property
    def base_url(self) -> str:
        return self._base_url

    def login(self, email: str, password: str) -> LoginResponse:
        """
        Authenticate with the API and return the structured response.

        Raises:
            requests.HTTPError: if the API responds with a non-success status code.
            KeyError: if expected keys are missing from the response payload.
        """
        endpoint = f"{self._base_url}/api/ecom/auth/login"
        payload = {"userEmail": email, "userPassword": password}
        response = self._session.post(endpoint, json=payload, timeout=self._timeout)
        response.raise_for_status()
        data = response.json()
        return LoginResponse.from_dict(data)
