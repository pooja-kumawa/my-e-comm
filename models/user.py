# models/user.py
from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)

    role = Column(String(50), default="user")  # user/vendor/admin



class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255))
    price = Column(Integer)

    # 🔥 IMPORTANT (vendor relation)
    vendor_id = Column(Integer, ForeignKey("users.id"))