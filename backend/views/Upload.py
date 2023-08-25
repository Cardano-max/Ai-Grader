from datetime import datetime, timedelta
from flask_restful import Resource
from flask import request, jsonify, make_response

from src.database.Subscriptions import Subscriptions
from src.database.Users import (
    create_user, check_email_exists,
    create_login_log
)
from src.database.Subscriptions import create_subscription
from config import app,storageManager
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import requests
from src.database.Images import create_image_entry
from uuid import uuid4
from src.utils.image_utils import convert_to_jpg, create_thumb


class UploadImages(Resource):
    @jwt_required()
    def post(self):
        if 1==1:
            identity = get_jwt_identity()
            filedata = request.files.get("file")
            filename = filedata.filename.lower()
            #if check_image_exists(filename):
            #    return jsonify({
            #        "status" : "failed",
            #        "message" : "File already exists"
            #    })

            file_path = "static/temp/" + filename
            filedata.save(file_path)

            new_filename = str(uuid4()) + ".jpg"

            # convert to jpg, if any other extension
            file_path = convert_to_jpg(file_path)
            # upload to storage
            main_file = storageManager.upload_blob_and_return_meta(file_path, "images/" + new_filename, delete=False)
            
            # create thumbnail, replace with orriginal image in local
            create_thumb(file_path)
            # upload thumbail
            thumbnail_file = storageManager.upload_blob_and_return_meta(file_path, "thumbs/" + new_filename, delete=True)
            create_image_entry(identity, new_filename, filename, main_file['url'], thumbnail_file['url'])

            return jsonify({
                "status" : "success",
                "message" : "File uploaded successfully"
            })
        # except Exception as err:
        #     print("Error: ", err)
        #     retJson = {
        #         "status": "error",
        #         "message": str(err)
        #     }
        #     return jsonify(retJson)