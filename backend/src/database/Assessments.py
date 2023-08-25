from src.database.db_model import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy import func
from datetime import datetime, timedelta
import enum
from sqlalchemy import desc

class Assessments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    context_country=db.Column(db.String(20))
    context_curriculum=db.Column(db.Text)
    context_subject=db.Column(db.Text)
    context_year_level=db.Column(db.Text)
    work_sample = db.Column(db.Text)
    criteria = db.Column(db.Text)
    evaluation_response = db.Column(db.Text)
    model = db.Column(db.String(20))
    token_count = db.Column(db.Integer)
    checks=db.Column(db.JSON)
    feedback=db.Column(db.String(10))
    max_tokens = db.Column(db.Integer)
    temperature = db.Column(db.Float)
    top_p = db.Column(db.Float)
    frequency_penalty = db.Column(db.Float)
    presence_penalty = db.Column(db.Float)
    score = db.Column(db.Integer, nullable=True)
    response_status = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=func.now())
    files = db.Column(db.JSON, default=None)
    
    student_name = db.Column(db.String(70))
    course_title = db.Column(db.String(70))
    assessment_title = db.Column(db.String(150))

    def to_json(self):
        return {
            'id': self.id,
            'user_id' : self.user_id,
            'context_country' : self.context_country,
            'context_curriculum' : self.context_curriculum,
            'context_subject' : self.context_subject,
            'context_year_level' : self.context_year_level,
            'criteria' : self.criteria,
            'work_sample': self.work_sample,
            'evaluation_response': self.evaluation_response,
            'model' : self.model,
            'token_count' : self.token_count,
            'max_tokens' : self.max_tokens,
            'temperature' : self.temperature,
            'top_p' : self.top_p,
            'score': self.score,
            'response_status': self.response_status,
            'created_at': str(self.created_at),
            'checks': self.checks,
            'files' : self.files,

            'student_name' : self.student_name,
            'course_title' : self.course_title,
            'assessment_title' : self.assessment_title
        }
    


def get_grouped_assessments(user_id=None):
    """
    Get assessments grouped and in a list where there will is key "title", which seperates each group
    """
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)
    this_month_start = datetime(today.year, today.month, 1).date()
    last_month_end = this_month_start - timedelta(days=1)
    last_month_start = datetime(last_month_end.year, last_month_end.month, 1).date()

    assessments = Assessments.query
    if user_id:
        assessments = assessments.filter_by(user_id=user_id)
    assessments = assessments.order_by(desc(Assessments.created_at)).all()

    assessments_grouped = {
        'Today': [],
        'Yesterday': [],
        'This Month': [],
        'Last Month': [],
        'All Time' : []
    }
    for assessment in assessments:
        created_at = assessment.created_at.date()
        assessment_json = {
            'id' : assessment.id,
            'criteria' : assessment.criteria,
            'created_at' : str(assessment.created_at),
            'token_count' : assessment.token_count,
            'temperature' : assessment.temperature,
            'student_name' : assessment.student_name,
            'course_title' : assessment.course_title,
            'assessment_title' : assessment.assessment_title,
        }
        if created_at == today:
            assessments_grouped['Today'].append(assessment_json)
        elif created_at == yesterday:
            assessments_grouped['Yesterday'].append(assessment_json)
        elif created_at >= this_month_start and created_at <= today:
            assessments_grouped['This Month'].append(assessment_json)
        elif created_at >= last_month_start and created_at <= last_month_end:
            assessments_grouped['Last Month'].append(assessment_json)
        else:
            assessments_grouped['All Time'].append(assessment_json)

    final_grouped = []
    for key in ['Today', 'Yesterday', 'This Month', 'Last Month', 'All Time']:
        if len(assessments_grouped[key]) == 0: continue
        #final_grouped.append({
        #    'title' : key, "rows" : assessments_grouped[key]
        #})
        final_grouped.append({
            'title' : key
        })
        final_grouped += assessments_grouped[key]
    return final_grouped