from src.database.db_model import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy import func
from datetime import datetime


class Users(db.Model):

    id = Column(Integer, primary_key=True)
    google_id = Column(String(50), unique=True)
    fullname = Column(String(100))
    email = Column(String(100), unique=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    status = Column(String(100), nullable=False, default='approved')
    profile_pic = Column(String(200), default=None)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now())
    role = Column(String(100), nullable=False, default="user")


def create_user(name, email, google_id, profile_pic):
    """ Create a new user 
    
    Args:
        email (str): user email
        password (str): user password
        status (str): user status (pending, active, inactive)
    Returns:
        user (obj): user object
    """
    try:
        # create username from email
        username = "{}-{}".format(email.split("@")[0], str(datetime.now().microsecond))
        # create user object
        user = Users(
            google_id=google_id,
            fullname=name,
            email=email,
            username=username,
            profile_pic=profile_pic
        )
        db.session.add(user)
        db.session.commit()
        return user
    except Exception as err:
        print(err)
        return False


def check_email_exists(email):
    """
    Check if email already exists
    Args:
        email (str): user email
    Returns:
        Boolean: User if exists, None if not
    """
    # check if user already exists
    user = Users.query.filter_by(email=email).first()
    return user if user else False






class LoginLog(db.Model):
    """ Login log table """
    id = Column(Integer, primary_key=True)
    email = Column(String(100), nullable=False)
    ip_address = Column(String(16), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    success = Column(Boolean, nullable=False)


def create_login_log(email, ip_address, success=True):
    """ Create a login log for user
    Args:
        email (str): user email
        ip_address (str): user ip address
    Returns:
        Boolean: True if success, False if not
    """
    try:
        new_entry = LoginLog(
            email=email,
            ip_address=ip_address,
            success=success
        )

        db.session.add(new_entry)
        db.session.commit()
        return True
    except Exception as err:
        return False