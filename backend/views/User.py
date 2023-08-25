# Authentication Routes for Login, Signup, and Logout
from datetime import datetime, timedelta
from flask_restful import Resource
from flask import request, jsonify, make_response

from src.database.Users import Users


from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required


# Refresh Token
class UserData(Resource):
    @jwt_required()
    def get(self):
        """ 
        Refresh Token API
        ---
        swagger_from_file: static/swagger/user/data.yml
        """
        identity = get_jwt_identity()
        
        user = Users.query.get(identity)

        
        return make_response(jsonify({
            "status" : "success",
            "data" : {
                "full_name" : user.fullname,
                'profile_pic' : user.profile_pic,
                "username" : user.username,
                "id" : identity,
                "email" : user.email,
                "created_at" : user.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
        }), 200)
