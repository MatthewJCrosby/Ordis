from . import db

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.Integer, nullable=True)
    
    orders = db.relationship("Order", back_populates="customer", cascade="all, delete")
    service_requests = db.relationship("ServiceRequest", back_populates="customer")
    