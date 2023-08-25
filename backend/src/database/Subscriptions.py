from src.database.db_model import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy import func
import enum
from datetime import datetime
from sqlalchemy import update


class Subscriptions(db.Model):
    class APIAccess(enum.Enum):
        active = 'active'
        paused = 'paused'

    class ServicePlan(enum.Enum):
        free = 'free'
        paid = 'paid'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    customer_id = db.Column(db.String(25))
    subscription_id = db.Column(db.String(40))
    payment_method_id = db.Column(db.String(40), default=None)
    status = db.Column(db.String(20))
    quota = db.Column(db.Integer, default=5)
    remaining_quota = db.Column(db.Integer, default=5)
    api_access = db.Column(db.Enum(APIAccess),
        default=APIAccess.paused,
        nullable=False)
    service_plan = db.Column(db.Enum(ServicePlan),
        default=ServicePlan.free,
        nullable=False)
    
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    
    lifetime_paid = db.Column(db.Double, default=0)
    last_payment_date = db.Column(db.DateTime, nullable=False, server_default=func.now())
    next_payment_date = db.Column(db.DateTime, nullable=False, server_default=func.now())


    def to_json(self):
        return {
            'id': self.id,
            'quota' : self.quota,
            'api_access' : str(self.api_access).split(".")[-1],
            'service_plan' : str(self.service_plan).split(".")[-1],
            'payment_method_id' : self.payment_method_id,
            'remaining_quota' : self.remaining_quota,
            'customer_id' : self.customer_id,
            'subscription_id' : self.subscription_id,
            'status' : self.status,
            'lifetime_paid' : self.lifetime_paid,
            'last_payment_date' : self.last_payment_date.strftime("%b %d, %Y"),
            'next_payment_date' : self.next_payment_date.strftime("%b %d, %Y")
        }
    



def create_subscription(user_id, quota=5):
    """ Create a new subscription 
    
    Args:
        user_id (int): user id
        quota (int): quota
    Returns:
        subscription (obj): subscription object
    """
    try:
        # create a subscription object
        sub = Subscriptions(
            user_id=user_id,
            quota = quota,
            remaining_quota=quota
        )
        db.session.add(sub)
        db.session.commit()
        return sub
    except Exception as err:
        print(err)
        return False



def update_remaining_quota(user_id):
    """
    Subtract 1 from remaining quota
    """
    stmt = (
        update(Subscriptions)
        .where(Subscriptions.user_id == user_id)
        .values(remaining_quota=Subscriptions.remaining_quota - 1)
    )
    db.session.execute(stmt)
    db.session.commit()


def get_subscription_json(user_id):
    return Subscriptions.query.filter_by(user_id=user_id).first().to_json()


def update_subscription(sub_id, payload):
    Subscriptions.query.filter_by(id = sub_id).update(payload)
    db.session.commit()


def subscription_by_sub_id(sub_id):
    try:
        return Subscriptions.query.filter_by(subscription_id=sub_id).first()
    except Exception as ex:
        return None