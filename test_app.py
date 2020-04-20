import os
import unittest
import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor


class CapstoneTestCase(unittest.TestCase):
	"""This class represents the trivia test case"""

	def setUp(self):
		"""Define test variables and initialize app."""
		self.app = create_app()
		self.client = self.app.test_client
		self.database_path = os.environ['DATABASE_URL']
		setup_db(self.app, self.database_path)
		
		self.HEADERS_UNAUTHENTICATED = {}
		self.HEADERS_CA = {
			'Authorization': 'Bearer ' + os.environ['TEST_TOKEN_CA']
		}
		self.HEADERS_CD = {
			'Authorization': 'Bearer ' + os.environ['TEST_TOKEN_CD']
		}
		self.HEADERS_EP = {
			'Authorization': 'Bearer ' + os.environ['TEST_TOKEN_EP']
		}
		
		# binds the app to the current context
		with self.app.app_context():
			self.db = SQLAlchemy()
			self.db.init_app(self.app)
			# create all tables
			self.db.create_all()
	
	def tearDown(self):
		"""Executed after reach test"""
		pass
	
	# Common db actions
	# =================
	def sample_movie(self):
		return Movie('Spiderman: Homecoming', datetime.strptime('2017-07-07', '%Y-%m-%d').date())
	
	def sample_actor(self):
		return Actor('Ben', 35, 'male')
	
	def movie_id(self, id):
		return Movie.query.get(id)
	
	def actor_id(self, id):
		return Actor.query.get(id)
	
	# Unauthenticated
	# ===============
	def test_get_movies_e401(self):
		res = self.client().get('/movies', headers=self.HEADERS_UNAUTHENTICATED)
		self.assertEqual(res.status_code, 401)
	
	# Casting Assistant
	# =================
	def test_get_movies(self):
		res = self.client().get('/movies', headers=self.HEADERS_CA)
		self.assertEqual(res.status_code, 200)
		data = json.loads(res.data)
		self.assertFalse(data == None)
		self.assertTrue('movies' in data)
	
	def test_get_actors(self):
		res = self.client().get('/actors', headers=self.HEADERS_CA)
		self.assertEqual(res.status_code, 200)
		data = json.loads(res.data)
		self.assertFalse(data == None)
		self.assertTrue('actors' in data)
	
	def test_post_actors_e403(self):
		res = self.client().post('/actors', headers=self.HEADERS_CA)
		self.assertEqual(res.status_code, 403)
	
	def test_patch_movies_e403(self):
		res = self.client().patch('/movies/1', headers=self.HEADERS_CA)
		self.assertEqual(res.status_code, 403)
		
	def test_patch_actors_e403(self):
		res = self.client().patch('/actors/1', headers=self.HEADERS_CA)
		self.assertEqual(res.status_code, 403)
	
	def test_del_actors_e403(self):
		res = self.client().delete('/actors/1', headers=self.HEADERS_CA)
		self.assertEqual(res.status_code, 403)
	
	# Casting Director
	# ================
	def test_post_actors(self):
		data = {
		'name': 'Lee',
		'age': 63,
		'gender': 'male'
		}
		res = self.client().post('/actors', json=data, headers=self.HEADERS_CD)
		self.assertEqual(res.status_code, 200)
		data = json.loads(res.data)
		self.assertFalse(data == None)
		self.assertTrue('actors' in data)
		self.assertEqual(len(data['actors']), 1)
		self.actor_id(data['actors'][0]['id']).delete()
	
	def test_patch_movies(self):
		movie = self.sample_movie()
		movie.insert()
		data = {
			'release': '2017-07-06'
		}
		res = self.client().patch('/movies/{}'.format(movie.id), json=data, headers=self.HEADERS_EP)
		self.assertEqual(res.status_code, 200)
		data = json.loads(res.data)
		self.assertFalse(data == None)
		self.assertTrue('movies' in data)
		self.assertEqual(len(data['movies']), 1)
		self.assertEqual(data['movies'][0]['release'], '2017-07-06')
		movie.delete()
	
	def test_patch_actors(self):
		actor = self.sample_actor()
		actor.insert()
		data = {
		'name': 'John'
		}
		res = self.client().patch('/actors/{}'.format(actor.id), json=data, headers=self.HEADERS_CD)
		self.assertEqual(res.status_code, 200)
		data = json.loads(res.data)
		self.assertFalse(data == None)
		self.assertTrue('actors' in data)
		self.assertEqual(len(data['actors']), 1)
		self.assertEqual(data['actors'][0]['name'], 'John')
		actor.delete()
	
	def test_del_actors(self):
		actor = self.sample_actor()
		actor.insert()
		res = self.client().delete('/actors/{}'.format(actor.id), headers=self.HEADERS_CD)
		self.assertEqual(res.status_code, 200)
		data = json.loads(res.data)
		self.assertFalse(data == None)
		self.assertTrue('delete' in data)
		self.assertEqual(data['delete'], actor.id)
	
	def test_post_movies_e403(self):
		res = self.client().post('/movies', headers=self.HEADERS_CD)
		self.assertEqual(res.status_code, 403)
	
	def test_del_movies_e403(self):
		res = self.client().delete('/movies/1', headers=self.HEADERS_CD)
		self.assertEqual(res.status_code, 403)
	
	# Executive Producer
	# ==================
	def test_post_movies(self):
		data = {
		'title': 'Spiderman: Homecoming',
		'release': '2017-07-06'
		}
		res = self.client().post('/movies', json=data, headers=self.HEADERS_EP)
		self.assertEqual(res.status_code, 200)
		data = json.loads(res.data)
		self.assertFalse(data == None)
		self.assertTrue('movies' in data)
		self.assertEqual(len(data['movies']), 1)
		self.movie_id(data['movies'][0]['id']).delete()
	
	def test_del_movies(self):
		movie = self.sample_movie()
		movie.insert()
		res = self.client().delete('/movies/{}'.format(movie.id), headers=self.HEADERS_EP)
		self.assertEqual(res.status_code, 200)
		data = json.loads(res.data)
		self.assertFalse(data == None)
		self.assertTrue('delete' in data)
		self.assertEqual(data['delete'], movie.id)

if __name__ == '__main__':
	unittest.main()
