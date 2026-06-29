import httpx

from .headers.easypaisa import generate_auth_header
from .schemas.easypaisa import EasyPaisaMAResponse


class EasyPaisa:
    def __init__(self, store_id: str, username: str, password: str, sandbox: bool):
        self.store_id = store_id
        self.username = username
        self.password = password
        self.sandbox = sandbox

        self.base_url = (
            "https://easypaystg.easypaisa.com.pk/easypay-service/rest/v4/initiate-ma-transaction"
            if self.sandbox
            else "https://easypay.easypaisa.com.pk/easypay-service/rest/v4/initiate-ma-transaction"
        )

    async def pay_via_ma(
        self, order_id: str, amount: str, mobile_number: str, email: str
    ):
        header = generate_auth_header(self.username, self.password)
        request_payload = {
            "orderId": order_id,
            "storeId": self.store_id,
            "transactionAmount": amount,
            "transactionType": "MA",
            "mobileAccountNo": mobile_number,
            "emailAddress": email,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                json=request_payload,
                headers={"Authorization": header},
            )
            return EasyPaisaMAResponse(**response.json())
