
from flask import render_template,request,url_for,session,redirect,flash
from sqlalchemy.sql.expression import null
from lib.model import Savant_list, Sozai, Use_sozai
from app import app
from lib.db import db
#デコレータに使用
from functools import wraps

#or検索
from sqlalchemy import or_


"""
頭イカレてきた
"""

#-----------------------------------------

#一覧表示
@app.route('/', methods=["POST","GET"])
def list_view():

    if request.method == 'GET':
        session.pop('name', None)
        session.pop('class_s', None)
        session.pop('star', None)
        session.pop('hougu_syurui', None)
        session.pop('hougu_color', None)
        session.pop('zokusei_1', None)
        session.pop('zokusei_2', None)
        session.pop('source', None)
        session.pop('country', None)
        session.pop('skill', None)
        session.pop('seihai', None)
        session.pop('kizuna', None)
        session.pop('hougu_lv', None)
        session.pop('sex', None)
        session.pop('input_list', None)
        session.pop('shoukan_list', None)

    # 各種項目取得
    savants = Savant_list.query.filter(Savant_list.day != None).filter(Savant_list.day != "")
    hougu_syuruis = db.session.query(Savant_list).group_by(Savant_list.hougu_syurui).order_by(Savant_list.hougu_syurui.desc())
    hougu_colors= db.session.query(Savant_list).group_by(Savant_list.hougu_color).order_by(Savant_list.hougu_color.asc())
    zokusei_1s = db.session.query(Savant_list).group_by(Savant_list.zokusei_1).order_by(Savant_list.zokusei_1.desc())
    zokusei_2s = db.session.query(Savant_list).group_by(Savant_list.zokusei_2).order_by(Savant_list.zokusei_2.desc())
    sexs = db.session.query(Savant_list).group_by(Savant_list.sex).order_by(Savant_list.sex.desc())

    print(session.get('hougu_syurui'))

    # 召喚状況←必ず最初に
    shoukan_list = request.form.get('shoukan_list') or session.get('shoukan_list') or ""
    if shoukan_list == "shoukan_none":
        savants = Savant_list.query.filter(Savant_list.day == "")
    elif shoukan_list == "shoukan_all":
        savants = Savant_list.query
    session['shoukan_list'] = shoukan_list

    # 名前検索
    name = request.form.get('name') or ""
    if name != "":
        savants = savants.filter(Savant_list.name.like("%" + name + "%"))
    else:
        name = ""
    session['name'] = name

    # クラス名検索
    class_s = request.form.getlist('class_s') or session.get('class_s') or ""
    print(class_s)
    if class_s:
        if not "all" in class_s:   #allが選択されていない
            filters = []    #検索条件を格納する変数
            filters.append(Savant_list.class_s.in_(class_s))  #filtersに検索条件を格納
            savants = savants.filter(or_(*filters))    #or条件に*付きで条件を追加
    session['class_s'] = class_s

    # レアリティ検索
    star = request.form.getlist('star') or session.get('star') or ""
    if star:
        if not "all" in star:   #allが選択されていない
            filters = []    #検索条件を格納する変数
            filters.append(Savant_list.star.in_(star))  #filtersに検索条件を格納
            savants = savants.filter(or_(*filters))    #or条件に*付きで条件を追加
    session['star'] = star

    # 宝具検索1
    hougu_syurui = request.form.get('hougu_syurui') or session.get('hougu_syurui') or "all"
    if  hougu_syurui != "all" and hougu_syurui != "":
        savants = savants.filter(Savant_list.hougu_syurui == hougu_syurui)
    else:
        hougu_syurui = "all"
    session['hougu_syurui'] = hougu_syurui

    # 宝具検索2
    hougu_color = request.form.get('hougu_color') or session.get('hougu_color') or "all"
    if  hougu_color != "all" and hougu_color != "":
        savants = savants.filter(Savant_list.hougu_color == hougu_color)
    else:
        hougu_color = "all"
    session['hougu_color'] = hougu_color

    # 宝具レベル検索
    hougu_lv = request.form.getlist('hougu_lv') or session.get('hougu_lv') or ""
    if hougu_lv:
        if not "all" in hougu_lv:   #allが選択されていない
            filters = []    #検索条件を格納する変数
            filters.append(Savant_list.hougu_lv.in_(hougu_lv))  #filtersに検索条件を格納
            savants = savants.filter(or_(*filters))    #or条件に*付きで条件を追加
    session['hougu_lv'] = hougu_lv

    # 性別検索
    sex = request.form.getlist('sex') or session.get('sex') or ""
    if sex:
        if not "all" in sex:   #allが選択されていない
            filters = []    #検索条件を格納する変数
            for val in sex:
                filters.append(Savant_list.sex.like("%" + val + "%"))  #filtersに検索条件を格納
                if "？" in sex:
                    filters.append(Savant_list.sex.like("%" + "朕" + "%"))
            savants = savants.filter(or_(*filters))    #or条件に*付きで条件を追加
    session['sex'] = sex

    # 属性検索1
    zokusei_1 = request.form.get('zokusei_1') or session.get('zokusei_1') or "all"
    if  zokusei_1 != "all" and zokusei_1 != "":
        savants = savants.filter(Savant_list.zokusei_1 == zokusei_1)
    else:
        zokusei_1 = "all"
    session['zokusei_1'] = zokusei_1
    
    # 属性検索2
    zokusei_2 = request.form.get('zokusei_2') or session.get('zokusei_2') or "all"
    if  zokusei_2 != "all" and zokusei_2 != "":
        savants = savants.filter(Savant_list.zokusei_2 == zokusei_2)
    else:
        zokusei_2 = "all"
    session['zokusei_2'] = zokusei_2

    # 出典検索
    source = request.form.get('source') or ""
    if source != "":
        savants = savants.filter(Savant_list.source.like("%" + source + "%"))
    else:
        source = ""
    session['source'] = source

    # 地域検索
    country = request.form.get('country') or ""
    if country != "":
        savants = savants.filter(Savant_list.country.like("%" + country + "%"))
    else:
        country = ""
    session['country'] = country

    # スキル検索
    skill = request.form.get('skill') or session.get('skill') or "all"
    if  skill == "10":
        savants = savants.filter(Savant_list.skill_1 == 10).filter(Savant_list.skill_2 == 10).filter(Savant_list.skill_3 == 10)
    elif skill == "9":
        savants = savants.filter(Savant_list.skill_1 >= 9).filter(Savant_list.skill_2 >= 9).filter(Savant_list.skill_3 >= 9)
    else:
        skill = "all"
    session['skill'] = skill

    # 聖杯検索
    seihai = request.form.get('seihai') or session.get('seihai') or "all"
    if  seihai == "true":
        savants = savants.filter(Savant_list.seihai > 0)
    elif seihai == "false":
        savants = savants.filter(or_(Savant_list.seihai==None,Savant_list.seihai==0))
    else:
        seihai = "all"
    session['seihai'] = seihai

    # 絆レベル検索
    kizuna = request.form.get('kizuna') or session.get('kizuna') or "all"
    if kizuna == "0~5":
        savants = savants.filter(Savant_list.kizuna < 6)
    elif kizuna == "6~9":
        savants = savants.filter(Savant_list.kizuna >= 6).filter(Savant_list.kizuna < 10)
    elif kizuna == "10~15":
        savants = savants.filter(Savant_list.kizuna >= 10)
    else:
        kizuna == "all"
    session['kizuna'] = kizuna

    #ソート
    if request.form.get('sort'):
        sort = request.form.get('sort')
        
        #すでにソート機能が働いているとき
        if session.get('sort'):
            if session.get('sort') == "name":
                savants = savants.order_by(Savant_list.name.desc())
            if session.get('sort') == "NO":
                savants = savants.order_by(Savant_list.NO.asc())
            if session.get('sort') == "class_s":
                savants = savants.order_by(Savant_list.class_s.desc())
            if session.get('sort') == "star":
                savants = savants.order_by(Savant_list.star.desc())
            if session.get('sort') == "hougu_lv":
                savants = savants.order_by(Savant_list.hougu_lv.desc())
            if session.get('sort') == "skill":
                savants = savants.order_by((Savant_list.skill_1 + Savant_list.skill_2 + Savant_list.skill_3).asc())
            if session.get('sort') == "shincho":
                savants = savants.order_by(Savant_list.shincho.desc())
            if session.get('sort') == "taiju":
                savants = savants.order_by(Savant_list.taiju.desc())
            if session.get('sort') == "day":
                savants = savants.order_by(Savant_list.day.desc())
            if session.get('sort') == "st1":
                savants = savants.order_by(Savant_list.st1.desc())
            if session.get('sort') == "st2":
                savants = savants.order_by(Savant_list.st2.desc())
            if session.get('sort') == "st3":
                savants = savants.order_by(Savant_list.st3.desc())
            if session.get('sort') == "st4":
                savants = savants.order_by(Savant_list.st4.desc())
            if session.get('sort') == "st5":
                savants = savants.order_by(Savant_list.st5.desc())
            if session.get('sort') == "st6":
                savants = savants.order_by(Savant_list.st6.desc())
            if session.get('sort') == "seihai":
                savants = savants.order_by(Savant_list.seihai.desc())
            if session.get('sort') == "kizuna":
                savants = savants.order_by(Savant_list.kizuna.asc())
            session.pop('sort', None)
        else:
            if sort == "name":
                savants = savants.order_by(Savant_list.name.asc())
            if sort == "NO":
                savants = savants.order_by(Savant_list.NO.desc())
            if sort == "class_s":
                savants = savants.order_by(Savant_list.class_s.asc())
            if sort == "star":
                savants = savants.order_by(Savant_list.star.asc())
            if sort == "hougu_lv":
                savants = savants.order_by(Savant_list.hougu_lv.asc())
            if sort == "skill":
                savants = savants.order_by((Savant_list.skill_1 + Savant_list.skill_2 + Savant_list.skill_3).desc())
            if sort == "shincho":
                savants = savants.order_by(Savant_list.shincho.asc())
            if sort == "taiju":
                savants = savants.order_by(Savant_list.taiju.asc())
            if sort == "day":
                savants = savants.order_by(Savant_list.day.asc())
            if sort == "st1":
                savants = savants.order_by(Savant_list.st1.asc())
            if sort == "st2":
                savants = savants.order_by(Savant_list.st2.asc())
            if sort == "st3":
                savants = savants.order_by(Savant_list.st3.asc())
            if sort == "st4":
                savants = savants.order_by(Savant_list.st4.asc())
            if sort == "st5":
                savants = savants.order_by(Savant_list.st5.asc())
            if sort == "st6":
                savants = savants.order_by(Savant_list.st6.asc())
            if sort == "seihai":
                savants = savants.order_by(Savant_list.seihai.asc())
            if sort == "kizuna":
                savants = savants.order_by(Savant_list.kizuna.desc())
            session['sort'] = sort
    else:
        session.pop('sort', None)
        # session['sort'] = "NO"
        savants = savants.order_by(Savant_list.NO.asc())

    # 行数カウント
    count = savants.count()

    return render_template('main_list.html',savants=savants,hougu_syuruis=hougu_syuruis,hougu_colors=hougu_colors,zokusei_1s=zokusei_1s,zokusei_2s=zokusei_2s,sexs=sexs,count=count)

