from pydantic import BaseModel, Field


class EasyPaisaResponse(BaseModel):
    orderId: str = Field(
        ..., min_length=1, description="Merchant’s system generated Order ID"
    )
    storeId: int = Field(
        ge=0, description="Store ID generated during merchant registration in Easypaisa"
    )
    responseCode: str = Field(
        ...,
        min_length=4,
        max_length=4,
        description="Easypaisa generated response codes",
    )
    responseDesc: str = Field(
        ..., min_length=3, description="Easypaisa generated response descriptions"
    )


# Code : Description
#
# 0000 = SUCCESS
# 0001 = SYSTEM ERROR
# 0002 = REQUIRED FIELD MISSING
# 0005 = MERCHANT ACCOUNT NOT ACTIVE
# 0006 = INVALID STORE ID
# 0007 = STORE NOT ACTIVE
# 0008 = PAYMENT METHOD NOT ENABLED
# 0010 = INVALID CREDENTIALS
# 0013 = LOW BALANCE
# 0014 = ACCOUNT DOES NOT EXIST


class EasyPaisaMAResponse(EasyPaisaResponse):
    transactionId: str = Field(..., description="Transaction ID of Ericsson (EWP ID)")
    transactionDateTime: str = Field(
        ..., description="Format = dd/MM/yyyy hh:mm [AM/PM]"
    )
