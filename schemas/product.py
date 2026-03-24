from pydantic import BaseModel
from typing import List, Optional

class ProductCreate(BaseModel):
    name: str
    price: int
    description: Optional[str]
    highlights: Optional[str]
    additional_info: Optional[str]
    size: Optional[str]
    color: Optional[str]
    seller_name: Optional[str]
    product_status: Optional[str] = "active"