#詳細画面
@app.route('/<int:NO>', methods=["GET"])
def detil_show(NO):
    savant = Savant_list.query.get(NO)

    return render_template('savant_detil.html',savant=savant)

#新規登録
@app.route('/input', methods=["POST","GET"])
def input():

    sozai_list = Sozai.query.order_by(Sozai.id.asc()).all()

    if request.method == 'GET':
        session.pop('up_NO', None)

    if request.form.get('up_NO'):
        session['up_NO'] = request.form.get('up_NO')
    if session.get('up_NO'):
        savant = Savant_list.query.get(session.get('up_NO'))
        use_sozai = Use_sozai.query.get(session.get('up_NO'))
        return render_template('update.html',savant=savant,sozai_list=sozai_list,use_sozai=use_sozai)

    #No自動入力
    max_no_savant = Savant_list.query.order_by(Savant_list.NO.desc()).first()
    max_no = int(max_no_savant.NO) + 1
    input_list = session.get('input_list') or ""
    return render_template('input.html',sozai_list=sozai_list,input_list=input_list,max_no=max_no)

#入力チェック→登録
@app.route('/input_check', methods=["POST"])
def input_check():

    NO = request.form.get('NO') or ""
    name = request.form.get('name') or ""
    class_s = request.form.get('class_s') or ""
    star = request.form.get('star') or ""
    hougu_name_1 = request.form.get('hougu_name_1') or ""
    hougu_name_2 = request.form.get('hougu_name_2') or ""
    hougu_syurui = request.form.get('hougu_syurui') or ""
    hougu_color = request.form.get('hougu_color') or ""
    hougu_lv = request.form.get('hougu_lv') or ""
    shincho = request.form.get('shincho') or ""
    taiju = request.form.get('taiju') or ""
    source = request.form.get('source') or ""
    country = request.form.get('country') or ""
    zokusei_1 = request.form.get('zokusei_1') or ""
    zokusei_2 = request.form.get('zokusei_2') or ""
    sex = request.form.get('sex') or ""
    st1 = request.form.get('st1') or ""
    st2 = request.form.get('st2') or ""
    st3 = request.form.get('st3') or ""
    st4 = request.form.get('st4') or ""
    st5 = request.form.get('st5') or ""
    st6 = request.form.get('st6') or ""
    day = request.form.get('day') or ""
    skill_1 = request.form.get('skill_1') or "1"
    skill_2 = request.form.get('skill_2') or "1"
    skill_3 = request.form.get('skill_3') or "1"
    seihai = request.form.get('seihai') or "0"
    kizuna = request.form.get('kizuna') or "0"
    url = request.form.get('url') or ""
    me = request.form.get('me') or ""
    you = request.form.get('you') or ""
    he_she = request.form.get('he_she') or ""
    master = request.form.get('master') or ""
    s1_2_name_1 = request.form.get('1_2_name_1') or ""
    s1_2_num_1 = request.form.get('1_2_num_1') or "0"
    s1_2_name_2 = request.form.get('1_2_name_2') or ""
    s1_2_num_2 = request.form.get('1_2_num_2') or "0"
    s1_2_name_3 = request.form.get('1_2_name_3') or ""
    s1_2_num_3 = request.form.get('1_2_num_3') or "0"

    s2_3_name_1 = request.form.get('2_3_name_1') or ""
    s2_3_num_1 = request.form.get('2_3_num_1') or "0"
    s2_3_name_2 = request.form.get('2_3_name_2') or ""
    s2_3_num_2 = request.form.get('2_3_num_2') or "0"
    s2_3_name_3 = request.form.get('2_3_name_3') or ""
    s2_3_num_3 = request.form.get('2_3_num_3') or "0"
    s2_3_name_4 = request.form.get('2_3_name_4') or ""
    s2_3_num_4 = request.form.get('2_3_num_4') or "0"

    s3_4_name_1 = request.form.get('3_4_name_1') or ""
    s3_4_num_1 = request.form.get('3_4_num_1') or "0"
    s3_4_name_2 = request.form.get('3_4_name_2') or ""
    s3_4_num_2 = request.form.get('3_4_num_2') or "0"
    s3_4_name_3 = request.form.get('3_4_name_3') or ""
    s3_4_num_3 = request.form.get('3_4_num_3') or "0"

    s4_5_name_1 = request.form.get('4_5_name_1') or ""
    s4_5_num_1 = request.form.get('4_5_num_1') or "0"
    s4_5_name_2 = request.form.get('4_5_name_2') or ""
    s4_5_num_2 = request.form.get('4_5_num_2') or "0"
    s4_5_name_3 = request.form.get('4_5_name_3') or ""
    s4_5_num_3 = request.form.get('4_5_num_3') or "0"
    s4_5_name_4 = request.form.get('4_5_name_4') or ""
    s4_5_num_4 = request.form.get('4_5_num_4') or "0"

    s5_6_name_1 = request.form.get('5_6_name_1') or ""
    s5_6_num_1 = request.form.get('5_6_num_1') or "0"
    s5_6_name_2 = request.form.get('5_6_name_2') or ""
    s5_6_num_2 = request.form.get('5_6_num_2') or "0"
    s5_6_name_3 = request.form.get('5_6_name_3') or ""
    s5_6_num_3 = request.form.get('5_6_num_3') or "0"

    s6_7_name_1 = request.form.get('6_7_name_1') or ""
    s6_7_num_1 = request.form.get('6_7_num_1') or "0"
    s6_7_name_2 = request.form.get('6_7_name_2') or ""
    s6_7_num_2 = request.form.get('6_7_num_2') or "0"
    s6_7_name_3 = request.form.get('6_7_name_3') or ""
    s6_7_num_3 = request.form.get('6_7_num_3') or "0"
    s6_7_name_4 = request.form.get('6_7_name_4') or ""
    s6_7_num_4 = request.form.get('6_7_num_4') or "0"

    s7_8_name_1 = request.form.get('7_8_name_1') or ""
    s7_8_num_1 = request.form.get('7_8_num_1') or "0"
    s7_8_name_2 = request.form.get('7_8_name_2') or ""
    s7_8_num_2 = request.form.get('7_8_num_2') or "0"

    s8_9_name_1 = request.form.get('8_9_name_1') or ""
    s8_9_num_1 = request.form.get('8_9_num_1') or "0"
    s8_9_name_2 = request.form.get('8_9_name_2') or ""
    s8_9_num_2 = request.form.get('8_9_num_2') or "0"

    hp = request.form.get('hp') or "0"
    atk = request.form.get('atk') or "0"
    memo = request.form.get('memo') or ""

    input_list = {
        "NO":NO,
        "name":name,
        "class_s":class_s,
        "star":star,
        "hougu_name_1":hougu_name_1,
        "hougu_name_2":hougu_name_2,
        "hougu_syurui":hougu_syurui,
        "hougu_color":hougu_color,
        "hougu_lv":hougu_lv , 
        "shincho":shincho,
        "taiju":taiju,
        "source":source,
        "country":country,
        "zokusei_1":zokusei_1,
        "zokusei_2":zokusei_2,
        "sex":sex,
        "st1":st1,
        "st2":st2,
        "st3":st3,
        "st4":st4,
        "st5":st5,
        "st6":st6,
        "day":day,
        "skill_1":skill_1,
        "skill_2":skill_2,
        "skill_3":skill_3,
        "kizuna":kizuna,
        "seihai":seihai,
        "url":url,
        "me":me,
        "you":you,
        "he_she":he_she,
        "master":master,
        "s1_2_name_1":s1_2_name_1,
        "s1_2_num_1":s1_2_num_1,
        "s1_2_name_2":s1_2_name_2,
        "s1_2_num_2":s1_2_num_2,
        "s1_2_name_3":s1_2_name_3,
        "s1_2_num_3":s1_2_num_3,

        "s2_3_name_1":s2_3_name_1,
        "s2_3_num_1":s2_3_num_1,
        "s2_3_name_2":s2_3_name_2,
        "s2_3_num_2":s2_3_num_2,
        "s2_3_name_3":s2_3_name_3,
        "s2_3_num_3":s2_3_num_3,
        "s2_3_name_4":s2_3_name_4,
        "s2_3_num_4":s2_3_num_4,

        "s3_4_name_1":s3_4_name_1,
        "s3_4_num_1":s3_4_num_1,
        "s3_4_name_2":s3_4_name_2,
        "s3_4_num_2":s3_4_num_2,
        "s3_4_name_3":s3_4_name_3,
        "s3_4_num_3":s3_4_num_3,

        "s4_5_name_1":s4_5_name_1,
        "s4_5_num_1":s4_5_num_1,
        "s4_5_name_2":s4_5_name_2,
        "s4_5_num_2":s4_5_num_2,
        "s4_5_name_3":s4_5_name_3,
        "s4_5_num_3":s4_5_num_3,

        "s5_6_name_1":s5_6_name_1,
        "s5_6_num_1":s5_6_num_1,
        "s5_6_name_2":s5_6_name_2,
        "s5_6_num_2":s5_6_num_2,
        "s5_6_name_3":s5_6_name_3,
        "s5_6_num_3":s5_6_num_3,

        "s6_7_name_1":s6_7_name_1,
        "s6_7_num_1":s6_7_num_1,
        "s6_7_name_2":s6_7_name_2,
        "s6_7_num_2":s6_7_num_2,
        "s6_7_name_3":s6_7_name_3,
        "s6_7_num_3":s6_7_num_3,
        "s6_7_name_4":s6_7_name_4,

        "s7_8_name_1":s7_8_name_1,
        "s7_8_num_1":s7_8_num_1,
        "s7_8_name_2":s7_8_name_2,
        "s7_8_num_2":s7_8_num_2,

        "s8_9_name_1":s8_9_name_1,
        "s8_9_num_1":s8_9_num_1,
        "s8_9_name_2":s8_9_name_2,
        "s8_9_num_2":s8_9_num_2,
        "hp":hp,
        "atk":atk,
        "memo":memo
    }
    session['input_list'] = input_list

    # NO重複チェック
    savants = Savant_list.query.all()

    for val in savants:
        if val.NO == int(NO):
            flash('NOが重複しています', 'error')
            return redirect(url_for('input'))


    # DB登録
    savant = Savant_list(
        NO = int(NO),
        name = name ,
        class_s = class_s ,
        star = int(star) ,
        hougu_name = hougu_name_1 + "（" + hougu_name_2 + "）",
        hougu_syurui = hougu_syurui,
        hougu_color = hougu_color,
        hougu_lv = int(hougu_lv),
        shincho = shincho,
        taiju = taiju,
        source = source,
        country = country,
        zokusei_1 = zokusei_1 ,
        zokusei_2 = zokusei_2 ,
        sex = sex,
        st1 = st1,
        st2 = st2,
        st3 = st3,
        st4 = st4,
        st5 = st5,
        st6 = st6,
        day = day,
        skill_1 = int(skill_1),
        skill_2 = int(skill_2),
        skill_3 = int(skill_3),
        kizuna = int(kizuna) ,
        seihai = int(seihai) ,
        url = url,
        me = me,
        you = you,
        he_she = he_she,
        master = master,
        hp = int(hp),
        atk = int(atk),
        memo = memo
    )

    use_sozai = Use_sozai.query.get(NO)
    
    if use_sozai:
        pass
    else:
        use_sozai = Use_sozai(
            NO = int(NO),
            s1_2_name_1 = s1_2_name_1,
            s1_2_num_1  = int(s1_2_num_1) ,
            s1_2_name_2 = s1_2_name_2,
            s1_2_num_2  = int(s1_2_num_2) ,
            s1_2_name_3 = s1_2_name_3,
            s1_2_num_3  = int(s1_2_num_3) ,

            s2_3_name_1 = s2_3_name_1,
            s2_3_num_1  = int(s2_3_num_1) ,
            s2_3_name_2 = s2_3_name_2,
            s2_3_num_2  = int(s2_3_num_2) ,
            s2_3_name_3 = s2_3_name_3,
            s2_3_num_3  = int(s2_3_num_3) ,
            s2_3_name_4 = s2_3_name_4,
            s2_3_num_4  = int(s2_3_num_4) ,

            s3_4_name_1 = s3_4_name_1,
            s3_4_num_1  = int(s3_4_num_1) ,
            s3_4_name_2 = s3_4_name_2,
            s3_4_num_2  = int(s3_4_num_2) ,
            s3_4_name_3 = s3_4_name_3,
            s3_4_num_3  = int(s3_4_num_3) ,

            s4_5_name_1 = s4_5_name_1,
            s4_5_num_1  = int(s4_5_num_1) ,
            s4_5_name_2 = s4_5_name_2,
            s4_5_num_2  = int(s4_5_num_2) ,
            s4_5_name_3 = s4_5_name_3,
            s4_5_num_3  = int(s4_5_num_3) ,
            s4_5_name_4 = s4_5_name_4,
            s4_5_num_4 = int(s4_5_num_4),

            s5_6_name_1 = s5_6_name_1,
            s5_6_num_1  = int(s5_6_num_1) ,
            s5_6_name_2 = s5_6_name_2,
            s5_6_num_2  = int(s5_6_num_2) ,
            s5_6_name_3 = s5_6_name_3,
            s5_6_num_3  = int(s5_6_num_3) ,

            s6_7_name_1 = s6_7_name_1,
            s6_7_num_1  = int(s6_7_num_1) ,
            s6_7_name_2 = s6_7_name_2,
            s6_7_num_2  = int(s6_7_num_2) ,
            s6_7_name_3 = s6_7_name_3,
            s6_7_num_3  = int(s6_7_num_3) ,
            s6_7_name_4 = s6_7_name_4,
            s6_7_num_4 = int(s6_7_num_4),

            s7_8_name_1 = s7_8_name_1,
            s7_8_num_1  = int(s7_8_num_1) ,
            s7_8_name_2 = s7_8_name_2,
            s7_8_num_2  = int(s7_8_num_2) ,

            s8_9_name_1 = s8_9_name_1,
            s8_9_num_1  = int(s8_9_num_1) ,
            s8_9_name_2 = s8_9_name_2,
            s8_9_num_2  = int(s8_9_num_2) ,
        )
        db.session.add(use_sozai)
    try:    
        db.session.add(savant)
        db.session.commit()
    except Exception as e:
        flash(e, 'error')
        return redirect(url_for('input'))

    session.pop('input_list', None)

    flash('登録しました', 'success')
    return redirect(url_for('list_view'))

