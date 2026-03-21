from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

security = HTTPBearer()


# =========================
# 🔐 GET CURRENT USER
# =========================
def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):

    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload   # {user_id, role}

    except:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# =========================
# 🔥 REQUIRE VENDOR
# =========================
def require_vendor(current_user = Depends(get_current_user)):

    if current_user["role"] != "vendor":
        raise HTTPException(
            status_code=403,
            detail="Only vendors can perform this action"
        )

    return current_user