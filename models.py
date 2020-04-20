import os
import json

from sqlalchemy import Column, Integer, String, Date, Enum, create_engine
from flask_sqlalchemy import SQLAlchemy

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
		binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
	app.config["SQLALCHEMY_DATABASE_URI"] = database_path
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	db.app = app
	db.init_app(app)
	#db.create_all()


'''
Movie
'''
class Movie(db.Model):  
	__tablename__ = 'movies'
	
	id = Column(Integer, primary_key=True)
	title = Column(String, nullable=False)
	release = Column(Date, nullable=False)
	
	def __init__(self, title, release):
		self.title = title
		self.release = release
	
	def insert(self):
		db.session.add(self)
		db.session.commit()
	
	def update(self):
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()
	
	def format(self):
		return {
			'id': self.id,
			'title': self.title,
			'release': self.release.strftime('%Y-%m-%d')
		}

'''
Actor
'''
class Actor(db.Model):  
	__tablename__ = 'actors'
	
	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	age = Column(Integer, nullable=False)
	gender = Column(Enum('male', 'female'), nullable=False)
	
	def __init__(self, name, age, gender):
		self.name = name
		self.age = age
		self.gender = gender
	
	def insert(self):
		db.session.add(self)
		db.session.commit()
	
	def update(self):
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()
	
	def format(self):
		return {
			'id': self.id,
			'name': self.name,
			'age': self.age,
			'gender': self.gender
		}
