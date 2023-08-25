from src.database.db_model import db
from sqlalchemy import Column
from sqlalchemy import func, desc
from datetime import datetime, timedelta
import enum

from sqlalchemy import func

class StripeLogs(db.Model):
    id = Column(db.Integer, primary_key=True)
    type = Column(db.String(100), default=None)
    payload = Column(db.JSON)
    created_at = Column(db.DateTime, nullable=False, server_default=func.now())

    def to_json(self):
        return {
            'id': self.id,
            'type' : self.type,
            'payload' : self.payload,
            'created_at': self.created_at.strftime("%a, %B %d %Y"),
        }
    


def create_stripe_log(type, payload):
    """ Create a new payment entry
    """
    try:
        # create stripelog object
        stp = StripeLogs(
            type=type, payload=payload
        )
        db.session.add(stp)
        db.session.commit()
        return stp
    except Exception as err:
        print(err)
        return False