#入力チェック→更新
@app.route('/update_check', methods=["POST"])
def update_check():
    
    NO = request.form.get('NO') or ""
    name = request.form.get('name') or ""
    class_s = request.form.get('class_s') or ""
    star = request.form.get('star') or ""
    hougu_name = request.form.get('hougu_name') or ""
    hougu_syurui = request.form.get('hougu_syurui') or ""
    hougu_color = request.form.get('hougu_color') or ""
    hougu_lv = request.form.get('hougu_lv') or ""
    shincho = request.form.get('shincho') or ""
    taiju = request.form.get('taiju') or ""
    source = request.form.get('source') or ""
    country = request.form.get('country') or ""
    zokusei_1 = request.form.get('zokusei_1') or ""
    zokusei_2 = request.form.get('zokusei_2') or ""
    sex = request.form.get('sex') or ""
    st1 = request.form.get('st1') or ""
    st2 = request.form.get('st2') or ""
    st3 = request.form.get('st3') or ""
    st4 = request.form.get('st4') or ""
    st5 = request.form.get('st5') or ""
    st6 = request.form.get('st6') or ""
    day = request.form.get('day') or ""
    skill_1 = request.form.get('skill_1') or "1"
    skill_2 = request.form.get('skill_2') or "1"
    skill_3 = request.form.get('skill_3') or "1"
    seihai = request.form.get('seihai') or "0"
    kizuna = request.form.get('kizuna') or "0"
    url = request.form.get('url') or ""
    me = request.form.get('me') or ""
    you = request.form.get('you') or ""
    he_she = request.form.get('he_she') or ""
    master = request.form.get('master') or ""
    s1_2_name_1 = request.form.get('1_2_name_1') or ""
    s1_2_num_1 = request.form.get('1_2_num_1') or "0"
    s1_2_name_2 = request.form.get('1_2_name_2') or ""
    s1_2_num_2 = request.form.get('1_2_num_2') or "0"
    s1_2_name_3 = request.form.get('1_2_name_3') or ""
    s1_2_num_3 = request.form.get('1_2_num_3') or "0"

    s2_3_name_1 = request.form.get('2_3_name_1') or ""
    s2_3_num_1 = request.form.get('2_3_num_1') or "0"
    s2_3_name_2 = request.form.get('2_3_name_2') or ""
    s2_3_num_2 = request.form.get('2_3_num_2') or "0"
    s2_3_name_3 = request.form.get('2_3_name_3') or ""
    s2_3_num_3 = request.form.get('2_3_num_3') or "0"
    s2_3_name_4 = request.form.get('2_3_name_4') or ""
    s2_3_num_4 = request.form.get('2_3_num_4') or "0"

    s3_4_name_1 = request.form.get('3_4_name_1') or ""
    s3_4_num_1 = request.form.get('3_4_num_1') or "0"
    s3_4_name_2 = request.form.get('3_4_name_2') or ""
    s3_4_num_2 = request.form.get('3_4_num_2') or "0"
    s3_4_name_3 = request.form.get('3_4_name_3') or ""
    s3_4_num_3 = request.form.get('3_4_num_3') or "0"

    s4_5_name_1 = request.form.get('4_5_name_1') or ""
    s4_5_num_1 = request.form.get('4_5_num_1') or "0"
    s4_5_name_2 = request.form.get('4_5_name_2') or ""
    s4_5_num_2 = request.form.get('4_5_num_2') or "0"
    s4_5_name_3 = request.form.get('4_5_name_3') or ""
    s4_5_num_3 = request.form.get('4_5_num_3') or "0"
    s4_5_name_4 = request.form.get('4_5_name_4') or ""
    s4_5_num_4 = request.form.get('4_5_num_4') or "0"

    s5_6_name_1 = request.form.get('5_6_name_1') or ""
    s5_6_num_1 = request.form.get('5_6_num_1') or "0"
    s5_6_name_2 = request.form.get('5_6_name_2') or ""
    s5_6_num_2 = request.form.get('5_6_num_2') or "0"
    s5_6_name_3 = request.form.get('5_6_name_3') or ""
    s5_6_num_3 = request.form.get('5_6_num_3') or "0"

    s6_7_name_1 = request.form.get('6_7_name_1') or ""
    s6_7_num_1 = request.form.get('6_7_num_1') or "0"
    s6_7_name_2 = request.form.get('6_7_name_2') or ""
    s6_7_num_2 = request.form.get('6_7_num_2') or "0"
    s6_7_name_3 = request.form.get('6_7_name_3') or ""
    s6_7_num_3 = request.form.get('6_7_num_3') or "0"
    s6_7_name_4 = request.form.get('6_7_name_4') or ""
    s6_7_num_4 = request.form.get('6_7_num_4') or "0"

    s7_8_name_1 = request.form.get('7_8_name_1') or ""
    s7_8_num_1 = request.form.get('7_8_num_1') or "0"
    s7_8_name_2 = request.form.get('7_8_name_2') or ""
    s7_8_num_2 = request.form.get('7_8_num_2') or "0"

    s8_9_name_1 = request.form.get('8_9_name_1') or ""
    s8_9_num_1 = request.form.get('8_9_num_1') or "0"
    s8_9_name_2 = request.form.get('8_9_name_2') or ""
    s8_9_num_2 = request.form.get('8_9_num_2') or "0"

    hp = request.form.get('hp') or "0"
    atk = request.form.get('atk') or "0"
    memo = request.form.get('memo') or ""

    input_list = {
        "NO":NO,
        "name":name,
        "class_s":class_s,
        "star":star,
        "hougu_name":hougu_name,
        "hougu_syurui":hougu_syurui,
        "hougu_color":hougu_color,
        "hougu_lv":hougu_lv , 
        "shincho":shincho,
        "taiju":taiju,
        "source":source,
        "country":country,
        "zokusei_1":zokusei_1,
        "zokusei_2":zokusei_2,
        "sex":sex,
        "st1":st1,
        "st2":st2,
        "st3":st3,
        "st4":st4,
        "st5":st5,
        "st6":st6,
        "day":day,
        "skill_1":skill_1,
        "skill_2":skill_2,
        "skill_3":skill_3,
        "kizuna":kizuna,
        "seihai":seihai,
        "url":url,
        "me":me,
        "you":you,
        "he_she":he_she,
        "master":master,
        "s1_2_name_1":s1_2_name_1,
        "s1_2_num_1":s1_2_num_1,
        "s1_2_name_2":s1_2_name_2,
        "s1_2_num_2":s1_2_num_2,
        "s1_2_name_3":s1_2_name_3,
        "s1_2_num_3":s1_2_num_3,

        "s2_3_name_1":s2_3_name_1,
        "s2_3_num_1":s2_3_num_1,
        "s2_3_name_2":s2_3_name_2,
        "s2_3_num_2":s2_3_num_2,
        "s2_3_name_3":s2_3_name_3,
        "s2_3_num_3":s2_3_num_3,
        "s2_3_name_4":s2_3_name_4,
        "s2_3_num_4":s2_3_num_4,

        "s3_4_name_1":s3_4_name_1,
        "s3_4_num_1":s3_4_num_1,
        "s3_4_name_2":s3_4_name_2,
        "s3_4_num_2":s3_4_num_2,
        "s3_4_name_3":s3_4_name_3,
        "s3_4_num_3":s3_4_num_3,

        "s4_5_name_1":s4_5_name_1,
        "s4_5_num_1":s4_5_num_1,
        "s4_5_name_2":s4_5_name_2,
        "s4_5_num_2":s4_5_num_2,
        "s4_5_name_3":s4_5_name_3,
        "s4_5_num_3":s4_5_num_3,

        "s5_6_name_1":s5_6_name_1,
        "s5_6_num_1":s5_6_num_1,
        "s5_6_name_2":s5_6_name_2,
        "s5_6_num_2":s5_6_num_2,
        "s5_6_name_3":s5_6_name_3,
        "s5_6_num_3":s5_6_num_3,

        "s6_7_name_1":s6_7_name_1,
        "s6_7_num_1":s6_7_num_1,
        "s6_7_name_2":s6_7_name_2,
        "s6_7_num_2":s6_7_num_2,
        "s6_7_name_3":s6_7_name_3,
        "s6_7_num_3":s6_7_num_3,
        "s6_7_name_4":s6_7_name_4,

        "s7_8_name_1":s7_8_name_1,
        "s7_8_num_1":s7_8_num_1,
        "s7_8_name_2":s7_8_name_2,
        "s7_8_num_2":s7_8_num_2,

        "s8_9_name_1":s8_9_name_1,
        "s8_9_num_1":s8_9_num_1,
        "s8_9_name_2":s8_9_name_2,
        "s8_9_num_2":s8_9_num_2,
        "hp":hp,
        "atk":atk,
        "memo":memo
    }
    session['input_list'] = input_list


    # NO重複チェック
    savants = Savant_list.query.all()
    savant = Savant_list.query.get(session.get('up_NO'))

    for val in savants:
        if val.NO == int(NO) and savant.NO != int(NO):
            flash('NOが重複しています', 'error')
            return redirect(url_for('input'))

    use_sozai = Use_sozai.query.get(session.get('up_NO'))

    if use_sozai:
        pass
    else:
        use_sozai_new = Use_sozai(
            NO = int(session.get('up_NO')),
            s1_2_name_1 = s1_2_name_1,
            s1_2_num_1  = int(s1_2_num_1) ,
            s1_2_name_2 = s1_2_name_2,
            s1_2_num_2  = int(s1_2_num_2) ,
            s1_2_name_3 = s1_2_name_3,
            s1_2_num_3  = int(s1_2_num_3) ,

            s2_3_name_1 = s2_3_name_1,
            s2_3_num_1  = int(s2_3_num_1) ,
            s2_3_name_2 = s2_3_name_2,
            s2_3_num_2  = int(s2_3_num_2) ,
            s2_3_name_3 = s2_3_name_3,
            s2_3_num_3  = int(s2_3_num_3) ,
            s2_3_name_4 = s2_3_name_4,
            s2_3_num_4  = int(s2_3_num_4) ,

            s3_4_name_1 = s3_4_name_1,
            s3_4_num_1  = int(s3_4_num_1) ,
            s3_4_name_2 = s3_4_name_2,
            s3_4_num_2  = int(s3_4_num_2) ,
            s3_4_name_3 = s3_4_name_3,
            s3_4_num_3  = int(s3_4_num_3) ,

            s4_5_name_1 = s4_5_name_1,
            s4_5_num_1  = int(s4_5_num_1) ,
            s4_5_name_2 = s4_5_name_2,
            s4_5_num_2  = int(s4_5_num_2) ,
            s4_5_name_3 = s4_5_name_3,
            s4_5_num_3  = int(s4_5_num_3) ,
            s4_5_name_4 = s4_5_name_4,
            s4_5_num_4 = int(s4_5_num_4),

            s5_6_name_1 = s5_6_name_1,
            s5_6_num_1  = int(s5_6_num_1) ,
            s5_6_name_2 = s5_6_name_2,
            s5_6_num_2  = int(s5_6_num_2) ,
            s5_6_name_3 = s5_6_name_3,
            s5_6_num_3  = int(s5_6_num_3) ,

            s6_7_name_1 = s6_7_name_1,
            s6_7_num_1  = int(s6_7_num_1) ,
            s6_7_name_2 = s6_7_name_2,
            s6_7_num_2  = int(s6_7_num_2) ,
            s6_7_name_3 = s6_7_name_3,
            s6_7_num_3  = int(s6_7_num_3) ,
            s6_7_name_4 = s6_7_name_4,
            s6_7_num_4 = int(s6_7_num_4),

            s7_8_name_1 = s7_8_name_1,
            s7_8_num_1  = int(s7_8_num_1) ,
            s7_8_name_2 = s7_8_name_2,
            s7_8_num_2  = int(s7_8_num_2) ,

            s8_9_name_1 = s8_9_name_1,
            s8_9_num_1  = int(s8_9_num_1) ,
            s8_9_name_2 = s8_9_name_2,
            s8_9_num_2  = int(s8_9_num_2) ,
        )
        try:    
            db.session.add(use_sozai_new)
            db.session.commit()
        except Exception as e:
            flash(e, 'error')
            return redirect(url_for('input'))

    use_sozai = Use_sozai.query.get(session.get('up_NO'))

    # DB登録
    savant.name = name 
    savant.class_s = class_s 
    savant.star = int(star) 
    savant.hougu_name = hougu_name
    savant.hougu_syurui = hougu_syurui
    savant.hougu_color = hougu_color
    savant.hougu_lv = int(hougu_lv)
    savant.shincho = shincho
    savant.taiju = taiju
    savant.source = source
    savant.country = country
    savant.zokusei_1 = zokusei_1 
    savant.zokusei_2 = zokusei_2 
    savant.sex = sex
    savant.st1 = st1
    savant.st2 = st2
    savant.st3 = st3
    savant.st4 = st4
    savant.st5 = st5
    savant.st6 = st6
    savant.day = day
    savant.skill_1 = int(skill_1)
    savant.skill_2 = int(skill_2)
    savant.skill_3 = int(skill_3)
    savant.kizuna = int(kizuna) 
    savant.seihai = int(seihai) 
    savant.url = url
    savant.me = me
    savant.you = you
    savant.he_she = he_she
    savant.master = master
    savant.hp = int(hp)
    savant.atk = int(atk)
    savant.memo = memo

    use_sozai.s1_2_name_1 = s1_2_name_1
    use_sozai.s1_2_num_1  = int(s1_2_num_1)
    use_sozai.s1_2_name_2 = s1_2_name_2
    use_sozai.s1_2_num_2  = int(s1_2_num_2)
    use_sozai.s1_2_name_3 = s1_2_name_3
    use_sozai.s1_2_num_3  = int(s1_2_num_3)

    use_sozai.s2_3_name_1 = s2_3_name_1
    use_sozai.s2_3_num_1  = int(s2_3_num_1)
    use_sozai.s2_3_name_2 = s2_3_name_2
    use_sozai.s2_3_num_2  = int(s2_3_num_2)
    use_sozai.s2_3_name_3 = s2_3_name_3
    use_sozai.s2_3_num_3  = int(s2_3_num_3)
    use_sozai.s2_3_name_4 = s2_3_name_4
    use_sozai.s2_3_num_4  = int(s2_3_num_4)

    use_sozai.s3_4_name_1 = s3_4_name_1
    use_sozai.s3_4_num_1  = int(s3_4_num_1)
    use_sozai.s3_4_name_2 = s3_4_name_2
    use_sozai.s3_4_num_2  = int(s3_4_num_2)
    use_sozai.s3_4_name_3 = s3_4_name_3
    use_sozai.s3_4_num_3  = int(s3_4_num_3)

    use_sozai.s4_5_name_1 = s4_5_name_1
    use_sozai.s4_5_num_1  = int(s4_5_num_1)
    use_sozai.s4_5_name_2 = s4_5_name_2
    use_sozai.s4_5_num_2  = int(s4_5_num_2)
    use_sozai.s4_5_name_3 = s4_5_name_3
    use_sozai.s4_5_num_3  = int(s4_5_num_3)
    use_sozai.s4_5_name_4 = s4_5_name_4
    use_sozai.s4_5_num_4  = int(s4_5_num_4)

    use_sozai.s5_6_name_1 = s5_6_name_1
    use_sozai.s5_6_num_1  = int(s5_6_num_1)
    use_sozai.s5_6_name_2 = s5_6_name_2
    use_sozai.s5_6_num_2  = int(s5_6_num_2)
    use_sozai.s5_6_name_3 = s5_6_name_3
    use_sozai.s5_6_num_3  = int(s5_6_num_3)

    use_sozai.s6_7_name_1 = s6_7_name_1
    use_sozai.s6_7_num_1  = int(s6_7_num_1)
    use_sozai.s6_7_name_2 = s6_7_name_2
    use_sozai.s6_7_num_2  = int(s6_7_num_2)
    use_sozai.s6_7_name_3 = s6_7_name_3
    use_sozai.s6_7_num_3  = int(s6_7_num_3)
    use_sozai.s6_7_name_4 = s6_7_name_4
    use_sozai.s6_7_num_4  = int(s6_7_num_4)

    use_sozai.s7_8_name_1 = s7_8_name_1
    use_sozai.s7_8_num_1  = int(s7_8_num_1)
    use_sozai.s7_8_name_2 = s7_8_name_2
    use_sozai.s7_8_num_2  = int(s7_8_num_2)

    use_sozai.s8_9_name_1 = s8_9_name_1
    use_sozai.s8_9_num_1  = int(s8_9_num_1)
    use_sozai.s8_9_name_2 = s8_9_name_2
    use_sozai.s8_9_num_2  = int(s8_9_num_2)


    try:    
        db.session.merge(savant)
        db.session.merge(use_sozai)
        db.session.commit()
    except Exception as e:
        flash(e, 'error')
        return redirect(url_for('input'))

    session.pop('input_list', None)

    flash('更新しました', 'success')
    return redirect(url_for('list_view'))

