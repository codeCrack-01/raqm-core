from typing import Optional

import httpx


class JazzCash:
    def __init__(
        self,
        merchant_id: str,
        sub_merchant_id: str,
        hash_key: str,
        password: str,
        sandbox: bool,
        client: Optional[httpx.AsyncClient] = None,
    ):
        self.merchant_id = merchant_id
        self.sub_merchant_id = sub_merchant_id
        self.password = password
        self.sandbox = sandbox
        self._client = client or httpx.AsyncClient()
        self.hash_key = hash_key
        self.base_url = (
            "https://sandbox.jazzcash.com.pk/..."
            if self.sandbox
            else "https://payments.jazzcash.com.pk/.."
        )
