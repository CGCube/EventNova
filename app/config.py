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
    TMDB_API_KEY = os.environ.get('TMDB_API_KEY') or 'a59b7e2451a75b9cf11363816cc0a8cd'
    TMDB_READ_ACCESS_TOKEN = os.environ.get('TMDB_READ_ACCESS_TOKEN') or 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhNTliN2UyNDUxYTc1YjljZjExMzYzODE2Y2MwYThjZCIsIm5iZiI6MTczNjc5MjA4Ni4yNDMsInN1YiI6IjY3ODU1ODE2YjkwOTRjN2RmZWJiNDliZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.3d_Fu5pz4-j1wwPiEtFbfRNs6GUIOdbZ1SCJNz0mhi0'