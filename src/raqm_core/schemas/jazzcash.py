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
    # Will add more if necessary, the docs are vague though...


class JazzcashOTCResponse(BaseModel):
    pp_Amount: str = Field(
        ...,
        description="The transaction amount. Please note that no decimal places are included. Decimal place will be assumed at the default position of the currency provided.",
    )
    pp_AuthCode: str = Field(..., description="Authorization code for the transaction.")
    pp_BankID: str = Field(..., description="Bank identifier for the transaction.")
    pp_BillReference: str = Field(..., description="Bill/invoice Number being settled.")
    pp_Language: str = Field(
        ...,
        description="Specifies the language in which to display the page. Fixed value 'EN'.",
    )
    pp_MerchantID: str = Field(
        ..., description="Unique Id assigned to each merchant by the payment gateway."
    )
    pp_ResponseCode: str = Field(
        ...,
        min_length=3,
        max_length=3,
        description="Response code indicating transaction status.",
    )
    pp_ResponseMessage: str = Field(
        ..., min_length=3, description="Response message describing transaction status."
    )
    pp_RetreivalReferenceNo: str = Field(
        ..., description="Retrieval reference number for the transaction."
    )
    pp_SubMerchantId: str = Field(
        ...,
        description="Unique Id assigned to each sub merchant by the payment gateway.",
    )
    pp_TxnCurrency: str = Field(
        ..., description="Currency of transaction amount. It has a fixed value 'PKR'."
    )
    pp_TxnDateTime: str = Field(
        ...,
        description="Merchant provided date and time of transaction. The format of date time should be yyyyMMddHHmmss.",
    )
    pp_TxnRefNo: str = Field(
        ...,
        description="A unique value created by the merchant to identify the transaction.",
    )
    pp_SettlementExpiry: str = Field(
        ..., description="Settlement expiry date for the transaction."
    )
    pp_TxnType: str = Field(
        ..., description="Type of instrument used for making payment."
    )
    pp_Version: str = Field(
        ...,
        description="Payment Portal Version. Refer to JazzCash API docs for details",
    )
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
    pp_SecureHash: str = Field(
        ...,
        description="Used to allow the Payment Gateway to check the integrity of the transaction request.",
    )
