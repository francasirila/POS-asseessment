from pos.models.product import Product
from sqlalchemy.orm import Session


class ProductRepository:
    def __init__(self):
        self.model =Product


    def get(self, db:Session, id:int):
        return db.get(Product, id)


    def get_all(self, db:Session):
        products = db.querry(Product).all()


    def create(self, db:Session, data:dict):
        product = Product(**data)
        db.commit()
        db.refresh(product)
        return Product

