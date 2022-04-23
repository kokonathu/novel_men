# 必要なパッケージを取得
import os

SQLALCHEMY_DATABASE_URI = 'sqlite:///fgo_DB.sqlite3'

# SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{password}@{host}/fgo'.format(**{
#  'user':os.getenv('DB_USER', 'postgres'),
#  'password':os.getenv('DB_PASSWORD', 'postgres'),
#  'host':os.getenv('DB_HOST', 'localhost:5432'),
# })

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'secret_key'