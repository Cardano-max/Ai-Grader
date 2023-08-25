# Authentication Routes for Login, Signup, and Logout
from datetime import datetime, timedelta
from flask_restful import Resource
from flask import request, jsonify, make_response

from src.database.Images import Images as ImagesTbl
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from src.database.Subscriptions import create_subscription
from config import app
import requests



class Images(Resource):
    @jwt_required()
    def get(self):
        """
        Google Auth API
        """
        identity = get_jwt_identity()
        images = ImagesTbl.query.order_by(ImagesTbl.created_at).filter(ImagesTbl.user_id==identity).all()
        
        images_data = []
        for img in images:
            images_data.append({
                'id' : img.id, 'name' : img.name, 'original_name' : img.original_name,
                'created_at' : str(img.created_at), 'thumbnail' : img.thumbnail, "graded" : img.gradings != None
            })


        return make_response(jsonify(images_data), 200)