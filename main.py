from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime
import databases
import sqlalchemy
from hashlib import sha256
from typing import List
import pandas as pd
from fastapi.responses import HTMLResponse, JSONResponse






DATABASE_URL = "sqlite:///store_database.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


users = sqlalchemy.Table('users', metadata,
sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
sqlalchemy.Column('name', sqlalchemy.String(50)),
sqlalchemy.Column('surname', sqlalchemy.String(70)),
sqlalchemy.Column('email', sqlalchemy.String(128)),
sqlalchemy.Column('password', sqlalchemy.String(129)),)

products = sqlalchemy.Table('products', metadata,
sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
sqlalchemy.Column('name_prod', sqlalchemy.String(30)),
sqlalchemy.Column('discription', sqlalchemy.String(1000)),
sqlalchemy.Column('price', sqlalchemy.Float),)

orders = sqlalchemy.Table('orders', metadata,
sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
sqlalchemy.Column('user_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id')),
sqlalchemy.Column('prod_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('products.id')),
sqlalchemy.Column('status_order', sqlalchemy.Boolean, default=True),
sqlalchemy.Column('created_at', sqlalchemy.TIMESTAMP, default=datetime.utcnow),)



engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)
app = FastAPI()

class User(BaseModel):
    id: int 
    name: str = Field(..., title='Name', max_length=50)
    surname: str = Field(..., title='Surname', max_length=70)
    email: str = Field(..., title='Email', max_length=128 ) 
    password: str = Field(..., title='Password', min_length=5)
   
   
    def __repr__(self):
        return f'User({self.name}, {self.surname},{self.email})'

    

class UserIn(BaseModel):
    name: str = Field(..., title='Name', max_length=50)
    surname: str = Field(..., title='Surname', max_length=70)
    email: str = Field(..., title='Email', max_length=128 ) 
    password: str = Field(..., title='Password', min_length=7)

class Product(BaseModel):
    id: int
    name_prod: str = Field(..., title='Name_products', max_length=30)
    discription: str = Field(default=None, title='Discription', max_length=1000)
    price: float = Field(..., title='Price', gt=0, le=100000)
  

class ProductIn(BaseModel):
    name_prod: str = Field(..., title='Name_products', max_length=30)
    discription: str = Field(default=None, title='Discription', max_length=1000)
    price: float = Field(..., title='Price', gt=0, le=100000)


class Order(BaseModel):
    id: int
    user_id: int
    prod_id: int
    status_order: bool
    created_at:datetime

class OrderIn(BaseModel):
    user_id: int
    prod_id: int
    status_order: bool
    created_at: datetime

@app.on_event('startup')
async def startup():
    await database.connect()

@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    # query = users.insert().values(**user.dict())
    query = users.insert().values(name=user.name, surname=user.surname, email=user.email, password=sha256(user.password.encode(encoding='utf-8')).hexdigest())
    last_record_id = await database.execute(query)
    return{**user.dict(), 'id': last_record_id}

@app.get("/users/", response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)

@app.get("/user/{user_id}", response_class=JSONResponse)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return  await database.fetch_one(query)


@app.put('/user/{user_id}', response_class=JSONResponse)
async def update_user(user_id: int, user: UserIn):
    query = users.update().where(users.c.id == user_id).values(name=user.name, surname=user.surname, email=user.email, password=sha256(user.password.encode(encoding='utf-8')).hexdigest())
    await database.execute(query)
    return {"name": user.name, "surname":user.surname, "email": user.email,"id": user_id}

@app.delete('/user/{user_id}', response_class=JSONResponse)
async def del_us(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'messge': 'User deleted'}


@app.post("/products/",response_model=Product)
async def create_product(product: ProductIn):
    query = products.insert().values(**product.dict())
    last_record_id = await database.execute(query)
    return {'id': last_record_id, **product.dict()}



@app.get("/products/", response_model=List[Product])
async def show_products():
    query = products.select()
    return await database.fetch_all(query)

@app.get("/product/{product_id}", response_model=Product)
async def show_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    return await database.fetch_one(query)


@app.put('/product/{product_id}', response_model=Product)
async def update_product(product_id: int, product: ProductIn):
    query = products.update().where(products.c.id == product_id).values(**product.dict())
    await database.execute(query)
    return {'id': product_id,'name_prod': product.name_prod,'discription': product.discription, 'price': product.price}

@app.delete('/product/{product_id}')
async def del_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    await database.execute(query)
    return {"message": "Product deleted"}



@app.post("/order/",response_model=Order)
async def add_order(order: OrderIn):
    query = orders.insert().values(**order.dict())
    last_record_id = await database.execute(query)
    return {"id": last_record_id, **order.dict()}


@app. get('/orders/', response_model=List[Order])
async def show_orders():
    query = orders.select()
    return await database.fetch_all(query)


@app.get('/orders/{order_id}', response_model=Order)
async def show_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)


@app.put('/orders/{order_id}', response_model=Order)
async def update_order(order_id: int, order: OrderIn):
    query = orders.update().where(orders.c.id == order_id).values(**order.dict())
    last_record_id = await database.execute(query)
    return {"id": last_record_id, **order.dict()}


@app.delete('/orders/{order_id}')
async def del_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return{"message": "Order deleted"}