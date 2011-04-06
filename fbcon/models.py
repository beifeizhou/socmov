from django.db import models
from datetime import *	
import urllib
import urllib2
import json
import time

from urlparse import urlparse
from cgi import parse_qs

_parse_json = lambda s: json.loads(s)
config = {}
config['apikey'] = "19e1fde682cf97ab5321ae7ec25c6765" #"a8b9f96dde091408a03cb4c78477bd14" #"YOUR_API_KEY" # Thanks BeeKeeper
config['urls'] = {}
config['urls']['movie.search'] = "http://api.themoviedb.org/2.1/Movie.search/en/json/%(apikey)s/%%s" % (config)
config['urls']['movie.getInfo'] = "http://api.themoviedb.org/2.1/Movie.getInfo/en/json/%(apikey)s/%%s" % (config)
config['urls']['media.getInfo'] = "http://api.themoviedb.org/2.1/Media.getInfo/en/json/%(apikey)s/%%s/%%s" % (config)
config['urls']['imdb.lookUp'] = "http://api.themoviedb.org/2.1/Movie.imdbLookup/en/json/%(apikey)s/%%s" % (config)
config['urls']['movie.browse'] = "http://api.themoviedb.org/2.1/Movie.browse/en/json/%(apikey)s?order_by=%%s&order=%%s&page=1&per_page=%%s&min_votes=10" % (config)
config['urls']['genre.getList'] = "http://api.themoviedb.org/2.1/Genres.getList/en/json/%(apikey)s" % (config)
offest = 2629743 * 3 #1 month = 2629743 seconds
genre_dict = {}

class Genre(models.Model):
	"""Database to store all the genres supported by TMDB"""
	gid = models.IntegerField(primary_key = True)
	name = models.CharField(max_length = 20)
	url = models.CharField(max_length = 100)
	last_modified_by_us = models.DateField(null = True)
	
	""" getGenreList is used to fetch all the genres from the TMDB API. This function is to be called only once """
	def getGenreList():
		url = config['urls']['genre.getList']
		resp = _parse_json( urllib2.urlopen(url).read() )
		for i in range(1, len(resp)):
			genre_dict[resp[i]['name']] = str(resp[i]['id'])
			gg = Genre(gid = resp[i]['id'], name = resp[i]['name'], url = resp[i]['url'], last_modified_by_us = datetime.now())
			gg.save()
	getGenreList = staticmethod(getGenreList)	
			
class SearchResults(list):
    """Stores a list of Movie's that matched the search"""
    def __repr__(self):
        return "<Search results: %s>" % (list.__repr__(self))			
							
class MovieResult(dict):
    """A dict containing the information about the film"""
    def __repr__(self):
        return "<MovieResult: %s (%s)>" % (self.get("name"), self.get("released"))

