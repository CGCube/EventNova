import os

db_config = {
    'user': 'root',
    'password': '123456',
    'host': '127.0.0.1',
    'database': 'eventnova'
}

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Removed TMDB configurations