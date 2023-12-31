import os
from app import app

class Config:
    SECRET_KEY = os.environ['SECRET_KEY']

    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CATEGORY_UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'img', 'category')
    PRODUCT_UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'img', 'product')