class Movie(models.Model):
	mid = models.IntegerField(primary_key = True)
	popularity = models.IntegerField(null = True)
	votes = models.IntegerField(null = True)
	runtime = models.IntegerField(null = True)
	version = models.IntegerField(null = True)
	revenue = models.BigIntegerField(null = True)
	budget = models.BigIntegerField(null = True)
	rating = models.DecimalField(max_digits = 2, decimal_places = 1, null = True)
	translated = models.BooleanField()
	adult = models.BooleanField()
	imdb_id = models.CharField(max_length = 15, null = True)
	status = models.CharField(max_length = 15, null = True)
	language = models.CharField(max_length = 10, null = True)
	original_name = models.CharField(max_length = 100, null = True)
	name = models.CharField(max_length = 100)
	alternative_name = models.CharField(max_length = 100, null = True)
	movie_type = models.CharField(max_length = 20, null = True)
	url = models.CharField(max_length = 100, null = True)
	certification = models.CharField(max_length = 10, null = True)
	homepage = models.CharField(max_length = 100, null = True)
	trailer = models.CharField(max_length = 100, null = True)
	overview = models.TextField(null = True)
	tagline = models.TextField(null = True)
	last_modified_by_tmdb = models.DateField(null = True)
	released = models.DateTimeField(null = True)
	last_modified_by_us = models.DateTimeField()
	genre = models.ManyToManyField("Genre")
	
	#json encoded fields
	posters = models.TextField(null = True)
	backdrops = models.TextField(null = True)
	languages_spoken = models.TextField(null = True)
	keywords = models.TextField(null = True)
	studios = models.TextField(null = True)
	cast = models.TextField(null = True)
	countries = models.TextField(null = True)
	genres = models.TextField(null = True)
		
	def parse(current):
		ret = MovieResult()
		keys = current.keys()
		for i in range(0, len(keys)):
			ret[keys[i]] = current[keys[i]]
		return ret		
	parse = staticmethod(parse)
	
	""" getMovieInfo is used to fetch all info about a movie. It takes the id (MID) of the Movie, 
		which can be obtained using the search method below. MID is an integer"""
	def getMovieInfo(MID):
		try:
			res = Movie.objects.filter(mid=MID)
			cached = True
			if len(res) == 0:
				cached = False
			elif res[0].last_modified_by_us < datetime.now() - timedelta(days = 30):
				cached = False
			
			if cached == False:
				url = config['urls']['movie.getInfo'] % (MID)
				resp = _parse_json( urllib2.urlopen(url).read() )[0]
				m = Movie.parse(resp)
				
				s = m['released']
				yy1 = int(s[0:4])
				mm1 = int(s[5:7])
				dd1 = int(s[8:])
				s = m['last_modified_at']
				yy2 = int(s[0:4])
				mm2 = int(s[5:7])
				dd2 = int(s[8:10])
				"""
				TODO youtube trailer crap, currently a very stupid system """
				m['trailer'] = parse_qs(urlparse(m['trailer']).query)
				if m['trailer'].get('v'):
					m['trailer'] = m['trailer']['v'][0]
				else:
					m['trailer'] = None 			
				
				movie = Movie(	mid = m['id'], 
								imdb_id = m['imdb_id'], 
								popularity = m['popularity'], 
								votes = m['votes'], 
								runtime = m['runtime'], 
								version = m['version'], 
								revenue = m['revenue'],
								budget = m['budget'],
								rating = str(m['rating']),
								translated = m['translated'],
								adult = m['adult'],
								language = m['language'],
								name = m['name'],
								original_name = m['original_name'],
								alternative_name = m['alternative_name'],
								movie_type = m['movie_type'],
								status = m['status'],
								url = m['url'],
								certification = m['certification'],
								homepage = m['homepage'],
								trailer = m['trailer'],
								overview = m['overview'],
								tagline = m['tagline'],
								last_modified_by_tmdb = date(yy2, mm2, dd2),
								released = date(yy1, mm1, dd1),
								last_modified_by_us = datetime.now(),
								posters = json.dumps(m['posters']),
								backdrops = json.dumps(m['backdrops']),
								countries = json.dumps(m['countries']),
								studios = json.dumps(m['studios']),
								cast = json.dumps(m['cast']),
								keywords = json.dumps(m['keywords']),
								genres = json.dumps(m['genres'])
							)
				
				movie.save()
				#many to many field relationship between Movie and Genre
				obj = m['genres']
				for i in range(0, len(obj)):
					G = Genre.objects.get(gid = obj[i]['id'])
					movie.genre.add(G)
				return movie
			else:
				return res[0]
		except Exception as detail:
			print detail
			return None
	getMovieInfo = staticmethod(getMovieInfo)
		
	""" search is used to find a list of movies that match your given 'tag'. It is particularly useful to 
		get the id of a particular movie. tag is a string"""
	def search(tag):
		search_results = SearchResults()
		try:
			url = config['urls']['movie.search'] % (tag)
			resp = _parse_json( urllib2.urlopen(url).read() )
			for i in range(0, len(resp)):
				cur_result = Movie.parse(resp[i])
				search_results.append(cur_result)
			return search_results
		except Exception:
			return SearchResults()
	search = staticmethod(search)
	
	""" browse method is used to fetch top_x number of movies, based on the following parameters:
		order_by: 	["rating", "release", "title"]
		order: 		["asc", "desc"]
		top_x:		an integer (number of movies to be fetched)
		genre:		an array containing all the genres to which the movies should belong to """
	def browse(order_by, order, top_x, genre):
		search_results = SearchResults()
		try:
			url = config['urls']['movie.browse'] % (order_by, order, top_x)
	
			if len(genre) > 0:
				G = Genre.objects.get(name = genre[0])
				url += "&genres=" + str(G.gid)
				for i in range(1, len(genre)):
					G = Genre.objects.get(name = genre[i])
					url += "," + str(G.gid)
				url += "&genres_selector=and"
			
			resp = _parse_json( urllib2.urlopen(url).read() )
			for i in range(0, len(resp)):
				cur_result = Movie.parse(resp[i])
				search_results.append(cur_result)
			return search_results
		except Exception:
			return SearchResults()
	browse = staticmethod(browse)
	
	def get_trailer_embed(self):
		return "http://www.youtube.com/embed/" + str(self.trailer)
	
		
		
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
	
	def get_by_id(id, access_token):
		r = User.objects.filter(uid=id)
		cached = True
		if len(r) == 0:
			cached = False
		else:
			r = r[0]
			if r.last_fetched < datetime.now() - timedelta(days=1):
				cached = False
			else:
				print "returning cached user"
				return r
		r = fetch(id, access_token)
		r.save()
		return r
	get_by_id = staticmethod(get_by_id)

