from src.database.db_model import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy import func
from datetime import datetime



class GradeData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grader_id = db.Column(db.Integer)
    image_id = db.Column(db.Integer)
    status = db.Column(db.Boolean, default=None)
    mlstatus = db.Column(db.Boolean, default=False)
    quality_check = db.Column(db.Boolean, default=None)
    vessel_check = db.Column(db.Boolean, default=None)
    save_type = db.Column(db.String(20), default="submit")
    grade_json = db.Column(db.JSON, default=None)
    selected_index = db.Column(db.Integer, default=None)
    
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now())


def create_grading_entry(user_id, image_id, submission_type, grade_json = {}):
    submission_type = submission_type.lower()
    new_entry = GradeData(grader_id=user_id, image_id=image_id, 
                          save_type=submission_type, grade_json = grade_json)
    db.session.add(new_entry)
    db.session.commit()
    return {"status" : "success", "id": new_entry.id}