
from flask import render_template,request,url_for,session,redirect,flash,Response,make_response
from app import app
import fitz
import os
from PIL import Image
import io
import os
from pathlib import Path
from pdf2image import convert_from_path,convert_from_bytes
import glob
import shutil
# ファイル名をチェックする関数
from werkzeug.utils import secure_filename


"""

"""

up_folder = app.config['UPLOAD_FOLDER']
pdf_name = "original.pdf"
image_forder = "png_list"
img_extension = ".png"

def PDF_to_img():
    # pdfから画像に変換
    pages = convert_from_path(os.path.join(up_folder, pdf_name))

    return pages

def pages_plus(left, right):
    """画像の横結合
        left:左のページ
        right:右のページ

    return:
        結合済み画像データ
    """
    # ２つの画像を開く
    im_bef1 = left
    im_bef2 = right
    # 結合後の画像の「枠」を作成
    im_aft = Image.new('RGB',((im_bef1.width + im_bef2.width),max(im_bef1.height,im_bef2.height)))
    # 「枠」に1つ目の画像を貼り付け
    im_aft.paste(im_bef1,(0,0))
    # 「枠」に2つ目の画像を貼り付け
    im_aft.paste(im_bef2,(im_bef1.width,0))

    return im_aft

def temp_plus(temp, page):
    """テンプレート結合
        temp:テンプレート
        page:ページ（結合済み）

    return
        テンプレ結合済みデータ
    """
    # 結合後の画像の「枠」を作成
    im_aft = Image.new('RGB',(temp.width, temp.height))
    # 「枠」に1つ目の画像を貼り付け
    im_aft.paste(temp,(0,0))

    # 張り付け点計算
    height_p:int = (temp.height - page.height)/2
    width_p:int = (temp.width - page.width)/2

    # 「枠」に2つ目の画像を貼り付け
    im_aft.paste(page,(width_p,height_p))

    return im_aft

def resize(images, size):
    """一括画像サイズ変換
        images:画像リスト
        size:(width, height)

    return
        サイズ変換済み画像データリスト
    """

    img_resize = []

    for img in images:
        img_resize.append(img.resize(size, Image.LANCZOS))

    return img_resize

#-----------------------------------------

#ページ表示
@app.route('/', methods=["POST","GET"])
def main():
    return render_template('main.html')

#ページ表示
@app.route('/create_two', methods=["POST"])
def create_two():

    file_data=None
    response=None

    try:
        # if 'file_data' in request.files and request.files["file_data"]:
        file_data = request.files["file_data"]

        # ファイルの保存
        file_data.save(os.path.join(up_folder, pdf_name))
        # 画像のリストに変換、格納
        print("PDF_to_img start")
        pages = PDF_to_img()

        if len(pages) % 4 != 0:
            raise TypeError("ページ数は4の倍数にしてください")

        # ページ数取得
        i :int= 1
        x :int= 0
        y :int= len(pages) - 1

        # img用フォルダ作成
        os.makedirs(os.path.join(up_folder, image_forder), exist_ok=True)

        while y >= x:
            # 表
            img_A = pages_plus(pages[x],pages[y])
            name_A = str(i).zfill(3) + img_extension
            print(name_A)
            img_A.save(os.path.join(up_folder, image_forder, name_A))
            # 裏
            img_B = pages_plus(pages[x+1],pages[y-1])
            name_B = str(i+1).zfill(3) + img_extension
            img_B.save(os.path.join(up_folder, image_forder, name_B))

            x = x + 2
            y = y - 2
            i = i + 2

        # zipfile
        shutil.make_archive('png_data', format='zip', root_dir=os.path.join(up_folder, image_forder))

        # zipダウンロード（切り出してボタン押下時にダウンロードさせる処理作ってもいい）
        response = make_response()
        response.data  = open('png_data.zip', "rb").read()
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers['Content-Disposition'] = 'attachment; filename=png_data.zip'

        # 不要になったファイル削除
        os.remove(os.path.join(up_folder, pdf_name)) #PDF
        os.remove('png_data.zip') #zip
        shutil.rmtree(os.path.join(up_folder, image_forder)) #imageのフォルダ
        
    except Exception as e:
        flash(str(e), "error")
        return render_template('main.html')

    return response


