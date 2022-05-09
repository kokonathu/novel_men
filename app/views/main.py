
from flask import render_template,request,url_for,session,redirect,flash,Response,make_response
from app import app
import os
from PIL import Image
from pathlib import Path
from pdf2image import convert_from_path
import shutil
import copy
from rq import Queue
from worker import conn
from ..views.methods import *


"""

"""

# 定数
up_folder = 'UPLOAD_FOLDER'
pdf_name = "original.pdf"
image_forder = "png_list"
img_extension = ".png"
temp_name = "temp.png"

q = Queue(connection=conn)


#-----------------------------------------

#ページ表示
@app.route('/', methods=["POST","GET"])
def main():
    if request.method == 'GET':
        if os.path.exists('png_data.zip'):
            os.remove('png_data.zip') #zip
        return render_template('main.html')

    file_data = request.files["file_data"]
    template_img = request.files["template_img"]
    page_size = request.form.get("page_size")
    layout = request.form.get("layout")
    ito_page = request.form.get("ito_page")
    temp_check = request.form.get("temp_check")
    temp_size = request.form.get("temp_size")

    result = main_sub(
            file_data
            , template_img
            , page_size
            , layout
            , ito_page
            , temp_check
            , temp_size
            )
    return result

    # result = q.enqueue(main_sub(
    #         file_data
    #         , template_img
    #         , page_size
    #         , layout
    #         , ito_page
    #         , temp_check
    #         , temp_size
    #         )
    #     )
    # return result

    # return url_for("main_sub",file_data
    #         , template_img
    #         , page_size
    #         , layout
    #         , ito_page
    #         , temp_check
    #         , temp_size)

def main_sub(
    file_data
    , template_img
    , page_size
    , layout
    , ito_page
    , temp_check
    , temp_size
):

    # if request.method == 'GET':
    #     if os.path.exists('png_data.zip'):
    #         os.remove('png_data.zip') #zip
    #     return render_template('main.html')

    file_data=None
    image_list = {}

    try:
        # if 'file_data' not in request.files or request.files["file_data"] is None:
        #     raise ValueError("ファイルを選択してください")

        file_data = request.files["file_data"]

        # ファイルの保存
        file_data.save(os.path.join(up_folder, pdf_name))

        # 画像のリストに変換、格納
        try:
            pages = PDF_to_img()
        except Exception as e:
            # raise ValueError("PDFファイルを選択してください")
            raise e

        if len(pages) % 4 != 0:
            raise TypeError("ページ数は4の倍数にしてください")

        # 原稿サイズ指定あればresize
        if page_size != "":
            size = ""
            if page_size == "A6":
                # size = (2894, 2039) #縦式はデフォルトでこのサイズになるよ
                size = (2039, 1447)
            elif page_size == "B6":
                # size = (3541, 2508)
                size =  (2508, 1746)

            pages = resize(pages, size)

        # img用フォルダ作成
        os.makedirs(os.path.join(up_folder, image_forder), exist_ok=True)

        # 面付けレイアウト分岐
        if layout == "":
            image_list = two_men(pages)
        elif layout == "men_4":
            image_list = four_men(pages)
        elif layout == "men_8":
            if len(pages) % 8 != 0:
                raise TypeError("ページ数は8の倍数にしてください")
            image_list = eight_men(pages)
        elif layout == "men_ito":
            oricho = int(ito_page)
            if oricho == "":
                raise TypeError("一つの折丁を何ページにするか入力してください")
            elif len(pages) % oricho != 0:
                raise TypeError("ページ数は入力した数字の倍数にしてください")
            image_list = ito_men(pages, oricho)

        # テンプレートありなら結合
        if temp_check:
            if template_img:
                tenp_img = template_img
            elif os.path.exists(os.path.join(up_folder, "temp.png")):
                tenp_img = os.path.join(up_folder, "temp.png")
            else:
                raise TypeError("テンプレートを選択してください")

            tenp_img = Image.open(tenp_img)

            if temp_size != "":
                temp_img_dict = {"img":request.files["template_img"]}
                size = ""
                if temp_size == "B5":
                    size = (3541, 2508)
                elif temp_size == "A4":
                    size = (4093, 2894)

                tenp_img = tenp_img.resize(size, Image.LANCZOS)

            image_list = temps_plus(tenp_img, image_list)

        # 画像として保存
        for name, img in image_list.items():
            img.save(os.path.join(up_folder, image_forder, name))

        # zipfile
        shutil.make_archive('png_data', format='zip', root_dir=os.path.join(up_folder, image_forder))

        # 不要になったファイル削除
        os.remove(os.path.join(up_folder, pdf_name)) #PDF
        shutil.rmtree(os.path.join(up_folder, image_forder)) #imageのフォルダ

    except Exception as e:
        flash(str(e), "error")
        return render_template('main.html')

    return render_template('main.html', make_file=True)

