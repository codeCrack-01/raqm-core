from typing import Optional

import httpx

from .headers.easypaisa import generate_auth_header
from .schemas.easypaisa import (
    EasyaisaMAResponse,
    EasyPaisaInquireTransactionResponse,
    EasyPaisaOTCResponse,
)


class EasyPaisa:
    def __init__(
        self,
        store_id: str,
        username: str,
        password: str,
        sandbox: bool,
        client: Optional[httpx.AsyncClient] = None,
    ):
        self.store_id = store_id
        self.username = username
        self.password = password
        self.sandbox = sandbox
        self._client = client or httpx.AsyncClient()

        self.base_url = (
            "https://easypaystg.easypaisa.com.pk/easypay-service/rest/v4/"
            if self.sandbox
            else "https://easypay.easypaisa.com.pk/easypay-service/rest/v4/"
        )

    async def _post(self, endpoint: str, payload: dict) -> dict:
        header = generate_auth_header(self.username, self.password)
        response = await self._client.post(
            self.base_url + endpoint,
            json=payload,
            headers={"Authorization": header},
        )
        return response.json()

    async def pay_via_otc(
        self, order_id: str, amount: str, email: str, msisdn: str, token_expiry: str
    ):
        request_payload = {
            "orderId": order_id,
            "storeId": self.store_id,
            "transactionAmount": amount,
            "transactionType": "OTC",
            "msisdn": msisdn,
            "emailAddress": email,
            "tokenExpiry": token_expiry,
        }
        data = await self._post("initiate-otc-transaction", request_payload)
        return EasyPaisaOTCResponse(**data)

    async def pay_via_ma(
        self, order_id: str, amount: str, email: str, mobile_number: str
    ):
        request_payload = {
            "orderId": order_id,
            "storeId": self.store_id,
            "transactionAmount": amount,
            "transactionType": "MA",
            "mobileAccountNo": mobile_number,
            "emailAddress": email,
        }
        data = await self._post("initiate-ma-transaction", request_payload)
        return EasyaisaMAResponse(**data)

    async def inquire_transaction_status(self, order_id: str, account_number: str):
        request_payload = {
            "orderId": order_id,
            "storeId": self.store_id,
            "accountNum": account_number,
        }
        data = await self._post("inquire-transaction", request_payload)
        return EasyPaisaInquireTransactionResponse(**data)
