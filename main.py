from fastapi import FastAPI
from database import Base, engine
from routers import auth
from routers.products import vendor_add_product
from fastapi.staticfiles import StaticFiles
from models.user import User, Product


app = FastAPI()

# 🔥 create tables
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(vendor_add_product.router)


app.mount("/static", StaticFiles(directory="static"), name="static")