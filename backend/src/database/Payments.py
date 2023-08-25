from src.database.db_model import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy import func, desc
from datetime import datetime, timedelta
import enum

from sqlalchemy import func

class Payments(db.Model):
    id = Column(db.Integer, primary_key=True)
    user_id = Column(db.Integer)
    customer_id = Column(db.String(25))
    payment_method_id = db.Column(db.String(40))
    payment_id = Column(db.String(50))
    status = Column(db.String(50))
    amount = Column(db.Double, default=0)
    payload = Column(db.JSON)
    created_at = Column(db.DateTime, nullable=False, server_default=func.now())

    def to_json(self):
        return {
            'id': self.id,
            'user_id' : self.user_id,
            'payment_id' : self.payment_id,
            'customer_id' : self.customer_id,
            'status' : self.status,
            'amount' : self.amount,
            'payload' : self.payload,
            'payment_method_id' : self.payment_method_id,
            'created_at': self.created_at.strftime("%a, %B %d %Y"),
        }
    


def create_payment(user_id, payment_id, customer_id, payment_method_id, amount, status, payload):
    """ Create a new payment entry
    """
    try:
        # create payment object
        user = Payments(
            user_id = user_id, payment_id=payment_id, amount=amount, payment_method_id=payment_method_id, status=status, payload=payload, customer_id=customer_id
        )
        db.session.add(user)
        db.session.commit()
        return user
    except Exception as err:
        print(err)
        return False
    

def get_total_amount(user_id):
    total_amount = func.sum(Payments.amount)

    query = Payments.query.filter_by(user_id=user_id).with_entities(total_amount).scalar()
    return query


def get_user_payments(user_id):
    query = Payments.query.filter_by(user_id=user_id).order_by(desc(Payments.created_at)).all()
    return query


def get_last_payment(user_id):
    try:
        return Payments.query.filter_by(user_id=user_id).order_by(desc(Payments.created_at)).first()
    except:
        return None