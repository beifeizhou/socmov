from django.db import models
from themoviedb import tmdb

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
	genre = models.ManyToManyField("Genre")
	
	#json encoded fields
	languages_spoken = models.TextField()
	categories = models.TextField()
	keywords = models.TextField()
	studios = models.TextField()
	countries = models.TextField()
		
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
	username = models.CharField(max_length=128)
	first_name = models.CharField(max_length=128)
	last_name = models.CharField(max_length=128)
	gender = models.CharField(max_length=16)
	uid = models.IntegerField()
	hometown = models.CharField(max_length=2048)
	languages = models.CharField(max_length=2048)
	link = models.CharField(max_length=128)
	interested_in = models.CharField(max_length=1024)
	relationship_status = models.CharField(max_length=1024)
	religion = models.CharField(max_length=1024)
	photo_url = models.CharField(max_length=1024)
	
	#json encoded strings
	friends = models.TextField()
	movies = models.TextField()
	
	

