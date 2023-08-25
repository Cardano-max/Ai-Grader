from src.database.db_model import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy import func
from datetime import datetime




class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    original_name = db.Column(db.String(200))
    name = db.Column(db.String(100))
    url = db.Column(db.String(700))
    thumbnail = db.Column(db.String(700))
    gradings = db.Column(JSON, default=None)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now())
    
    
def create_image_entry(user_id, image_name, original_name, url, thumbnail):
    new_entry = Images(user_id=user_id, name=image_name, original_name=original_name, url=url, thumbnail=thumbnail)
    db.session.add(new_entry)
    db.session.commit()
    return new_entry


def update_image_by_id(image_id, payload):
    Images.query.filter_by(id = image_id).update(payload)
    db.session.commit()