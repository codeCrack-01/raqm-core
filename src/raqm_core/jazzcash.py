from datetime import datetime, timedelta
from typing import Optional

import httpx

from src.raqm_core.headers.jazzcash import generate_secure_hash
from src.raqm_core.schemas.jazzcash import JazzcashMWalletRequest, JazzcashResponse


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
            "https://sandbox.jazzcash.com.pk/ApplicationAPI/API/2.0/"
            if self.sandbox
            else "https://payments.jazzcash.com.pk/ApplicationAPI/API/2.0/"
        )

    async def _post(self, endpoint: str, payload: dict) -> dict:
        response = await self._client.post(
            self.base_url + endpoint,
            json=payload,
        )
        return response.json()

    async def pay_via_mwallet(
        self,
        mobile_number: str,
        amount: str,
        description: str,
        bill_reference: str,
        txn_ref_no: str,
    ) -> (
        JazzcashResponse
    ):  # txn_ref_no — unique transaction ID, developer generates this
        now = datetime.now()

        pp_TxnDateTime = now.strftime("%Y%m%d%H%M%S")
        pp_TxnExpiryDateTime = (now + timedelta(hours=1)).strftime("%Y%m%d%H%M%S")

        request = JazzcashMWalletRequest(
            pp_Language="EN",
            pp_MerchantID=self.merchant_id,
            pp_SubMerchantID=self.sub_merchant_id,
            pp_Password=self.password,
            pp_TxnRefNo=txn_ref_no,
            pp_Amount=amount,
            pp_TxnCurrency="PKR",
            pp_TxnDateTime=pp_TxnDateTime,
            pp_BillReference=bill_reference,
            pp_Description=description,
            pp_TxnExpiryDateTime=pp_TxnExpiryDateTime,
            pp_MobileNumber=mobile_number,
        )  # type: ignore

        payload = request.model_dump()
        secure_hash = generate_secure_hash(hash_key=self.hash_key, params=payload)

        payload["pp_SecureHash"] = secure_hash
        data = await self._post(endpoint="DoMWalletTransaction", payload=payload)

        return JazzcashResponse(**data)
