
from django.db import models
from themoviedb import tmdb
from datetime import *	

import urllib
import urllib2
import json
_parse_json = lambda s: json.loads(s)

class Genre(models.Model):
	gid = models.IntegerField()
	name = models.CharField(max_length = 20)
	url = models.CharField(max_length = 100)
	last_modified_by_us = models.DateField()
	
	genre = {}
	def getGenreList():
		url = tmdb.config['urls']['genre.getList']
		etree = tmdb.XmlHandler(url).getEt()
		for cur_result in etree.find("genres").findall("genre"):
			name = cur_result.get("name")
			for item in cur_result.getchildren():
				if item.tag == 'id':
					genre[name] = item.text

class Movie(models.Model):
	mid = models.IntegerField()
	imdb_id = models.IntegerField()
	popularity = models.IntegerField()
	votes = models.IntegerField()
	runtime = models.IntegerField()
	version = models.IntegerField()
	revenue = models.BigIntegerField()
	budget = models.BigIntegerField()
	rating = models.DecimalField(max_digits = 2, decimal_places = 1)
	translated = models.BooleanField()
	adult = models.BooleanField()
	language = models.CharField(max_length = 10)
	original_name = models.CharField(max_length = 100)
	name = models.CharField(max_length = 100)
	alternative_name = models.CharField(max_length = 100)
	type = models.CharField(max_length = 20)
	url = models.CharField(max_length = 100)
	certification = models.CharField(max_length = 10)
	homepage = models.CharField(max_length = 100)
	trailer = models.CharField(max_length = 100)
	overview = models.TextField()
	tagline = models.TextField()
	last_modified_by_tmdb = models.DateField()
	released = models.DateField()
	last_modified_by_us = models.DateField()
	
	#foreign key(s)
	genre = models.ManyToManyField("Genre")
	
	#json encoded fields
	languages_spoken = models.TextField()
	categories = models.TextField()
	keywords = models.TextField()
	studios = models.TextField()
	countries = models.TextField()

	#TODO: puravshah, caching
	def getMovieById(self, mid):
		return tmdb.getMovieInfo(mid)	
	
	def browse(self, order_by, order, topX, gen):
		url = "http://api.themoviedb.org/2.1/Movie.browse/en-US/xml/" + tmdb.config['apikey']
		url += "?order_by=" + str(order_by) + "&order=" + str(order) + "&page=1&per_page=" + str(topX)
		optional = "&release_max=" + str(int(time.time() + 2629743 * 6)) + "&release_min=0"
		url += optional
		
		length = len(gen)
		if length > 0:
			url += "&genres=" + Genre.genre[gen[0]]
		for i in range(1, length):
			url += "," + Genre.genre[gen[i]]
		#print "URL : " + url
		
		etree = tmdb.XmlHandler(url).getEt()
		search_results = tmdb.SearchResults()
		for cur_result in etree.find("movies").findall("movie"):
			cur_movie = tmdb.parseSearchResults(cur_result)
			search_results.append(cur_movie)	
		return search_results
		
	def getLatestMovie(self):
		url = tmdb.config['urls']['movie.getLatest']
		#print "URL Latest : " + url
		etree = tmdb.XmlHandler(url).getEt()
		
		movie = tmdb.Movie()
		for item in etree.find("movie").getchildren():
			movie[item.tag] = item.text
		return movie
	
class User(models.Model):
	username = models.CharField(max_length=128, null=True)
	first_name = models.CharField(max_length=128, null=True)
	last_name = models.CharField(max_length=128, null=True)
	gender = models.CharField(max_length=16, null=True)
	uid = models.CharField(max_length=128, primary_key=True)
	hometown = models.CharField(max_length=2048, null=True)
	languages = models.CharField(max_length=2048, null=True)
	link = models.CharField(max_length=128)
	interested_in = models.CharField(max_length=1024, null=True)
	relationship_status = models.CharField(max_length=1024, null=True)
	religion = models.CharField(max_length=1024, null=True)
	photo_url = models.CharField(max_length=1024)

	#json encoded strings
	friends = models.TextField()
	movies = models.TextField()

	
	last_fetched = models.DateTimeField()
	
	
	def fetch(id, access_token):
		id = str(id)
		batchstr  = [{"method":"get","relative_url":id,"access_token":access_token},
					 {"method":"get","relative_url":id+"/friends","access_token":access_token},
					 {"method":"get","relative_url":id+"/movies","access_token":access_token}]
		args = { "batch" : batchstr,
				 "method" : "POST", 
				 "access_token" : access_token, 
				}
		file = urllib2.urlopen("https://graph.facebook.com/", urllib.urlencode(args))
		resp = _parse_json(file.read())
		
		profile = _parse_json(resp[0]['body'])
		friends = _parse_json(resp[1]['body'])['data']
		likes = _parse_json(resp[2]['body'])['data']
		
		x = User( 	username = profile.get('username'),
					first_name = profile.get('first_name'),
					last_name = profile.get('last_name'),
					gender = profile.get('gender'),
					uid = profile.get('id'),
					hometown = profile.get('hometown'),
					languages = profile.get('languages'),
					link = profile.get('link'),
					interested_in = profile.get('interested_in'),
					relationship_status = profile.get('relationship_state'),
					religion = profile.get('religion'),
					photo_url = 'http://todo.com',
					friends = json.dumps(friends),
					movies = json.dumps(likes),
					last_fetched = datetime.now(),
				 )
		return x
	fetch = staticmethod(fetch)
	
	def fetch_current(access_token):
		#check cookie for UID, if it exists then fetch for that user, else fetch for another one
		#security concerns, think about it
		return User.fetch("me", access_token)
	fetch_current = staticmethod(fetch_current)
	
	
	def get_current(access_token):
		#caching / use cookies maybe needed here
		u = User.fetch_current(access_token)
		u.save()
		return u
	get_current = staticmethod(get_current)
	
	def get_by_id(id):
		r = User.objects.filter(uid=id)
		cached = True
		if len(r) == 0:
			cached = False
		else:
			r = r[0]
			if r.last_fetched < datetime.now() - timedelta(days=1):
				cached = False
			else:
				return r
		r = fetch(id)
		r.save()
		return r
	get_by_id = staticmethod(get_by_id)
