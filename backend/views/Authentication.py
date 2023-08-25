# Authentication Routes for Login, Signup, and Logout
from datetime import datetime, timedelta
from flask_restful import Resource
from flask import request, jsonify, make_response

from src.database.Subscriptions import Subscriptions
from src.database.Users import (
    create_user, check_email_exists,
    create_login_log
)
from src.database.Subscriptions import create_subscription
from config import app
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
import requests



class GoogleAuth(Resource):
    def post(self):
        """
        Google Auth API
        """
        auth_data = request.get_json()

        user_data = requests.get('https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=' + auth_data.get("access_token"))
        
        if user_data.status_code != 200:
            return make_response(jsonify({"message" : "Invalid Token"}), 400)
        
        user_data = user_data.json()
        
        user = check_email_exists(user_data.get("email"))
        if not user:
            user = create_user(user_data.get('name'), user_data.get('email'), user_data.get("id"), user_data.get('picture'))
            
        # generate token
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

       

        user_data = {
            'id': user.id,
            'accessToken': access_token,
            'refreshToken': refresh_token,
            "fullName" : user.fullname,
            "username" : user.username,
            "role" : user.role,
            "email" : user.email,
            'profile_pic' : user.profile_pic
        }


        create_login_log(user.email, '') # success

        return make_response(jsonify(user_data), 200)