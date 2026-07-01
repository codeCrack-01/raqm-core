from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class JazzCashResponseCode(str, Enum):
    SUCCESS = "000"
    LIMIT_EXCEEDED = "001"
    ACCOUNT_NOT_FOUND = "002"
    ACCOUNT_INACTIVE = "003"
    LOW_BALANCE = "004"
    INVALID_HASH = "115"
    SYSTEM_ERROR = "199"
    TRANSACTION_TIMED_OUT = "403"
    INSUFFICIENT_BALANCE = "405"


# ── REQUEST MODELS ────────────────────────────────────────────────────────────


class JazzcashRequest(BaseModel):
    pp_Version: str = Field("1.1", description="Payment Portal Version.")
    pp_Language: str = Field("EN", description="Display language. Fixed value 'EN'.")
    pp_MerchantID: str = Field(
        ..., description="Unique merchant ID assigned by JazzCash."
    )
    pp_SubMerchantID: str = Field(
        "", description="Sub merchant ID, leave empty if unused."
    )
    pp_Password: str = Field(..., description="Password assigned by JazzCash.")
    pp_BankID: str = Field("", description="Bank identifier, leave empty if unused.")
    pp_ProductID: str = Field(
        "", description="Product identifier, leave empty if unused."
    )
    pp_TxnRefNo: str = Field(..., description="Unique transaction reference number.")
    pp_Amount: str = Field(..., description="Transaction amount, no decimal places.")
    pp_TxnCurrency: str = Field(
        "PKR", description="Transaction currency. Fixed value 'PKR'."
    )
    pp_TxnDateTime: str = Field(
        ..., description="Transaction datetime. Format: yyyyMMddHHmmss."
    )
    pp_BillReference: str = Field(..., description="Bill/invoice number being settled.")
    pp_Description: str = Field(..., description="Transaction description.")
    pp_TxnExpiryDateTime: str = Field(
        ..., description="Expiry datetime. Format: yyyyMMddHHmmss."
    )
    ppmpf_1: str = ""
    ppmpf_2: str = ""
    ppmpf_3: str = ""
    ppmpf_4: str = ""
    ppmpf_5: str = ""


class JazzcashMWalletRequest(JazzcashRequest):
    pp_TxnType: str = Field("MWALLET", description="Transaction type.")
    pp_MobileNumber: str = Field(..., description="Customer's JazzCash mobile number.")


# ── RESPONSE MODELS ───────────────────────────────────────────────────────────


class JazzcashResponse(BaseModel):
    pp_Amount: str = Field(..., description="Transaction amount.")
    pp_AuthCode: Optional[str] = None
    pp_BankID: Optional[str] = None
    pp_BillReference: Optional[str] = None
    pp_Language: Optional[str] = None
    pp_MerchantID: str = Field(..., description="Merchant ID.")
    pp_ResponseCode: str = Field(..., description="Response code.")
    pp_ResponseMessage: str = Field(..., description="Response message.")
    pp_RetreivalReferenceNo: Optional[str] = None
    pp_SubMerchantId: Optional[str] = None
    pp_TxnCurrency: Optional[str] = None
    pp_TxnDateTime: Optional[str] = None
    pp_TxnRefNo: str = Field(..., description="Transaction reference number.")
    pp_SettlementExpiry: Optional[str] = None
    pp_TxnType: Optional[str] = None
    pp_Version: Optional[str] = None
    ppmbf_1: Optional[str] = None
    ppmbf_2: Optional[str] = None
    ppmbf_3: Optional[str] = None
    ppmbf_4: Optional[str] = None
    ppmbf_5: Optional[str] = None
    ppmpf_1: Optional[str] = None
    ppmpf_2: Optional[str] = None
    ppmpf_3: Optional[str] = None
    ppmpf_4: Optional[str] = None
    ppmpf_5: Optional[str] = None
    pp_SecureHash: Optional[str] = None
