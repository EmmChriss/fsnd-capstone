available at: [https://emmchris-fsnd-capstone.herokuapp.com/]

## Abbreviations
Casting Assistant = CA
Casting Director = CD
Executive Producer = EP

## Environment
I use a virtual environment and recommend you do the same
```
virtualenv env
pip install -r requirements.txt
```

Necessary environment can be set up like so `source setup.sh`

## Testing
Auth0 jwts available through `source setup.sh`
Testing is done like so `python test_app.py`

## Local server
After setting up the environment a local server can be started with `flask run`

## Endpoints
Note: parts containing `[...]` describe necessary authorization to request the following action
```
[CA or higher]
GET /movies 
 - returns the list of movies

[CA or higher]
GET /actors
 - returns the list of actors

[EP]
POST /movies
 - takes json-serialized string cotaining movie data
 - returns the created movie

[CD or higher]
PATCH /movies/<int:id>
 - takes json-serialized string cotaining movie data
 - modifies data stored about {id}
 - returns the modified movie

[EP]
DELETE /movies/<int:id>
 - deletes movie entry {id}
 - returns id of deleted movie

[CD or higher]
POST /actors
 - takes json-serialized string cotaining actor data
 - returns the created actor

[CD or higher]
PATCH /actors/<int:id>
 - takes json-serialized string cotaining actor data
 - modifies data stored about {id}
 - returns the modified actor

[CD or higher]
DELETE /actors/<int:id>
 - deletes actor entry {id}
 - returns id of deleted actor
```
