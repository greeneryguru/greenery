from flask_wtf.csrf import CSRFProtect
from flask_jwt_extended import JWTManager

csrf = CSRFProtect()
jwt = JWTManager()
