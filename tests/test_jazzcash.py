import httpx
import pytest

from src.raqm_core.jazzcash import JazzCash

MWALLET_SUCCESS_BODY = {
    "pp_Amount": "1000",
    "pp_AuthCode": "123456",
    "pp_BankID": "",
    "pp_BillReference": "bill123",
    "pp_Language": "EN",
    "pp_MerchantID": "MERCH123",
    "pp_ResponseCode": "000",
    "pp_ResponseMessage": "Success",
    "pp_RetreivalReferenceNo": "RET123",
    "pp_SubMerchantId": "SUBMERCH123",
    "pp_TxnCurrency": "PKR",
    "pp_TxnDateTime": "20260101120000",
    "pp_TxnRefNo": "TXN123456",
    "pp_SettlementExpiry": "20260101130000",
    "pp_TxnType": "MWALLET",
    "pp_Version": "1.1",
    "pp_SecureHash": "abc123hash",
}


def make_client(response_body: dict) -> httpx.AsyncClient:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code=200, json=response_body)

    return httpx.AsyncClient(transport=httpx.MockTransport(handler))


def make_jc(response_body: dict) -> JazzCash:
    return JazzCash(
        merchant_id="MERCH123",
        sub_merchant_id="SUBMERCH123",
        hash_key="test_hash_key",
        password="test_password",
        sandbox=True,
        client=make_client(response_body),
    )


class TestPayViaMWallet:
    @pytest.mark.asyncio
    async def test_success(self):
        jc = make_jc(MWALLET_SUCCESS_BODY)
        result = await jc.pay_via_mwallet(
            mobile_number="03001234567",
            amount="1000",
            description="Test payment",
            bill_reference="bill123",
            txn_ref_no="TXN123456",
        )
        assert result.pp_ResponseCode == "000"
        assert result.pp_ResponseMessage == "Success"
        assert result.pp_TxnRefNo == "TXN123456"
        assert result.pp_Amount == "1000"
        assert result.pp_MerchantID == "MERCH123"

    @pytest.mark.parametrize(
        ("body", "expected_code"),
        [
            ({"pp_ResponseCode": "001", "pp_ResponseMessage": "LIMIT EXCEEDED"}, "001"),
            ({"pp_ResponseCode": "002", "pp_ResponseMessage": "ACCOUNT NOT FOUND"}, "002"),
            ({"pp_ResponseCode": "115", "pp_ResponseMessage": "INVALID HASH"}, "115"),
            ({"pp_ResponseCode": "199", "pp_ResponseMessage": "SYSTEM ERROR"}, "199"),
            ({"pp_ResponseCode": "403", "pp_ResponseMessage": "TRANSACTION TIMED OUT"}, "403"),
            ({"pp_ResponseCode": "405", "pp_ResponseMessage": "INSUFFICIENT BALANCE"}, "405"),
        ],
    )
    @pytest.mark.asyncio
    async def test_error_codes(self, body, expected_code):
        payload = {**MWALLET_SUCCESS_BODY, **body}
        jc = make_jc(payload)
        result = await jc.pay_via_mwallet(
            mobile_number="03001234567",
            amount="1000",
            description="Test payment",
            bill_reference="bill123",
            txn_ref_no="TXN123456",
        )
        assert result.pp_ResponseCode == expected_code
