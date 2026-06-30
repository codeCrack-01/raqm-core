# raqm-core

**Unified Python SDK for Pakistani payment gateways.**

One async, type-safe interface across multiple processors — EasyPaisa, JazzCash, HBL, ABL, UBL, and more.

> ⚠️ **Work in progress.** Currently only EasyPaisa is fully implemented. Contributions welcome!

---

## Supported Gateways

| Gateway | Status |
|---------|--------|
| [EasyPaisa](https://easypaisa.com.pk) | ✅ Live |
| [JazzCash](https://jazzcash.com.pk) | 🚧 Header utils ready |
| HBL | 📅 Planned |
| ABL | 📅 Planned |
| UBL | 📅 Planned |
| … | 📅 Your gateway here |

---

## Features

- **Async-first** — built on `httpx.AsyncClient` for non-blocking I/O
- **Type-safe** — all responses are validated through Pydantic models
- **Consistent API** — same patterns across all gateways
- **Mock-friendly** — inject your own `httpx.AsyncClient` for testing
- **Minimal dependencies** — just `httpx` and `pydantic`

---

## Installation

```bash
pip install raqm-core
```

Or with `uv`:

```bash
uv add raqm-core
```

> Requires Python 3.12+.

---

## Quick Start

```python
import asyncio
from raqm_core import EasyPaisa


async def main():
    ep = EasyPaisa(
        store_id="43",
        username="your_username",
        password="your_password",
        sandbox=True,
    )

    result = await ep.pay_via_ma(
        order_id="order_123",
        amount="1000.00",
        email="customer@example.com",
        mobile_number="03451234567",
    )

    print(f"Status: {result.responseCode} — {result.responseDesc}")
    print(f"Transaction ID: {result.transactionId}")


asyncio.run(main())
```

---

## Usage

### EasyPaisa

#### Initialisation

```python
from raqm_core import EasyPaisa

ep = EasyPaisa(
    store_id="43",
    username="your_username",
    password="your_password",
    sandbox=True,           # set False for production
)
```

You can optionally inject your own `httpx.AsyncClient` — useful for testing with `httpx.MockTransport`:

```python
import httpx

client = httpx.AsyncClient(...)
ep = EasyPaisa(store_id="43", username="...", password="...", sandbox=True, client=client)
```

#### Mobile Account (MA) Payment

```python
result = await ep.pay_via_ma(
    order_id="order_123",
    amount="500.00",
    email="customer@example.com",
    mobile_number="03451234567",
)

# EasyPaisaMAResponse fields:
result.orderId           # str
result.storeId           # int
result.transactionId     # str
result.transactionDateTime  # str (dd/MM/yyyy hh:mm AM/PM)
result.responseCode      # EasypaisaResponseCode (enum)
result.responseDesc      # str
```

#### Over-the-Counter (OTC) Payment

```python
result = await ep.pay_via_otc(
    order_id="order_456",
    amount="1500.00",
    email="customer@example.com",
    msisdn="03451234567",
    token_expiry="01/01/2025 11:59 PM",
)

# EasyPaisaOTCResponse fields (extends base):
result.paymentToken              # str
result.paymentTokenExpiryDateTime  # str
```

#### Transaction Inquiry

```python
result = await ep.inquire_transaction_status(
    order_id="order_123",
    account_number="123456789",
)

# EasyPaisaInquireTransactionResponse fields:
result.transactionStatus   # str (e.g. "COMPLETED")
result.transactionAmount   # str
result.accountNum          # str
result.storeName           # str
result.msisdn              # str
result.paymentMode         # str ("MA", "OTC", "CC")
```

---

## Architecture

Each payment gateway follows a consistent 3-layer structure:

```
src/
├── <gateway>.py              # Client class — public API
├── headers/
│   └── <gateway>.py          # Auth / signing helpers
└── schemas/
    └── <gateway>.py          # Pydantic request/response models
```

Current structure:

```
src/
├── easypaisa.py              # EasyPaisa client
├── headers/
│   ├── easypaisa.py          # Basic Auth header
│   └── jazzcash.py           # SHA-256 secure hash
└── schemas/
    └── easypaisa.py          # EasyPaisa Pydantic models

tests/
├── test_easypaisa.py         # EasyPaisa integration tests
└── headers/
    ├── test_easypaisa.py     # Auth header unit tests
    └── test_jazzcash.py      # Secure hash unit tests
```

---

## Adding a New Gateway

Want to add support for a new processor? Follow this checklist.

### 1. Research the API

Understand the gateway's:
- Authentication mechanism (Basic Auth, HMAC, API key, etc.)
- Endpoints and request/response formats
- Error/response codes

### 2. Create header helpers

`src/headers/<gateway>.py` — authentication or signing logic.

```python
# src/headers/hbl.py
def generate_signature(api_key: str, payload: dict) -> str:
    ...
```

Write unit tests in `tests/headers/test_<gateway>.py`.

### 3. Create Pydantic schemas

`src/schemas/<gateway>.py` — response models and enums.

```python
# src/schemas/hbl.py
from pydantic import BaseModel, Field


class HBLResponse(BaseModel):
    orderId: str = Field(...)
    responseCode: str = Field(...)
    responseDesc: str = Field(...)
```

### 4. Create the client class

`src/<gateway>.py` — async client with a `_post()` helper and public methods.

```python
# src/hbl.py
import httpx
from .headers.hbl import generate_signature
from .schemas.hbl import HBLResponse


class HBL:
    def __init__(self, api_key: str, sandbox: bool, client: httpx.AsyncClient | None = None):
        self._client = client or httpx.AsyncClient()
        ...

    async def _post(self, endpoint: str, payload: dict) -> dict:
        ...

    async def pay(self, order_id: str, amount: str, ...) -> HBLResponse:
        ...
```

### 5. Write integration tests

`tests/test_<gateway>.py` — use `httpx.MockTransport` to mock responses.

```python
# tests/test_hbl.py
import httpx
import pytest
from raqm_core import HBL


@pytest.mark.asyncio
async def test_pay_success():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code=200, json={...})

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    hbl = HBL(api_key="test", sandbox=True, client=client)
    result = await hbl.pay(...)
    assert result.responseCode == "0000"
```

### 6. Update this README

Add the new gateway to the **Supported Gateways** table with the appropriate status badge.

---

## Roadmap

- [x] EasyPaisa (MA, OTC, inquiry)
- [ ] JazzCash client + schemas
- [ ] HBL payment gateway
- [ ] ABL payment gateway
- [ ] UBL payment gateway
- [ ] Standardised error handling across gateways
- [ ] Request/response logging middleware
- [ ] CI/CD + automated testing

---

## Development

```bash
# Clone the repo
git clone https://github.com/your-username/raqm-core.git
cd raqm-core

# Create a virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv sync

# Run tests
pytest
```

---

## Contributing

Contributions are welcome! See [Adding a New Gateway](#adding-a-new-gateway) for the detailed guide.

Please open an issue first to discuss your proposed changes.

---

## License

MIT
