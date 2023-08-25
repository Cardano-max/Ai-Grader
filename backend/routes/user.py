from config import api
from views.User import (
    UserData
)
from views.Upload import UploadImages
from views.Images import Images
from views.Grading import Grade, CreateReport

api.add_resource(UserData, '/api/v1/user')
api.add_resource(UploadImages, '/api/v1/images/upload')
api.add_resource(Images, '/api/v1/images')
api.add_resource(Grade, '/api/v1/grade')
api.add_resource(CreateReport, '/api/v1/grade/report')