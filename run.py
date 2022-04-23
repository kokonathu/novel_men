# 「__init__.py」で宣言した変数appを取得
from app import app

# アプリケーションの起動
if __name__ == '__main__':
    app.run(debug=True)