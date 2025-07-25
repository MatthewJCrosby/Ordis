from . import db

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    customer = db.relationship("Customer", back_populates="orders")
    line_items = db.relationship("LineItem", back_populates="order")
    service_requests = db.relationship("ServiceRequest", back_populates="order") 