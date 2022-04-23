from sys import addaudithook
from werkzeug.utils import header_property
from lib.db import db

class Savant_list(db.Model):

	__tablename__ = 'savant_list'

	name = db.Column(db.String(50), nullable=False)
	NO = db.Column(db.Integer, primary_key=True)
	class_s = db.Column(db.String(10), nullable=False)
	star = db.Column(db.Integer, nullable=False)
	hougu_lv = db.Column(db.Integer, nullable=False)
	zokusei_1 = db.Column(db.String(10), nullable=False)
	zokusei_2 = db.Column(db.String(10), nullable=False)
	shincho = db.Column(db.String(20), nullable=False)
	taiju = db.Column(db.String(20), nullable=False)
	sex = db.Column(db.String(10), nullable=False)
	hougu_name = db.Column(db.String(80), nullable=False)
	hougu_syurui = db.Column(db.String(10), nullable=False)
	hougu_color = db.Column(db.String(10), nullable=False)
	day = db.Column(db.String(20))
	source = db.Column(db.String(100), nullable=False)
	country = db.Column(db.String(100), nullable=False)
	st1 = db.Column(db.String(10), nullable=False)
	st2 = db.Column(db.String(10), nullable=False)
	st3 = db.Column(db.String(10), nullable=False)
	st4 = db.Column(db.String(10), nullable=False)
	st5 = db.Column(db.String(10), nullable=False)
	st6 = db.Column(db.String(10), nullable=False)
	me = db.Column(db.String(50))
	you = db.Column(db.String(50))
	he_she = db.Column(db.String(50))
	master = db.Column(db.String(50))
	seihai = db.Column(db.Integer)
	url = db.Column(db.String(400))
	skill_1 = db.Column(db.Integer)
	skill_2 = db.Column(db.Integer)
	skill_3 = db.Column(db.Integer)
	hp = db.Column(db.Integer)
	atk = db.Column(db.Integer)
	memo = db.Column(db.String(500))
	kizuna = db.Column(db.Integer)


	def __init__(self, name, NO, class_s, star, hougu_lv, zokusei_1, zokusei_2, shincho, taiju, sex, hougu_name, hougu_syurui, hougu_color, day, source, country, st1, st2, st3, st4, st5, st6, me, you, he_she, master, seihai, url, skill_1, skill_2, skill_3, hp, atk, memo, kizuna):
		self.name = name
		self.NO = NO
		self.class_s = class_s
		self.star = star
		self.hougu_lv = hougu_lv
		self.zokusei_1 = zokusei_1
		self.zokusei_2 = zokusei_2
		self.shincho = shincho
		self.taiju = taiju
		self.sex = sex
		self.hougu_name = hougu_name
		self.hougu_syurui = hougu_syurui
		self.hougu_color = hougu_color
		self.day = day
		self.source = source
		self.country = country
		self.st1 = st1
		self.st2 = st2
		self.st3 = st3
		self.st4 = st4
		self.st5 = st5
		self.st6 = st6
		self.me = me
		self.you = you
		self.he_she = he_she
		self.master = master
		self.seihai = seihai
		self.url = url
		self.skill_1 = skill_1
		self.skill_2 = skill_2
		self.skill_3 = skill_3
		self.hp = hp 
		self.atk = atk 
		self.memo = memo
		self.kizuna = kizuna








