from config import api
from views.Authentication import (
    GoogleAuth
)


api.add_resource(GoogleAuth, '/api/v1/auth-google')