# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from models.user import User
from schemas.user import UserCreate, UserLogin
from utils.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/Auth", tags=["Auth"])
# =========================
# DB connection
# =========================



# =========================
# SIGNUP
# =========================
# VALID ROLES
VALID_ROLES = ["user", "vendor", "admin"]

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):

    email = user.email.strip().lower()
    password = user.password.strip()
    role = user.role.lower() if user.role else "user"

    # 🔹 role validation
    if role not in VALID_ROLES:
        raise HTTPException(status_code=400, detail="Invalid role")

    # 🔐 password validation
    if len(password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    # 🔍 check existing
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(password)

    new_user = User(
        email=email,
        password=hashed_password,
        role=role   # 🔥 important
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": f"{role} created successfully"}

# =========================
# LOGIN
# =========================
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    email = user.email.strip().lower()
    password = user.password.strip()
    role = user.role.lower() if user.role else "user"

    db_user = db.query(User).filter(User.email == email).first()

    # 🔐 common error (security)
    if not db_user or not verify_password(password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # 🔥 ROLE CHECK (IMPORTANT)
    if db_user.role != role:
        raise HTTPException(
            status_code=403,
            detail=f"You are not registered as {role}"
        )

    token = create_access_token({
        "user_id": db_user.id,
        "role": db_user.role
    })

    return {
        "access_token": token,
        "role": db_user.role,
        "token_type": "bearer"
    }