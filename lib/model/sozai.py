from lib.db import db

class Sozai(db.Model):

	__tablename__ = 'sozai'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	shurui = db.Column(db.String(50), nullable=False)
	num = db.Column(db.Integer)

	def __init__(self, id, name, shurui, num):
		self.id = id
		self.name = name
		self.shurui = shurui
		self.num = num