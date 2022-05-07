
from flask import render_template,request,url_for,session,redirect,flash,Response,make_response
from app import app
import os
from PIL import Image
import os
from pathlib import Path
from pdf2image import convert_from_path
import shutil
import copy


"""

"""

# 定数
up_folder = app.config['UPLOAD_FOLDER']
pdf_name = "original.pdf"
image_forder = "png_list"
img_extension = ".png"
temp_name = "temp.png"

def PDF_to_img():
    # pdfから画像に変換
    pages = convert_from_path(os.path.join(up_folder, pdf_name), dpi=350)

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

def pages_plus_height(over, under):
    """画像の縦結合
        over:上のページ
        under:下のページ

    return:
        結合済み画像データ
    """
    # ２つの画像を開く
    im_bef1 = over
    im_bef2 = under
    # 結合後の画像の「枠」を作成
    im_aft = Image.new('RGB',(max(im_bef1.width,im_bef2.width),(im_bef1.height + im_bef2.height)))
    # 「枠」に1つ目の画像を貼り付け
    im_aft.paste(im_bef1,(0,0))
    # 「枠」に2つ目の画像を貼り付け
    im_aft.paste(im_bef2,(0,im_bef1.height))

    return im_aft

def temps_plus(temp, pages):
    """テンプレート結合
        temp:テンプレート
        pages:ページ（結合済み）リスト

    return
        テンプレ結合済みデータリスト
    """
    return_pages = {}

    # 結合後の画像の「枠」を作成
    im_aft = Image.new('RGB',(temp.width, temp.height))

    for name, page in pages.items():
        im_aft_copy = copy.deepcopy(im_aft)
        # 張り付け点計算
        height_p:int = (temp.height - page.height)//2
        width_p:int = (temp.width - page.width)//2
        # 「枠」に1つ目の画像を貼り付け
        im_aft_copy.paste(temp,(0,0))
        # 「枠」に2つ目の画像を貼り付け
        im_aft_copy.paste(page,(width_p,height_p))
        return_pages[name] = im_aft_copy

    return return_pages

def resize(images:list, size:tuple):
    """一括画像サイズ変換
        images:画像リスト
        size:(width, height)

    return
        サイズ変換済み画像データリスト
    """

    for img in images:
        img = img.resize(size, Image.LANCZOS)

    # for name, img in images.items():
    #     images[name] = img.resize(size, Image.LANCZOS)

    return images

def two_men(pages):
    """二面面付け
        pages:画像リスト

    return
        結合済み画像の辞書
    """

    image_list = {}

    # ページ数取得
    i :int= 1
    x :int= 0
    y :int= len(pages) - 1


    while y >= x:
        # 表
        img_A = pages_plus(pages[x],pages[y])
        name_A = str(i).zfill(3) + img_extension
        image_list[name_A] = img_A

        # 裏
        img_B = pages_plus(pages[y-1],pages[x+1])
        name_B = str(i+1).zfill(3) + img_extension
        image_list[name_B] = img_B

        x = x + 2
        y = y - 2
        i = i + 2

    return image_list

def ito_men(pages,oricho):
    """糸綴じ複数折用二面面付け
        pages:画像リスト
        oricho:一つの折丁のページ数

    return
        結合済み画像の辞書
    """

    image_list = {}

    # ページ数取得
    i :int= 1
    x :int= 0
    y :int= len(pages) - 1

    count = y / oricho

    while count > 0:

        oricho_x = x
        oricho_y = x + oricho - 1

        while oricho_y >= oricho_x:
            # 表
            img_A = pages_plus(pages[oricho_x],pages[oricho_y])
            name_A = str(i).zfill(3) + img_extension
            image_list[name_A] = img_A

            # 裏
            img_B = pages_plus(pages[oricho_y-1], pages[oricho_x+1])
            name_B = str(i+1).zfill(3) + img_extension
            image_list[name_B] = img_B

            oricho_x = oricho_x + 2
            oricho_y = oricho_y - 2
            i = i + 2

        x = x + oricho
        count = count - 1

    return image_list