#素材計算
@app.route('/sozai', methods=["POST","GET"])
def sozai_view():

    sozai_list = Sozai.query.all()
    savant_list = Savant_list.query.all()
    class_list = db.session.query(Savant_list).group_by(Savant_list.class_s)

    if request.form.get('reset'):
        session.pop('skill_up_list', None)

    if request.form.getlist('skill_up_list'):
        session['skill_up_list'] = request.form.getlist('skill_up_list')

    skill_up_list = session.get('skill_up_list') or ""
    # skill_up_list = [0]

    #空の素材リスト作成
    use_sozai_list = {}
    for val in sozai_list:
        use_sozai_list[val.name] = 0

    #int型のリストに
    int_skill_up_list = []
    for No in skill_up_list:
        if No != " ":
            int_skill_up_list.append(int(No))

    #素材のリスト作成
    for No in int_skill_up_list:
        if No != " ":
            savant = Savant_list.query.get(No)
            use_sozai = Use_sozai.query.get(No)
            
            if use_sozai:
                if savant.skill_1 <= 8:
                    if use_sozai.s8_9_name_1 != "" and use_sozai.s8_9_num_1 != 0:
                        use_sozai_list.setdefault(use_sozai.s8_9_name_1, 0)
                        use_sozai_list[use_sozai.s8_9_name_1] += use_sozai.s8_9_num_1
                    if use_sozai.s8_9_name_2 != "" and use_sozai.s8_9_num_2!= 0:
                        use_sozai_list.setdefault(use_sozai.s8_9_name_2, 0)
                        use_sozai_list[use_sozai.s8_9_name_2] += use_sozai.s8_9_num_2
                if savant.skill_1 <= 7:
                    if use_sozai.s7_8_name_1 != "" and use_sozai.s7_8_num_1 != 0:
                        use_sozai_list.setdefault(use_sozai.s7_8_name_1, 0)
                        use_sozai_list[use_sozai.s7_8_name_1] += use_sozai.s7_8_num_1
                    if use_sozai.s7_8_name_2 != "" and use_sozai.s7_8_num_2!= 0:
                        use_sozai_list.setdefault(use_sozai.s7_8_name_2, 0)
                        use_sozai_list[use_sozai.s7_8_name_2] += use_sozai.s7_8_num_2
                if savant.skill_1 <= 6:
                    if use_sozai.s6_7_name_1 != "" and use_sozai.s6_7_num_1 != 0:
                        use_sozai_list.setdefault(use_sozai.s6_7_name_1, 0)
                        use_sozai_list[use_sozai.s6_7_name_1] += use_sozai.s6_7_num_1
                    if use_sozai.s6_7_name_2 != "" and use_sozai.s6_7_num_2!= 0:
                        use_sozai_list.setdefault(use_sozai.s6_7_name_2, 0)
                        use_sozai_list[use_sozai.s6_7_name_2] += use_sozai.s6_7_num_2
                    if use_sozai.s6_7_name_3 != "" and use_sozai.s6_7_num_3 != 0:
                        use_sozai_list.setdefault(use_sozai.s6_7_name_3, 0)
                        use_sozai_list[use_sozai.s6_7_name_3] += use_sozai.s6_7_num_3
                    if use_sozai.s6_7_name_4 != "" and use_sozai.s6_7_num_4 != 0:
                        use_sozai_list.setdefault(use_sozai.s6_7_name_4, 0)
                        use_sozai_list[use_sozai.s6_7_name_4] += use_sozai.s6_7_num_4
                if savant.skill_1 <= 5:
                    if use_sozai.s5_6_name_1 != "" and use_sozai.s5_6_num_1 != 0:
                        use_sozai_list.setdefault(use_sozai.s5_6_name_1, 0)
                        use_sozai_list[use_sozai.s5_6_name_1] += use_sozai.s5_6_num_1
                    if use_sozai.s5_6_name_2 != "" and use_sozai.s5_6_num_2!= 0:
                        use_sozai_list.setdefault(use_sozai.s5_6_name_2, 0)
                        use_sozai_list[use_sozai.s5_6_name_2] += use_sozai.s5_6_num_2
                    if use_sozai.s5_6_name_3 != "" and use_sozai.s5_6_num_3 != 0:
                        use_sozai_list.setdefault(use_sozai.s5_6_name_3, 0)
                        use_sozai_list[use_sozai.s5_6_name_3] += use_sozai.s5_6_num_3
                if savant.skill_1 <= 4:
                    if use_sozai.s4_5_name_1 != "" and use_sozai.s4_5_num_1 != 0:
                        use_sozai_list.setdefault(use_sozai.s4_5_name_1, 0)
                        use_sozai_list[use_sozai.s4_5_name_1] += use_sozai.s4_5_num_1
                    if use_sozai.s4_5_name_2 != "" and use_sozai.s4_5_num_2!= 0:
                        use_sozai_list.setdefault(use_sozai.s4_5_name_2, 0)
                        use_sozai_list[use_sozai.s4_5_name_2] += use_sozai.s4_5_num_2
                    if use_sozai.s4_5_name_3 != "" and use_sozai.s4_5_num_3 != 0:
                        use_sozai_list.setdefault(use_sozai.s4_5_name_3, 0)
                        use_sozai_list[use_sozai.s4_5_name_3] += use_sozai.s4_5_num_3
                    if use_sozai.s4_5_name_4 != "" and use_sozai.s4_5_num_4 != 0:
                        use_sozai_list.setdefault(use_sozai.s4_5_name_4, 0)
                        use_sozai_list[use_sozai.s4_5_name_4] += use_sozai.s4_5_num_4
                if savant.skill_1 <= 3:
                    if use_sozai.s3_4_name_1 != "" and use_sozai.s3_4_num_1 != 0:
                        use_sozai_list.setdefault(use_sozai.s3_4_name_1, 0)
                        use_sozai_list[use_sozai.s3_4_name_1] += use_sozai.s3_4_num_1
                    if use_sozai.s3_4_name_2 != "" and use_sozai.s3_4_num_2!= 0:
                        use_sozai_list.setdefault(use_sozai.s3_4_name_2, 0)
                        use_sozai_list[use_sozai.s3_4_name_2] += use_sozai.s3_4_num_2
                    if use_sozai.s3_4_name_3 != "" and use_sozai.s3_4_num_3 != 0:
                        use_sozai_list.setdefault(use_sozai.s3_4_name_3, 0)
                        use_sozai_list[use_sozai.s3_4_name_3] += use_sozai.s3_4_num_3
                if savant.skill_1 <= 2:
                    if use_sozai.s2_3_name_1 != "" and use_sozai.s2_3_num_1 != 0:
                        use_sozai_list.setdefault(use_sozai.s2_3_name_1, 0)
                        use_sozai_list[use_sozai.s2_3_name_1] += use_sozai.s2_3_num_1
                    if use_sozai.s2_3_name_2 != "" and use_sozai.s2_3_num_2!= 0:
                        use_sozai_list.setdefault(use_sozai.s2_3_name_2, 0)
                        use_sozai_list[use_sozai.s2_3_name_2] += use_sozai.s2_3_num_2
                    if use_sozai.s2_3_name_3 != "" and use_sozai.s2_3_num_3 != 0:
                        use_sozai_list.setdefault(use_sozai.s2_3_name_3, 0)
                        use_sozai_list[use_sozai.s2_3_name_3] += use_sozai.s2_3_num_3
                    if use_sozai.s2_3_name_4 != "" and use_sozai.s2_3_num_4 != 0:
                        use_sozai_list.setdefault(use_sozai.s2_3_name_4, 0)
                        use_sozai_list[use_sozai.s2_3_name_4] += use_sozai.s2_3_num_4
                if savant.skill_1 <= 1:
                    if use_sozai.s1_2_name_1 != "" and use_sozai.s1_2_num_1 != 0:
                        use_sozai_list.setdefault(use_sozai.s1_2_name_1, 0)
                        use_sozai_list[use_sozai.s1_2_name_1] += use_sozai.s1_2_num_1
                    if use_sozai.s1_2_name_2 != "" and use_sozai.s1_2_num_2!= 0:
                        use_sozai_list.setdefault(use_sozai.s1_2_name_2, 0)
                        use_sozai_list[use_sozai.s1_2_name_2] += use_sozai.s1_2_num_2
                    if use_sozai.s1_2_name_3 != "" and use_sozai.s1_2_num_3 != 0:
                        use_sozai_list.setdefault(use_sozai.s1_2_name_3, 0)
                        use_sozai_list[use_sozai.s1_2_name_3] += use_sozai.s1_2_num_3
                
                if savant.skill_2 <= 8:
                    if use_sozai.s8_9_name_1 != "" and use_sozai.s8_9_num_1 != 0:
                        use_sozai_list.setdefault(use_sozai.s8_9_name_1, 0)
                        use_sozai_list[use_sozai.s8_9_name_1] += use_sozai.s8_9_num_1
                    if use_sozai.s8_9_name_2 != "" and use_sozai.s8_9_num_2!= 0:
                        use_sozai_list.setdefault(use_sozai.s8_9_name_2, 0)
                        use_sozai_list[use_sozai.s8_9_name_2] += use_sozai.s8_9_num_2
                if savant.skill_2 <= 7:
                    if use_sozai.s7_8_name_1 != "" and use_sozai.s7_8_num_1 != 0:
                        use_sozai_list.setdefault(use_sozai.s7_8_name_1, 0)
                        use_sozai_list[use_sozai.s7_8_name_1] += use_sozai.s7_8_num_1
                    if use_sozai.s7_8_name_2 != "" and use_sozai.s7_8_num_2!= 0:
                        use_sozai_list.setdefault(use_sozai.s7_8_name_2, 0)
                        use_sozai_list[use_sozai.s7_8_name_2] += use_sozai.s7_8_num_2
                if savant.skill_2 <= 6:
                    if use_sozai.s6_7_name_1 != "" and use_sozai.s6_7_num_1 != 0:
                        use_sozai_list.setdefault(use_sozai.s6_7_name_1, 0)
                        use_sozai_list[use_sozai.s6_7_name_1] += use_sozai.s6_7_num_1
                    if use_sozai.s6_7_name_2 != "" and use_sozai.s6_7_num_2!= 0:
                        use_sozai_list.setdefault(use_sozai.s6_7_name_2, 0)
                        use_sozai_list[use_sozai.s6_7_name_2] += use_sozai.s6_7_num_2
                    if use_sozai.s6_7_name_3 != "" and use_sozai.s6_7_num_3 != 0:
                        use_sozai_list.setdefault(use_sozai.s6_7_name_3, 0)
                        use_sozai_list[use_sozai.s6_7_name_3] += use_sozai.s6_7_num_3
                    if use_sozai.s6_7_name_4 != "" and use_sozai.s6_7_num_4 != 0:
                        use_sozai_list.setdefault(use_sozai.s6_7_name_4, 0)
                        use_sozai_list[use_sozai.s6_7_name_4] += use_sozai.s6_7_num_4
                if savant.skill_2 <= 5:
                    if use_sozai.s5_6_name_1 != "" and use_sozai.s5_6_num_1 != 0:
                        use_sozai_list.setdefault(use_sozai.s5_6_name_1, 0)
                        use_sozai_list[use_sozai.s5_6_name_1] += use_sozai.s5_6_num_1
                    if use_sozai.s5_6_name_2 != "" and use_sozai.s5_6_num_2!= 0:
                        use_sozai_list.setdefault(use_sozai.s5_6_name_2, 0)
                        use_sozai_list[use_sozai.s5_6_name_2] += use_sozai.s5_6_num_2
                    if use_sozai.s5_6_name_3 != "" and use_sozai.s5_6_num_3 != 0:
                        use_sozai_list.setdefault(use_sozai.s5_6_name_3, 0)
                        use_sozai_list[use_sozai.s5_6_name_3] += use_sozai.s5_6_num_3
                if savant.skill_2 <= 4:
                    if use_sozai.s4_5_name_1 != "" and use_sozai.s4_5_num_1 != 0:
                        use_sozai_list.setdefault(use_sozai.s4_5_name_1, 0)
                        use_sozai_list[use_sozai.s4_5_name_1] += use_sozai.s4_5_num_1
                    if use_sozai.s4_5_name_2 != "" and use_sozai.s4_5_num_2!= 0:
                        use_sozai_list.setdefault(use_sozai.s4_5_name_2, 0)
                        use_sozai_list[use_sozai.s4_5_name_2] += use_sozai.s4_5_num_2
                    if use_sozai.s4_5_name_3 != "" and use_sozai.s4_5_num_3 != 0:
                        use_sozai_list.setdefault(use_sozai.s4_5_name_3, 0)
                        use_sozai_list[use_sozai.s4_5_name_3] += use_sozai.s4_5_num_3
                    if use_sozai.s4_5_name_4 != "" and use_sozai.s4_5_num_4 != 0:
                        use_sozai_list.setdefault(use_sozai.s4_5_name_4, 0)
                        use_sozai_list[use_sozai.s4_5_name_4] += use_sozai.s4_5_num_4
                if savant.skill_2 <= 3:
                    if use_sozai.s3_4_name_1 != "" and use_sozai.s3_4_num_1 != 0:
                        use_sozai_list.setdefault(use_sozai.s3_4_name_1, 0)
                        use_sozai_list[use_sozai.s3_4_name_1] += use_sozai.s3_4_num_1
                    if use_sozai.s3_4_name_2 != "" and use_sozai.s3_4_num_2!= 0:
                        use_sozai_list.setdefault(use_sozai.s3_4_name_2, 0)
                        use_sozai_list[use_sozai.s3_4_name_2] += use_sozai.s3_4_num_2
                    if use_sozai.s3_4_name_3 != "" and use_sozai.s3_4_num_3 != 0:
                        use_sozai_list.setdefault(use_sozai.s3_4_name_3, 0)
                        use_sozai_list[use_sozai.s3_4_name_3] += use_sozai.s3_4_num_3
                if savant.skill_2 <= 2:
                    if use_sozai.s2_3_name_1 != "" and use_sozai.s2_3_num_1 != 0:
                        use_sozai_list.setdefault(use_sozai.s2_3_name_1, 0)
                        use_sozai_list[use_sozai.s2_3_name_1] += use_sozai.s2_3_num_1
                    if use_sozai.s2_3_name_2 != "" and use_sozai.s2_3_num_2!= 0:
                        use_sozai_list.setdefault(use_sozai.s2_3_name_2, 0)
                        use_sozai_list[use_sozai.s2_3_name_2] += use_sozai.s2_3_num_2
                    if use_sozai.s2_3_name_3 != "" and use_sozai.s2_3_num_3 != 0:
                        use_sozai_list.setdefault(use_sozai.s2_3_name_3, 0)
                        use_sozai_list[use_sozai.s2_3_name_3] += use_sozai.s2_3_num_3
                    if use_sozai.s2_3_name_4 != "" and use_sozai.s2_3_num_4 != 0:
                        use_sozai_list.setdefault(use_sozai.s2_3_name_4, 0)
                        use_sozai_list[use_sozai.s2_3_name_4] += use_sozai.s2_3_num_4
                if savant.skill_2 <= 1:
                    if use_sozai.s1_2_name_1 != "" and use_sozai.s1_2_num_1 != 0:
                        use_sozai_list.setdefault(use_sozai.s1_2_name_1, 0)
                        use_sozai_list[use_sozai.s1_2_name_1] += use_sozai.s1_2_num_1
                    if use_sozai.s1_2_name_2 != "" and use_sozai.s1_2_num_2!= 0:
                        use_sozai_list.setdefault(use_sozai.s1_2_name_2, 0)
                        use_sozai_list[use_sozai.s1_2_name_2] += use_sozai.s1_2_num_2
                    if use_sozai.s1_2_name_3 != "" and use_sozai.s1_2_num_3 != 0:
                        use_sozai_list.setdefault(use_sozai.s1_2_name_3, 0)
                        use_sozai_list[use_sozai.s1_2_name_3] += use_sozai.s1_2_num_3
                
                if savant.skill_3 <= 8:
                    if use_sozai.s8_9_name_1 != "" and use_sozai.s8_9_num_1 != 0:
                        use_sozai_list.setdefault(use_sozai.s8_9_name_1, 0)
                        use_sozai_list[use_sozai.s8_9_name_1] += use_sozai.s8_9_num_1
                    if use_sozai.s8_9_name_2 != "" and use_sozai.s8_9_num_2!= 0:
                        use_sozai_list.setdefault(use_sozai.s8_9_name_2, 0)
                        use_sozai_list[use_sozai.s8_9_name_2] += use_sozai.s8_9_num_2
                if savant.skill_3 <= 7:
                    if use_sozai.s7_8_name_1 != "" and use_sozai.s7_8_num_1 != 0:
                        use_sozai_list.setdefault(use_sozai.s7_8_name_1, 0)
                        use_sozai_list[use_sozai.s7_8_name_1] += use_sozai.s7_8_num_1
                    if use_sozai.s7_8_name_2 != "" and use_sozai.s7_8_num_2!= 0:
                        use_sozai_list.setdefault(use_sozai.s7_8_name_2, 0)
                        use_sozai_list[use_sozai.s7_8_name_2] += use_sozai.s7_8_num_2
                if savant.skill_3 <= 6:
                    if use_sozai.s6_7_name_1 != "" and use_sozai.s6_7_num_1 != 0:
                        use_sozai_list.setdefault(use_sozai.s6_7_name_1, 0)
                        use_sozai_list[use_sozai.s6_7_name_1] += use_sozai.s6_7_num_1
                    if use_sozai.s6_7_name_2 != "" and use_sozai.s6_7_num_2!= 0:
                        use_sozai_list.setdefault(use_sozai.s6_7_name_2, 0)
                        use_sozai_list[use_sozai.s6_7_name_2] += use_sozai.s6_7_num_2
                    if use_sozai.s6_7_name_3 != "" and use_sozai.s6_7_num_3 != 0:
                        use_sozai_list.setdefault(use_sozai.s6_7_name_3, 0)
                        use_sozai_list[use_sozai.s6_7_name_3] += use_sozai.s6_7_num_3
                    if use_sozai.s6_7_name_4 != "" and use_sozai.s6_7_num_4 != 0:
                        use_sozai_list.setdefault(use_sozai.s6_7_name_4, 0)
                        use_sozai_list[use_sozai.s6_7_name_4] += use_sozai.s6_7_num_4
                if savant.skill_3 <= 5:
                    if use_sozai.s5_6_name_1 != "" and use_sozai.s5_6_num_1 != 0:
                        use_sozai_list.setdefault(use_sozai.s5_6_name_1, 0)
                        use_sozai_list[use_sozai.s5_6_name_1] += use_sozai.s5_6_num_1
                    if use_sozai.s5_6_name_2 != "" and use_sozai.s5_6_num_2!= 0:
                        use_sozai_list.setdefault(use_sozai.s5_6_name_2, 0)
                        use_sozai_list[use_sozai.s5_6_name_2] += use_sozai.s5_6_num_2
                    if use_sozai.s5_6_name_3 != "" and use_sozai.s5_6_num_3 != 0:
                        use_sozai_list.setdefault(use_sozai.s5_6_name_3, 0)
                        use_sozai_list[use_sozai.s5_6_name_3] += use_sozai.s5_6_num_3
                if savant.skill_3 <= 4:
                    if use_sozai.s4_5_name_1 != "" and use_sozai.s4_5_num_1 != 0:
                        use_sozai_list.setdefault(use_sozai.s4_5_name_1, 0)
                        use_sozai_list[use_sozai.s4_5_name_1] += use_sozai.s4_5_num_1
                    if use_sozai.s4_5_name_2 != "" and use_sozai.s4_5_num_2!= 0:
                        use_sozai_list.setdefault(use_sozai.s4_5_name_2, 0)
                        use_sozai_list[use_sozai.s4_5_name_2] += use_sozai.s4_5_num_2
                    if use_sozai.s4_5_name_3 != "" and use_sozai.s4_5_num_3 != 0:
                        use_sozai_list.setdefault(use_sozai.s4_5_name_3, 0)
                        use_sozai_list[use_sozai.s4_5_name_3] += use_sozai.s4_5_num_3
                    if use_sozai.s4_5_name_4 != "" and use_sozai.s4_5_num_4 != 0:
                        use_sozai_list.setdefault(use_sozai.s4_5_name_4, 0)
                        use_sozai_list[use_sozai.s4_5_name_4] += use_sozai.s4_5_num_4
                if savant.skill_3 <= 3:
                    if use_sozai.s3_4_name_1 != "" and use_sozai.s3_4_num_1 != 0:
                        use_sozai_list.setdefault(use_sozai.s3_4_name_1, 0)
                        use_sozai_list[use_sozai.s3_4_name_1] += use_sozai.s3_4_num_1
                    if use_sozai.s3_4_name_2 != "" and use_sozai.s3_4_num_2!= 0:
                        use_sozai_list.setdefault(use_sozai.s3_4_name_2, 0)
                        use_sozai_list[use_sozai.s3_4_name_2] += use_sozai.s3_4_num_2
                    if use_sozai.s3_4_name_3 != "" and use_sozai.s3_4_num_3 != 0:
                        use_sozai_list.setdefault(use_sozai.s3_4_name_3, 0)
                        use_sozai_list[use_sozai.s3_4_name_3] += use_sozai.s3_4_num_3
                if savant.skill_3 <= 2:
                    if use_sozai.s2_3_name_1 != "" and use_sozai.s2_3_num_1 != 0:
                        use_sozai_list.setdefault(use_sozai.s2_3_name_1, 0)
                        use_sozai_list[use_sozai.s2_3_name_1] += use_sozai.s2_3_num_1
                    if use_sozai.s2_3_name_2 != "" and use_sozai.s2_3_num_2!= 0:
                        use_sozai_list.setdefault(use_sozai.s2_3_name_2, 0)
                        use_sozai_list[use_sozai.s2_3_name_2] += use_sozai.s2_3_num_2
                    if use_sozai.s2_3_name_3 != "" and use_sozai.s2_3_num_3 != 0:
                        use_sozai_list.setdefault(use_sozai.s2_3_name_3, 0)
                        use_sozai_list[use_sozai.s2_3_name_3] += use_sozai.s2_3_num_3
                    if use_sozai.s2_3_name_4 != "" and use_sozai.s2_3_num_4 != 0:
                        use_sozai_list.setdefault(use_sozai.s2_3_name_4, 0)
                        use_sozai_list[use_sozai.s2_3_name_4] += use_sozai.s2_3_num_4
                if savant.skill_3 <= 1:
                    if use_sozai.s1_2_name_1 != "" and use_sozai.s1_2_num_1 != 0:
                        use_sozai_list.setdefault(use_sozai.s1_2_name_1, 0)
                        use_sozai_list[use_sozai.s1_2_name_1] += use_sozai.s1_2_num_1
                    if use_sozai.s1_2_name_2 != "" and use_sozai.s1_2_num_2!= 0:
                        use_sozai_list.setdefault(use_sozai.s1_2_name_2, 0)
                        use_sozai_list[use_sozai.s1_2_name_2] += use_sozai.s1_2_num_2
                    if use_sozai.s1_2_name_3 != "" and use_sozai.s1_2_num_3 != 0:
                        use_sozai_list.setdefault(use_sozai.s1_2_name_3, 0)
                        use_sozai_list[use_sozai.s1_2_name_3] += use_sozai.s1_2_num_3
                
    # 足りない素材の数確認
    over_sozai_list = []
    over_savant_list = {}
    # over_sozai_list["test"] = {"test":"2"}

    for sozai_name, num in use_sozai_list.items():
        for val in sozai_list:
            if val.name == sozai_name:
                if val.num < num:
                    over_sozai_list.append(val.name)
    
    for No in int_skill_up_list:
        savant = Savant_list.query.get(No)
        use_sozai = Use_sozai.query.get(No)
        over_savant_list[savant.NO] = {}

        for name in over_sozai_list:
            if savant.skill_1 <= 8:
                if name == use_sozai.s8_9_name_1:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s8_9_num_1
                if name == use_sozai.s8_9_name_2:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s8_9_num_2
            if savant.skill_1 <= 7:
                if name == use_sozai.s7_8_name_1:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s7_8_num_1
                if name == use_sozai.s7_8_name_2:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s7_8_num_2
            if savant.skill_1 <= 6:
                if name == use_sozai.s6_7_name_1:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s6_7_num_1
                if name == use_sozai.s6_7_name_2:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s6_7_num_2
                if name == use_sozai.s6_7_name_3:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s6_7_num_3
                if name == use_sozai.s6_7_name_4:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s6_7_num_4
            if savant.skill_1 <= 5:
                if name == use_sozai.s5_6_name_1:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s5_6_num_1
                if name == use_sozai.s5_6_name_2:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s5_6_num_2
                if name == use_sozai.s5_6_name_3:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s5_6_num_3
            if savant.skill_1 <= 4:
                if name == use_sozai.s4_5_name_1:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s4_5_num_1
                if name == use_sozai.s4_5_name_2:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s4_5_num_2
                if name == use_sozai.s4_5_name_3:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s4_5_num_3
                if name == use_sozai.s4_5_name_4:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s4_5_num_4
            if savant.skill_1 <= 3:
                if name == use_sozai.s3_4_name_1:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s3_4_num_1
                if name == use_sozai.s3_4_name_2:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s3_4_num_2
                if name == use_sozai.s3_4_name_3:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s3_4_num_3
            if savant.skill_1 <= 2:
                if name == use_sozai.s2_3_name_1:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s2_3_num_1
                if name == use_sozai.s2_3_name_2:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s2_3_num_2
                if name == use_sozai.s2_3_name_3:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s2_3_num_3
                if name == use_sozai.s2_3_name_4:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s2_3_num_4
            if savant.skill_1 <= 1:
                if name == use_sozai.s1_2_name_1:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s1_2_num_1
                if name == use_sozai.s1_2_name_2:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s1_2_num_2
                if name == use_sozai.s1_2_name_3:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s1_2_num_3

            if savant.skill_2 <= 8:
                if name == use_sozai.s8_9_name_1:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s8_9_num_1
                if name == use_sozai.s8_9_name_2:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s8_9_num_2
            if savant.skill_2 <= 7:
                if name == use_sozai.s7_8_name_1:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s7_8_num_1
                if name == use_sozai.s7_8_name_2:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s7_8_num_2
            if savant.skill_2 <= 6:
                if name == use_sozai.s6_7_name_1:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s6_7_num_1
                if name == use_sozai.s6_7_name_2:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s6_7_num_2
                if name == use_sozai.s6_7_name_3:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s6_7_num_3
                if name == use_sozai.s6_7_name_4:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s6_7_num_4
            if savant.skill_2 <= 5:
                if name == use_sozai.s5_6_name_1:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s5_6_num_1
                if name == use_sozai.s5_6_name_2:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s5_6_num_2
                if name == use_sozai.s5_6_name_3:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s5_6_num_3
            if savant.skill_2 <= 4:
                if name == use_sozai.s4_5_name_1:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s4_5_num_1
                if name == use_sozai.s4_5_name_2:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s4_5_num_2
                if name == use_sozai.s4_5_name_3:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s4_5_num_3
                if name == use_sozai.s4_5_name_4:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s4_5_num_4
            if savant.skill_2 <= 3:
                if name == use_sozai.s3_4_name_1:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s3_4_num_1
                if name == use_sozai.s3_4_name_2:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s3_4_num_2
                if name == use_sozai.s3_4_name_3:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s3_4_num_3
            if savant.skill_2 <= 2:
                if name == use_sozai.s2_3_name_1:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s2_3_num_1
                if name == use_sozai.s2_3_name_2:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s2_3_num_2
                if name == use_sozai.s2_3_name_3:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s2_3_num_3
                if name == use_sozai.s2_3_name_4:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s2_3_num_4
            if savant.skill_2 <= 1:
                if name == use_sozai.s1_2_name_1:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s1_2_num_1
                if name == use_sozai.s1_2_name_2:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s1_2_num_2
                if name == use_sozai.s1_2_name_3:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s1_2_num_3

            if savant.skill_3 <= 8:
                if name == use_sozai.s8_9_name_1:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s8_9_num_1
                if name == use_sozai.s8_9_name_2:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s8_9_num_2
            if savant.skill_3 <= 7:
                if name == use_sozai.s7_8_name_1:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s7_8_num_1
                if name == use_sozai.s7_8_name_2:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s7_8_num_2
            if savant.skill_3 <= 6:
                if name == use_sozai.s6_7_name_1:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s6_7_num_1
                if name == use_sozai.s6_7_name_2:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s6_7_num_2
                if name == use_sozai.s6_7_name_3:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s6_7_num_3
                if name == use_sozai.s6_7_name_4:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s6_7_num_4
            if savant.skill_3 <= 5:
                if name == use_sozai.s5_6_name_1:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s5_6_num_1
                if name == use_sozai.s5_6_name_2:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s5_6_num_2
                if name == use_sozai.s5_6_name_3:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s5_6_num_3
            if savant.skill_3 <= 4:
                if name == use_sozai.s4_5_name_1:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s4_5_num_1
                if name == use_sozai.s4_5_name_2:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s4_5_num_2
                if name == use_sozai.s4_5_name_3:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s4_5_num_3
                if name == use_sozai.s4_5_name_4:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s4_5_num_4
            if savant.skill_3 <= 3:
                if name == use_sozai.s3_4_name_1:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s3_4_num_1
                if name == use_sozai.s3_4_name_2:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s3_4_num_2
                if name == use_sozai.s3_4_name_3:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s3_4_num_3
            if savant.skill_3 <= 2:
                if name == use_sozai.s2_3_name_1:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s2_3_num_1
                if name == use_sozai.s2_3_name_2:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s2_3_num_2
                if name == use_sozai.s2_3_name_3:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s2_3_num_3
                if name == use_sozai.s2_3_name_4:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s2_3_num_4
            if savant.skill_3 <= 1:
                if name == use_sozai.s1_2_name_1:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s1_2_num_1
                if name == use_sozai.s1_2_name_2:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s1_2_num_2
                if name == use_sozai.s1_2_name_3:
                    over_savant_list[savant.NO].setdefault(name, 0)
                    over_savant_list[savant.NO][name] += use_sozai.s1_2_num_3
                    



    return render_template('sozai_num.html',sozai_list=sozai_list,use_sozai_list=use_sozai_list,savant_list=savant_list,int_skill_up_list=int_skill_up_list,over_savant_list=over_savant_list,class_list=class_list)

