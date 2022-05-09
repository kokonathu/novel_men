
# from flask import render_template,request,url_for,session,redirect,flash,Response,make_response
# from app import app
import os
from PIL import Image
from pdf2image import convert_from_path
import copy


"""

"""

# 定数
up_folder = 'UPLOAD_FOLDER'
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