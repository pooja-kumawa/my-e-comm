# models/user.py
from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.dialects.postgresql import JSON  # if using Postgres

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)

    role = Column(String(50), default="user")  # user/vendor/admin

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)

    description = Column(Text, nullable=True)
    highlights = Column(Text, nullable=True)
    additional_info = Column(Text, nullable=True)

    size = Column(String(100), nullable=True)
    color = Column(String(100), nullable=True)

    images = Column(Text, nullable=False)  # required

    seller_name = Column(String(255), nullable=True)

    product_status = Column(String(50), nullable=False)

    vendor_id = Column(Integer, ForeignKey("users.id"))