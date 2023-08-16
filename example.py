import os
from app import app

class Config:
    SECRET_KEY = "test-secret"

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '') or "postgresql://<<user>>:<<password>>@<<host>>:<<port>>/postgres"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CATEGORY_UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'img', 'category')
    PRODUCT_UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'img', 'product')