# 必要なパッケージを取得
from flask import Flask

# Flaskアプリケーションの作成
app = Flask(__name__)

# 「config.py」を設定ファイルとして扱う
app.config.from_object('config')

# views.pyをインポート
from app.views import main
