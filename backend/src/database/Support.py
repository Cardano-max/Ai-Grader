from src.database.db_model import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy import func
from datetime import datetime


class Support(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    name = Column(String(100))
    email = Column(String(100), nullable=False)
    subject = Column(String(500), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    

def create_support_entry(user_id, name, email, subject, message):
    """ Create a support entry 
    """
    try:
        # create support object
        sp = Support(
            user_id=user_id,
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        db.session.add(sp)
        db.session.commit()
        return sp
    except Exception as err:
        print(err)
        return False