from . import db

class LineItem(db.Model):
    __tablename__ = 'line_items'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    product = db.relationship("Product", back_populates="line_items")
    price = db.Column(db.Numeric(10,2), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    order = db.relationship("Order", back_populates="line_items")