#各種表表示
@app.route('/meter', methods=["POST","GET"])
def meter_view():

    # 年別召喚
    day_list = {}

    #ここを編集すると年が伸びます
    for year in range(2016, 2023):
        for month in range(1, 13):
            if month <= 9:
                savant = Savant_list.query.filter(Savant_list.day.like(str(year) + "-0" + str(month) + "%"))
            else:
                savant = Savant_list.query.filter(Savant_list.day.like(str(year) + "-" + str(month) + "%"))

            day_list["c" + str(year) + "_" +str(month)] = savant.count()
            day_list.setdefault("c" + str(year) + "_sum", 0)
            day_list["c" + str(year) + "_sum"] += savant.count()


    # 宝具種別
    savant = Savant_list.query.filter(Savant_list.day != None)

    hougu_list = {}
    hougu_list["buster_single"] = savant.filter(Savant_list.hougu_color.like("バスター")).filter(Savant_list.hougu_syurui.like("単体")).count()
    hougu_list["buster_all"] = savant.filter(Savant_list.hougu_color.like("バスター")).filter(Savant_list.hougu_syurui.like("全体")).count()
    hougu_list["buster_support"] = savant.filter(Savant_list.hougu_color.like("バスター")).filter(Savant_list.hougu_syurui.like("サポート")).count()
    hougu_list["arts_single"] = savant.filter(Savant_list.hougu_color.like("アーツ")).filter(Savant_list.hougu_syurui.like("単体")).count()
    hougu_list["arts_all"] = savant.filter(Savant_list.hougu_color.like("アーツ")).filter(Savant_list.hougu_syurui.like("全体")).count()
    hougu_list["arts_support"] = savant.filter(Savant_list.hougu_color.like("アーツ")).filter(Savant_list.hougu_syurui.like("サポート")).count()
    hougu_list["quick_single"] = savant.filter(Savant_list.hougu_color.like("クイック")).filter(Savant_list.hougu_syurui.like("単体")).count()
    hougu_list["quick_all"] = savant.filter(Savant_list.hougu_color.like("クイック")).filter(Savant_list.hougu_syurui.like("全体")).count()
    hougu_list["quick_support"] = savant.filter(Savant_list.hougu_color.like("クイック")).filter(Savant_list.hougu_syurui.like("サポート")).count()
    hougu_list["buster_sum"] = savant.filter(Savant_list.hougu_color.like("バスター")).count()
    hougu_list["arts_sum"] = savant.filter(Savant_list.hougu_color.like("アーツ")).count()
    hougu_list["quick_sum"] = savant.filter(Savant_list.hougu_color.like("クイック")).count()
    hougu_list["single_sum"] = savant.filter(Savant_list.hougu_syurui.like("単体")).count()
    hougu_list["all_sum"] = savant.filter(Savant_list.hougu_syurui.like("全体")).count()
    hougu_list["support_sum"] = savant.filter(Savant_list.hougu_syurui.like("サポート")).count()


    # 宝具レベル別
    hougu_lv_list = {}
    for star in range(1, 6):
        hougu_lv_list["h" + str(star) + "_S_sum"] = savant.filter(Savant_list.star==star).count()
        for Lv in range(1, 6):
            hougu_lv_list["h" + str(star) + "_" + str(Lv)] = savant.filter(Savant_list.star==star).filter(Savant_list.hougu_lv==Lv).count()
            hougu_lv_list["h" + str(Lv) + "_L_sum"] = savant.filter(Savant_list.hougu_lv==Lv).count()

    # アイテム使用数
    item_num = {}
    item_num["seihai_savant"] = savant.filter(Savant_list.seihai > 0).count()
    item_num["skill_savant"] = savant.filter(Savant_list.skill_1==10).filter(Savant_list.skill_2==10).filter(Savant_list.skill_3==10).count()
    item_num["skill_num"] = savant.filter(Savant_list.skill_1==10).count() + savant.filter(Savant_list.skill_2==10).count() + savant.filter(Savant_list.skill_3==10).count()
    item_num["999_num"] = savant.filter(Savant_list.skill_1==9).filter(Savant_list.skill_2==9).filter(Savant_list.skill_3==9).count()
    item_num["kizuna_10"] = savant.filter(Savant_list.kizuna>=10).count()

    seihai_sv = savant.filter(Savant_list.seihai > 0)
    item_num["seihai_num"] = 0
    for val in seihai_sv:
        item_num["seihai_num"] += val.seihai

    return render_template('meter.html',day_list=day_list,hougu_list=hougu_list,hougu_lv_list=hougu_lv_list,item_num=item_num)

