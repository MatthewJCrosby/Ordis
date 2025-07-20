from . import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    product_description = db.Column(db.String(5000), nullable=True)
    product_price = db.Column(db.Numeric(10,2), nullable=False)
    stock = db.Column(db.Integer, nullable=True)
    line_items = db.relationship("LineItem", back_populates="product")
    