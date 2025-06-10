#!/


from pydantic import BaseModel, Field
from typing import Optional

class BaseRequestModel(BaseModel):
    request_id: Optional[str] = Field(None, description="请求的唯一标识符")
    timestamp: Optional[str] = Field(None, description="请求的时间戳")
    data: Optional[dict] = Field(None, description="请求的数据")