# 所持素材登録フォーム
@app.route('/sozai_up', methods=["GET"])
def sozai_up():

    sozai_list = Sozai.query.order_by(Sozai.id.asc()).all()

    return render_template('sozai_up.html',sozai_list=sozai_list)

# 所持素材登録
@app.route('/sozai_up_grade', methods=["POST"])
def sozai_up_grade():

    sozai_list = Sozai.query.order_by(Sozai.id.asc()).all()

    for val in sozai_list:
        num = request.form.get(val.name) or 0
        sozai = Sozai.query.filter(Sozai.name==val.name).first()
        sozai.num = int(num)
        db.session.merge(sozai)

    db.session.commit()

    flash('更新しました', 'success')
    return redirect(url_for('sozai_view'))

# 新規素材登録
@app.route('/sozai_new', methods=["GET"])
def sozai_new():

    sozai_shurui = db.session.query(Sozai).group_by(Sozai.shurui).all()
    sozai_list = Sozai.query.order_by(Sozai.id.asc()).all()

    return render_template('sozai_new.html',sozai_list=sozai_list,sozai_shurui=sozai_shurui)

# 素材名更新
@app.route('/sozai_name_up_grade', methods=["POST"])
def sozai_name_up():

    sozai_list = Sozai.query.order_by(Sozai.id.asc())

    try:
        for val in sozai_list:
            name = request.form.get(str(val.id)) or ""
            sozai = Sozai.query.filter(Sozai.id==val.id).first()
            if name != "":
                sozai.name = name
                print(val.id)
                print(name)
                db.session.merge(sozai)
            else:
                if sozai:
                    db.session.delete(sozai)

        db.session.commit()
    except Exception as e:
        flash(e, 'error')
        return redirect(url_for('sozai_new'))

    flash('更新しました', 'success')
    return redirect(url_for('sozai_view'))

