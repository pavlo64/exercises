import httpx
from typing import Optional, Dict, Any, Literal
from tenacity import retry, stop_after_attempt, wait_exponential


class BaseAPIClient:
    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None, timeout: int = 10):
        self.base_url = base_url
        self.headers = headers or {}
        self.timeout = timeout

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def request(
        self,
        endpoint: str,
        method: Literal["GET", "POST", "PUT", "DELETE"] = "GET",
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        extra_headers: Optional[Dict[str, str]] = None
    ) -> Any:
        try:
            async with httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout) as client:
                response = await client.request(
                    method=method,
                    url=endpoint,
                    headers={**self.headers, **(extra_headers or {})},
                    params=params,
                    data=data,
                    json=json
                )
                response.raise_for_status()
                return response.json()
        except httpx.RequestError as e:
            print(f"[HTTP ERROR] {e}")
            raise
        except httpx.HTTPStatusError as e:
            print(f"[STATUS ERROR] {e.response.status_code} {e.response.text}")
            raise
