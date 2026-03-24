import json

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from dependencies.auth import require_vendor, get_current_user
from models.user import Product

from fastapi import APIRouter, Depends, Form, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import uuid

router = APIRouter()

security = HTTPBearer(auto_error=False)

def empty_to_none(value):
    return value if value not in ["", None] else None


@router.post("/products")
def add_product(
    name: str = Form(...),
    price: int = Form(...),
    product_status: str = Form(...),  # ✅ required

    description: str = Form(None),
    highlights: str = Form(None),
    additional_info: str = Form(None),
    size: str = Form(None),
    color: str = Form(None),
    seller_name: str = Form(None),

    images: List[UploadFile] = File(...),  # ✅ required

    db: Session = Depends(get_db),
    user = Depends(require_vendor)
):
    # ❌ validate images
    if not images or len(images) == 0:
        raise HTTPException(status_code=400, detail="At least one image is required")

    image_paths = []

    upload_dir = "static/products"
    os.makedirs(upload_dir, exist_ok=True)

    for image in images:
        filename = f"{uuid.uuid4()}_{image.filename}"
        filepath = os.path.join(upload_dir, filename)

        with open(filepath, "wb") as f:
            f.write(image.file.read())

        image_paths.append(filepath)

    new_product = Product(
        name=name,
        price=price,
        product_status=product_status,

        description=empty_to_none(description),
        highlights=empty_to_none(highlights),
        additional_info=empty_to_none(additional_info),
        size=empty_to_none(size),
        color=empty_to_none(color),
        seller_name=empty_to_none(seller_name),

        images=json.dumps(image_paths),

        vendor_id=user["user_id"]
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "message": "Product added successfully",
        "product_id": new_product.id
    }




@router.get("/products")
def get_products(
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
):

    offset = (page - 1) * limit

    try:
        if token:
            user = get_current_user(token)

            # 🔥 Vendor → only his products
            if user["role"] == "vendor":
                query = db.query(Product).filter(
                    Product.vendor_id == user["user_id"]
                )
            else:
                query = db.query(Product)
        else:
            query = db.query(Product)

    except:
        query = db.query(Product)

    total = query.count()
    products = query.offset(offset).limit(limit).all()

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "data": products
    }