# 素材登録
@app.route('/sozai_create', methods=["POST"])
def sozai_create():

    try:
        shurui = request.form.get("shurui")
        name = request.form.get("name")
    except Exception as e:
        flash(e, 'error')
        return redirect(url_for('sozai_new'))

    sozai_end = Sozai.query.order_by(Sozai.id.desc()).first()
    end_id = int(sozai_end.id) + 1

    sozai = Sozai(
        id = end_id,
        shurui = shurui,
        name = name,
        num = 0
    )

    try:    
        db.session.add(sozai)
        db.session.commit()
    except Exception as e:
        flash(e, 'error')
        return redirect(url_for('sozai_new'))

    session.pop('input_list', None)

    flash('登録しました', 'success')
    return redirect(url_for('sozai_view'))

# サーヴァント削除
@app.route('/delete/<int:NO>', methods=["POST"])
def delete(NO):

    savant = Savant_list.query.get(NO)

    try:
        if savant:
            db.session.delete(savant)
            db.session.commit()
    except Exception as e:
        flash(e, 'error')
        return redirect(url_for('list_view'))

    flash('削除しました', 'success')
    return redirect(url_for('list_view'))

@app.route('/reset/sozai', methods=["POST"])
def sozai_reset():

    sozai_list = Sozai.query.order_by(Sozai.id.asc()).all()

    for val in sozai_list:
        val.num = 0
        db.session.merge(val)

    db.session.commit()

    flash('初期化しました', 'success')
    return redirect(url_for('sozai_view'))

