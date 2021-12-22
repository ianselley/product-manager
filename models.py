import db
from sqlalchemy import Column, Integer, String, Float


class Product(db.Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    stock = Column(Integer, nullable=False)


def get_product(id):
    product = db.session.query(Product).filter_by(id=id).first()
    return product


def get_products():
    products = db.session.query(Product).all()
    return products


def add_product(name, price, category, stock):
    product = Product(name=name, price=price, category=category, stock=stock)
    db.session.add(product)
    db.session.commit()
    return product


def delete_product(id):
    product = db.session.query(Product).filter_by(id=id).first()
    db.session.delete(product)
    db.session.commit()


def edit_product(id, new_name=None, new_price=None, new_category=None, new_stock=None):
    product = db.session.query(Product).filter_by(id=id).first()
    if new_name is not None:
        product.name = new_name
    if new_price is not None:
        product.price = new_price
    if new_category is not None:
        product.category = new_category
    if new_stock is not None:
        product.stock = new_stock
    db.session.commit()
    return product