#直接DL
@app.route('/create_two', methods=["POST"])
def create_two():

    file_data=None
    response=None

    try:
        if 'file_data' not in request.files or request.files["file_data"] is None:
            raise ValueError("ファイルを選択してください")

        file_data = request.files["file_data"]

        # ファイルの保存
        file_data.save(os.path.join(up_folder, pdf_name))
        # 画像のリストに変換、格納
        try:
            pages = PDF_to_img()
        except:
            raise ValueError("PDFファイルを選択してください")

        if len(pages) % 4 != 0:
            raise TypeError("ページ数は4の倍数にしてください")

        # ページ数取得
        i :int= 1
        x :int= 0
        y :int= len(pages) - 1

        # img用フォルダ作成
        os.makedirs(os.path.join(up_folder, image_forder), exist_ok=True)

        image_list = {}

        while y >= x:
            # 表
            img_A = pages_plus(pages[x],pages[y])
            name_A = str(i).zfill(3) + img_extension
            image_list[name_A] = img_A

            # 裏
            img_B = pages_plus(pages[x+1],pages[y-1])
            name_B = str(i+1).zfill(3) + img_extension
            image_list[name_B] = img_B

            x = x + 2
            y = y - 2
            i = i + 2

        # 原稿サイズ指定あればresize
        if request.form.get("page_size") != "":
            size = ""
            if request.form.get("page_size") == "A6":
                size = (2894, 2039)
            elif request.form.get("page_size") == "B6":
                size = (3541, 2508)

            image_list = resize(image_list, size)

        # テンプレートありなら結合
        if request.files["template_img"].filename != "" and request.files["template_img"].filename is not None:

            tenp_img = request.files["template_img"]
            tenp_img = Image.open(tenp_img)

            if request.form.get("temp_size") != "":
                temp_img_dict = {"img":request.files["template_img"]}
                size = ""
                if request.form.get("temp_size") == "B5":
                    size = (3541, 2508)
                elif request.form.get("temp_size") == "A4":
                    size = (4093, 2894)

                tenp_img = tenp_img.resize(size, Image.LANCZOS)

            image_list = temps_plus(tenp_img, image_list)

        # 画像として保存
        for name, img in image_list.items():
            img.save(os.path.join(up_folder, image_forder, name))

        # zipfile
        shutil.make_archive('png_data', format='zip', root_dir=os.path.join(up_folder, image_forder))

        # zipダウンロード（切り出してボタン押下時にダウンロードさせる処理作ってもいい）
        response = make_response()
        response.data  = open('png_data.zip', "rb").read()
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers['Content-Disposition'] = 'attachment; filename=png_data.zip'

        # 不要になったファイル削除
        os.remove(os.path.join(up_folder, pdf_name)) #PDF
        shutil.rmtree(os.path.join(up_folder, image_forder)) #imageのフォルダ
        # os.remove('png_data.zip') #zip

    except Exception as e:
        flash(str(e), "error")
        return render_template('main.html')

    return response

@app.route('/download', methods=["POST"])
def download():
    # zipダウンロード（切り出してボタン押下時にダウンロードさせる処理作ってもいい）
    response = make_response()
    response.data  = open('png_data.zip', "rb").read()
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = 'attachment; filename=png_data.zip'

    return response
