# 必要なパッケージを取得
import os
from pathlib import Path

SECRET_KEY = 'secret_key'

DEBUG = True

UPLOAD_FOLDER = "UPLOAD_FOLDER"

poppler_dir = Path(__file__).parent.absolute() / "poppler/bin"
os.environ["PATH"] += os.pathsep + str(poppler_dir)