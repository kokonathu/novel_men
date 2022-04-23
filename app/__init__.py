# 必要なパッケージを取得
from flask import Flask
from lib.db import init_db

# Flaskアプリケーションの作成
app = Flask(__name__)

# 「config.py」を設定ファイルとして扱う
app.config.from_object('lib.config')

# dbの設定
init_db(app)

# views.pyをインポート
from app.views import savant
