# 必要なパッケージを取得
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# db定義
db = SQLAlchemy()

import lib.model

def init_db(app):
    db.init_app(app)
    Migrate(app, db)