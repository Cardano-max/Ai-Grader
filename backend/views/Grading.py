# Authentication Routes for Login, Signup, and Logout
from datetime import datetime, timedelta
from flask_restful import Resource
from flask import request, jsonify, make_response

from src.database.Users import Users
from src.database.Images import Images, update_image_by_id
from config import storageManager, app
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from src.utils.mlutils import process_image
import json
import os
from src.utils.generate_report import get_report
os.makedirs("static/temp", exist_ok=True)


classNames = {
    "cws_objects" : "Cotton Wool Spots",
    "ex_objects" : "Exudates",
    "h_objects" : "Hemorrhages"
}

class Grade(Resource):
    @jwt_required()
    def get(self):
        """
        Assessment data
        """
        identity = get_jwt_identity()
        try:
            image_id = request.args.get("image_id")
            img = Images.query.filter_by(id=image_id).one()
            

            if img.gradings == None:
                print("No gradings found")
                resp = process_image(img.url)
                update_image_by_id(img.id, {"gradings" : resp})
                img = Images.query.filter_by(id=image_id).one()

            gradings_data = []
            if img.gradings:
                my_dict = img.gradings.get("detections")
                for key in ['h_objects', 'ex_objects', 'cws_objects']:
                    for point in my_dict[key]:

                        gradings_data.append({
                            'class' : classNames.get(key),
                            "visible": True,
                            "handles": {
                                "start": {
                                "x": point[0],
                                "y": point[1],
                                },
                                "end": {
                                "x": point[2],
                                "y": point[3],
                                },
                                "initialRotation": 0,
                    },
                    "uuid": "c77922bd-0e12-4591-bab4-7a00d9d37a6b",
                    })

            return make_response(jsonify({
                'id' : img.id, 'name' : img.name, 'original_name' : img.original_name,
                'created_at' : str(img.created_at), 'thumbnail' : img.thumbnail, 'url' : img.url,
                "gradings" : img.gradings, 'markings' : {"data" : gradings_data}
                
            }), 200)
        except Exception as ex:
            return make_response(str(ex), 400)


class CreateReport(Resource):
    def get(self):
        """
        Returns assessments
        """
        try:
            image_id = request.args.get("image_id")
            img = Images.query.filter_by(id=image_id).one()

            img_path = f"{img.name}"
            storageManager.download_blob(f"masked/{img.name.replace('.jpg', '.png')}", img_path)

            report = get_report([
                                    {"type" : "image", "path" : img_path},
                                    {"type" : "text", "text" : f"CDR {img.gradings.get('cdr')}" + "\n" + f"Cotton Wool Spots {img.gradings.get('detections', {}).get('num_cws')}" +
                                      f"\nExudates {img.gradings.get('detections', {}).get('num_ex')}" +  f"\nHemorrhages {img.gradings.get('detections', {}).get('num_h')}"
                                     },
                                    {"type" : "image", "path" : img_path},
                                    {"type" : "text", "text" : f"CDR {img.gradings.get('cdr')}" + "\n" + f"Cotton Wool Spots {img.gradings.get('detections', {}).get('num_cws')}" +
                                      f"\nExudates {img.gradings.get('detections', {}).get('num_ex')}" +  f"\nHemorrhages {img.gradings.get('detections', {}).get('num_h')}"
                                     },
                                ])
            
            url = storageManager.upload_blob_and_return_meta(report, "reports", delete=True, random_name=True)
            if os.path.exists(img_path):
                os.remove(img_path)
            return make_response(url, 200)
        except Exception as ex:
            return make_response(str(ex), 400)


