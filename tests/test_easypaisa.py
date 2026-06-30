import httpx
import pytest

from src.easypaisa import EasyPaisa


MA_SUCCESS_BODY = {
    "orderId": "abc123",
    "storeId": 43,
    "transactionId": "253184",
    "transactionDateTime": "11/08/2018 11:30 PM",
    "responseCode": "0000",
    "responseDesc": "SUCCESS",
}

OTC_SUCCESS_BODY = {
    "orderId": "abc123",
    "storeId": 43,
    "transactionDateTime": "11/08/2021 11:30 PM",
    "responseCode": "0000",
    "responseDesc": "SUCCESS",
    "paymentToken": "tok_abc123",
    "paymentTokenExpiryDateTime": "12/08/2021 11:30 PM",
}

INQUIRE_SUCCESS_BODY = {
    "orderId": "abc123",
    "storeId": 43,
    "transactionId": "253184",
    "transactionDateTime": "11/08/2021 11:30 PM",
    "responseCode": "0000",
    "responseDesc": "SUCCESS",
    "accountNum": "123456789",
    "storeName": "Test Store",
    "paymentToken": None,
    "transactionStatus": "COMPLETED",
    "transactionAmount": "1.23",
    "paymentTokenExpiryDateTime": None,
    "msisdn": "03458508726",
    "paymentMode": "MA",
}


def make_client(response_body: dict) -> httpx.AsyncClient:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code=200, json=response_body)

    return httpx.AsyncClient(transport=httpx.MockTransport(handler))


def make_ep(response_body: dict) -> EasyPaisa:
    return EasyPaisa(
        store_id="43",
        username="admin",
        password="123",
        sandbox=True,
        client=make_client(response_body),
    )


class TestPayViaMA:
    @pytest.mark.asyncio
    async def test_success(self):
        ep = make_ep(MA_SUCCESS_BODY)
        result = await ep.pay_via_ma(
            order_id="abc123",
            amount="1.23",
            email="test@example.com",
            mobile_number="03458508726",
        )
        assert result.orderId == "abc123"
        assert result.transactionId == "253184"
        assert result.responseCode == "0000"

    @pytest.mark.parametrize(
        ("body", "expected_code"),
        [
            ({"responseCode": "0001", "responseDesc": "SYSTEM ERROR"}, "0001"),
            ({"responseCode": "0006", "responseDesc": "INVALID STORE ID"}, "0006"),
            ({"responseCode": "0010", "responseDesc": "INVALID CREDENTIALS"}, "0010"),
        ],
    )
    @pytest.mark.asyncio
    async def test_error_codes(self, body, expected_code):
        payload = {**MA_SUCCESS_BODY, **body}
        ep = make_ep(payload)
        result = await ep.pay_via_ma(
            order_id="abc123",
            amount="1.23",
            email="test@example.com",
            mobile_number="03458508726",
        )
        assert result.responseCode == expected_code


class TestPayViaOTC:
    @pytest.mark.asyncio
    async def test_success(self):
        ep = make_ep(OTC_SUCCESS_BODY)
        result = await ep.pay_via_otc(
            order_id="abc123",
            amount="1.23",
            email="test@example.com",
            msisdn="03458508726",
            token_expiry="11/12/2018 11:30 PM",
        )
        assert result.orderId == "abc123"
        assert result.responseCode == "0000"
        assert result.paymentToken == "tok_abc123"

    @pytest.mark.parametrize(
        ("body", "expected_code"),
        [
            ({"responseCode": "0001", "responseDesc": "SYSTEM ERROR"}, "0001"),
            ({"responseCode": "0006", "responseDesc": "INVALID STORE ID"}, "0006"),
            ({"responseCode": "0010", "responseDesc": "INVALID CREDENTIALS"}, "0010"),
        ],
    )
    @pytest.mark.asyncio
    async def test_error_codes(self, body, expected_code):
        payload = {**OTC_SUCCESS_BODY, **body}
        ep = make_ep(payload)
        result = await ep.pay_via_otc(
            order_id="abc123",
            amount="1.23",
            email="test@example.com",
            msisdn="03458508726",
            token_expiry="11/12/2018 11:30 PM",
        )
        assert result.responseCode == expected_code


class TestInquireTransaction:
    @pytest.mark.asyncio
    async def test_success(self):
        ep = make_ep(INQUIRE_SUCCESS_BODY)
        result = await ep.inquire_transaction_status(
            order_id="abc123", account_number="123456789"
        )
        assert result.orderId == "abc123"
        assert result.responseCode == "0000"
        assert result.transactionStatus == "COMPLETED"
        assert result.accountNum == "123456789"
        assert result.storeName == "Test Store"
        assert result.msisdn == "03458508726"
        assert result.paymentMode == "MA"

    @pytest.mark.parametrize(
        ("body", "expected_code"),
        [
            ({"responseCode": "0001", "responseDesc": "SYSTEM ERROR"}, "0001"),
            ({"responseCode": "0006", "responseDesc": "INVALID STORE ID"}, "0006"),
            ({"responseCode": "0010", "responseDesc": "INVALID CREDENTIALS"}, "0010"),
        ],
    )
    @pytest.mark.asyncio
    async def test_error_codes(self, body, expected_code):
        payload = {**INQUIRE_SUCCESS_BODY, **body}
        ep = make_ep(payload)
        result = await ep.inquire_transaction_status(
            order_id="abc123", account_number="123456789"
        )
        assert result.responseCode == expected_code