def four_men(pages):
    """四面面付け
        pages:画像リスト

    return
        結合済み画像の辞書
    """

    image_list = {}

    # ページ数取得
    i :int= 1
    x :int= 0
    y :int= len(pages) - 1


    while y >= x:
        # 表
        img_Aa = pages_plus(pages[x],pages[y])
        img_Ab = pages_plus(pages[x+2],pages[y-2])
        img_A = pages_plus_height(img_Aa,img_Ab)
        name_A = str(i).zfill(3) + img_extension
        image_list[name_A] = img_A

        # 裏
        img_Ba = pages_plus(pages[y-1],pages[x+1])
        img_Bb = pages_plus(pages[y-3],pages[x+3])
        img_B = pages_plus_height(img_Ba,img_Bb)
        name_B = str(i+1).zfill(3) + img_extension
        image_list[name_B] = img_B

        x = x + 4
        y = y - 4
        i = i + 2

    return image_list

def eight_men(pages):
    """8面面付け
        pages:画像リスト

    return
        結合済み画像の辞書
    """

    image_list = {}

    # ページ数取得
    i :int= 1
    x :int= 0
    y :int= len(pages) - 1


    while y >= x:
        # 上
        img_Aa = pages_plus(pages[x],pages[x+7])
        img_Ab = pages_plus(pages[x+6],pages[x+5])
        img_A = pages_plus(img_Aa,img_Ab).rotate(180, expand=True)

        # 下
        img_Ba = pages_plus(pages[x+4],pages[x+3])
        img_Bb = pages_plus(pages[x+2],pages[x+1])
        img_B = pages_plus(img_Ba,img_Bb)

        image = pages_plus_height(img_A,img_B)

        name = str(i).zfill(3) + img_extension
        image_list[name] = image

        x = x + 8
        i = i + 1

    return image_list


#-----------------------------------------

#ページ表示
@app.route('/', methods=["POST","GET"])
def main():

    if request.method == 'GET':
        if os.path.exists('png_data.zip'):
            os.remove('png_data.zip') #zip
        return render_template('main.html')

    file_data=None
    image_list = {}

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

        # 原稿サイズ指定あればresize
        if request.form.get("page_size") != "":
            size = ""
            if request.form.get("page_size") == "A6":
                # size = (2894, 2039) #縦式はデフォルトでこのサイズになるよ
                size = (2039, 1447)
            elif request.form.get("page_size") == "B6":
                # size = (3541, 2508)
                size =  (2508, 1746)

            pages = resize(pages, size)

        # img用フォルダ作成
        os.makedirs(os.path.join(up_folder, image_forder), exist_ok=True)

        # 面付けレイアウト分岐
        if request.form.get("layout") == "":
            image_list = two_men(pages)
        elif request.form.get("layout") == "men_4":
            image_list = four_men(pages)
        elif request.form.get("layout") == "men_8":
            if len(pages) % 8 != 0:
                raise TypeError("ページ数は8の倍数にしてください")
            image_list = eight_men(pages)
        elif request.form.get("layout") == "men_ito":
            oricho = int(request.form.get("ito_page"))
            if oricho == "":
                raise TypeError("一つの折丁を何ページにするか入力してください")
            elif len(pages) % oricho != 0:
                raise TypeError("ページ数は入力した数字の倍数にしてください")
            image_list = ito_men(pages, oricho)

        # テンプレートありなら結合
        if request.form.get("temp_check"):
            if request.files["template_img"].filename != "" and request.files["template_img"].filename is not None:
                tenp_img = request.files["template_img"]
            elif os.path.exists(os.path.join(up_folder, "temp.png")):
                tenp_img = os.path.join(up_folder, "temp.png")
            else:
                raise TypeError("テンプレートを選択してください")

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
