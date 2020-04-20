import os
from datetime import date, datetime

from models import db, setup_db, Movie, Actor
from auth import requires_auth, AuthError

from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__)
	setup_db(app)
	CORS(app)
	
	@app.after_request
	def after_request(response):
		response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
		response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
		return response
	
	# Movie Endpoints
	# ===============
	@app.route('/movies')
	@requires_auth('get:movies')
	def get_movies(jwt_payload):
		movies = Movie.query.all()
		
		movies_f = [m.format() for m in movies]
		
		return jsonify({
		'success': True,
		'movies': movies_f
		})
	
	@app.route('/movies', methods=['POST'])
	@requires_auth('post:movies')
	def post_movie(jwt_payload):
		data = request.get_json()
		
		if data == None:
			abort(400)
		
		if 'title' not in data:
			abort(400)
		
		if 'release' not in data:
			abort(400)
		
		try:
			title = str(data.get('title'))
			release = datetime.strptime(data.get('release'), '%Y-%m-%d').date()
		except:
			abort(400)
		
		movie = Movie(title, release)
		movie.insert()
		
		movie_f = [movie.format()]
		
		return jsonify({
		'success': True,
		'movies': movie_f
		})
	
	@app.route('/movies/<int:id>', methods=['PATCH'])
	@requires_auth('patch:movies')
	def patch_movie(jwt_payload, id):
		data = request.get_json()
		
		if data == None:
			abort(400)
		
		movie = Movie.query.get(id)
		if movie == None:
			abort(404)
		
		if 'title' in data:
			try:
				movie.title = str(data.get('title'))
			except:
				abort(400)
		
		if 'release' in data:
			try:
				movie.release = datetime.strptime(data.get('release'), '%Y-%m-%d').date()
			except:
				abort(400)
		
		movie.update()
		
		movie_f = [movie.format()]
		
		return jsonify({
		'success': True,
		'movies': movie_f
		})
	
	@app.route('/movies/<int:id>', methods=['DELETE'])
	@requires_auth('delete:movies')
	def del_movie(jwt_payload, id):
		movie = Movie.query.get(id)
		
		if movie == None:
			abort(404)
		
		movie.delete()
		
		return jsonify({
		'success': True,
		'delete': id
		})
	
	# Actor Endpoints
	# ===============
	@app.route('/actors')
	@requires_auth('get:actors')
	def get_actors(jwt_payload):
		actors = Actor.query.all()
		
		actors_f = [a.format() for a in actors]
		
		return jsonify({
		'success': True,
		'actors': actors_f
		})
	
	@app.route('/actors', methods=['POST'])
	@requires_auth('post:actors')
	def post_actor(jwt_payload):
		data = request.get_json()
		
		if data == None:
			abort(400)
		
		if 'name' not in data:
			abort(400)
		
		if 'age' not in data:
			abort(400)
			
		if 'gender' not in data:
			abort(400)
		
		try:
			name = str(data.get('name'))
			age = int(data.get('age'))
			gender = str(data.get('gender'))
		except:
			abort(400)
		
		actor = Actor(name, age, gender)
		actor.insert()
		
		actor_f = [actor.format()]
		
		return jsonify({
		'success': True,
		'actors': actor_f
		})
	
	@app.route('/actors/<int:id>', methods=['PATCH'])
	@requires_auth('patch:actors')
	def patch_actor(jwt_payload, id):
		data = request.get_json()
		
		if data == None:
			abort(400)
		
		actor = Actor.query.get(id)
		if actor == None:
			abort(404)
		
		if 'name' in data:
			try:
				actor.name = str(data.get('name'))
			except:
				abort(400)
		
		if 'age' in data:
			try:
				actor.age = int(data.get('age'))
			except:
				abort(400)
		
		if 'gender' in data:
			try:
				actor.gender = str(data.get('gender'))
			except:
				abort(400)
		
		actor.update()
		
		actor_f = [actor.format()]
		
		return jsonify({
		'success': True,
		'actors': actor_f
		})
	
	@app.route('/actors/<int:id>', methods=['DELETE'])
	@requires_auth('delete:actors')
	def del_actor(jwt_payload, id):
		actor = Actor.query.get(id)
		
		if actor == None:
			abort(404)
		
		actor.delete()
		
		return jsonify({
		'success': True,
		'delete': id
		})
	
	# Error handlers
	# ==============
	@app.errorhandler(400)
	def bad_request(error):
		return jsonify({
		"success": False, 
		"error": 400,
		"message": "bad request"
		}), 400
	
	@app.errorhandler(404)
	def not_found(error):
		return jsonify({
		"success": False, 
		"error": 404,
		"message": "not found"
		}), 404

	@app.errorhandler(422)
	def unprocessable(error):
		return jsonify({
		"success": False, 
		"error": 422,
		"message": "unprocessable"
		}), 422

	@app.errorhandler(AuthError)
	def auth_error(error):
		return jsonify({
		'success': False,
		'code': error.status_code,
		'message': error.error
		}), error.status_code
	
	return app

APP = create_app()

if __name__ == '__main__':
	APP.run(host='0.0.0.0', port=8080, debug=True)
