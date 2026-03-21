from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from dependencies.auth import require_vendor, get_current_user
from models.user import Product

router = APIRouter()

security = HTTPBearer(auto_error=False)


# =========================
# ADD PRODUCT (ONLY VENDOR)
# =========================
@router.post("/products")
def add_product(
    name: str,
    price: int,
    db: Session = Depends(get_db),
    user = Depends(require_vendor)
):

    new_product = Product(
        name=name,
        price=price,
        vendor_id=user["user_id"]
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "message": "Product added",
        "product_id": new_product.id
    }


# =========================
# GET PRODUCTS (SMART + PAGINATION)
# =========================
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