from flask_cors import CORS
from sqlalchemy.orm import DeclarativeBase
from flask_jwt_extended import JWTManager

class BaseSQL(DeclarativeBase):
    pass
jwt = JWTManager()
cors = CORS()