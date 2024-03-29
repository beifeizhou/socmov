from django.db import models, connection, transaction
from datetime import *	
import sys
import subprocess
import urllib
import urllib2
import json
import time
import logging

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
config['urls']['movie.browse'] = "http://api.themoviedb.org/2.1/Movie.browse/en/json/%(apikey)s?order_by=%%s&order=%%s&page=1&per_page=%%s&min_votes=%%s" % (config)
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
		try:
			url = config['urls']['genre.getList']
			resp = _parse_json( urllib2.urlopen(url).read() )
			for i in range(1, len(resp)):
				genre_dict[resp[i]['name']] = str(resp[i]['id'])
				gg = Genre(gid = resp[i]['id'], name = resp[i]['name'], url = resp[i]['url'], last_modified_by_us = datetime.now())
				gg.save()
		except Exception, e:
			logging.exception(e)
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
	rating = models.DecimalField(max_digits = 4, decimal_places = 2, null = True)
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
		#current = json.loads(current)
		ret = MovieResult()
		keys = current.keys()
		for i in range(0, len(keys)):
			ret[keys[i]] = current[keys[i]]
		return ret		
	parse = staticmethod(parse)
	
	""" getMovieInfo is used to fetch all info about a movie. It takes the id (MID) of the Movie, 
		which can be obtained using the search method below. MID is an integer"""
	def getMovieInfo(MID):
		#this part fills the Genre Database, if its empty
		cursor = connection.cursor()
		cursor.execute("select * from fbcon_genre")
		if cursor.rowcount <= 0:
			Genre.getGenreList()
			
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
				
				try:
					s = m['released']
					yy1 = int(s[0:4])
					mm1 = int(s[5:7])
					dd1 = int(s[8:])
					d1 = date(yy1, mm1, dd1)
				except Exception:
					d1 = date(1900, 1, 1)
				try:
					s = m['last_modified_at']
					yy2 = int(s[0:4])
					mm2 = int(s[5:7])
					dd2 = int(s[8:10])
					d2 = date(yy2, mm2, dd2)
				except Exception:
					d2 = date(1900, 1, 1)
				
				"""
				TODO youtube trailer crap, currently a very stupid system """
				
				if m['trailer']:
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
								original_name = "", #m['original_name'],
								alternative_name = "", #m['alternative_name'],
								movie_type = m['movie_type'],
								status = m['status'],
								url = m['url'],
								certification = m['certification'],
								homepage = m['homepage'],
								trailer = m['trailer'],
								overview = m['overview'],
								tagline = m['tagline'],
								last_modified_by_tmdb = d2,
								released = d1,
								last_modified_by_us = datetime.now(),
								posters = json.dumps(m['posters']),
								backdrops = json.dumps(m['backdrops']),
								countries = json.dumps(m['countries']),
								studios = json.dumps(m['studios']),
								cast = json.dumps(m['cast']),
								keywords = json.dumps(m['keywords']),
								genres = json.dumps(m['genres']),
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

		except Exception, e:
			logging.exception(e)
			return None
	getMovieInfo = staticmethod(getMovieInfo)
		
	""" search is used to find a list of movies that match your given 'tag'. It is particularly useful to 
		get the id of a particular movie. tag is a string """
	def search(tag):
		search_results = SearchResults()
		tag = tag.replace(" ", "+")
		try:
			url = config['urls']['movie.search'] % (tag)
			resp = _parse_json( urllib2.urlopen(url).read() )
			temp = json.dumps(resp)
			if temp == "[\"Nothing found.\"]":
				#print "returning empty list"
				return SearchResults()
				
			for i in range(0, len(resp)):
				cur_result = Movie.parse(resp[i])
				search_results.append(cur_result)
			return search_results
		except Exception, e:
			logging.exception(e)
			return SearchResults()
	search = staticmethod(search)
	
	def rating_percent(self):
		return int(float(self.rating)*10)
		
	""" browse method is used to fetch top_x number of movies, based on the following parameters:
		order_by: 	["rating", "release", "title"]
		order: 		["asc", "desc"]
		top_x:		an integer (number of movies to be fetched)
		genre:		an array containing all the genres to which the movies should belong to """
	def browse(order_by, order, top_x, min_votes, genre):
		search_results = SearchResults()
		try:
			url = config['urls']['movie.browse'] % (order_by, order, top_x, min_votes)
	
			if len(genre) > 0:
				G = Genre.objects.get(name = genre[0])
				url += "&genres=" + str(G.gid)
				for i in range(1, len(genre)):
					G = Genre.objects.get(name = genre[i])
					url += "," + str(G.gid)
				if len(genre) > 1:
					url += "&genres_selector=and"
			#print url
			resp = _parse_json( urllib2.urlopen(url).read() )
			for i in range(0, len(resp)):
				cur_result = Movie.parse(resp[i])
				search_results.append(cur_result)
			return search_results
		except Exception, e:
			logging.exception(e)
			return SearchResults()
	browse = staticmethod(browse)
	
	def get_genre(self):
		ret = []
		for i in json.loads(self.genres):
			ret.append(i['name'])
		return ret
		
	
	def get_trailer_embed(self):
		if self.trailer:
			return "http://www.youtube.com/embed/" + str(self.trailer)
		return None

	def get_render_dict(self):
		posters = []
		for i  in json.loads(self.posters):
			if i['image']['size'] == 'mid':
				posters.append( i['image'] )
		backdrops = []
		for i in json.loads(self.backdrops):
			if i['image']['size'] == 'original':
				backdrops.append( i['image'] )
		trailer = self.get_trailer_embed()
		return	{"mov" 			: self, 
				 "posters" 		: posters,
				 "backdrops"	: backdrops, 
				 "trailer" 		: trailer,
				}
	def get_render_compact_dict(self):
		poster = None
		for i in json.loads(self.posters):
			if i['image']['size'] == 'thumb':
				poster = i['image']
				break
		return {"mov"		: self,
				"poster"	: poster}
	
	def get_genres(self):
		ret = []
		for i in json.loads(self.genres):
			ret.append(i['name'])
		return ret

class User(models.Model):
	username = models.CharField(max_length=128, null=True)
	first_name = models.CharField(max_length=128, null=True)
	last_name = models.CharField(max_length=128, null=True)
	gender = models.CharField(max_length=16, null=True)
	uid = models.CharField(max_length=128, primary_key=True)
	hometown = models.CharField(max_length=2048, null=True)
	hometown = models.CharField(max_length=2048, null=True)
	
	languages = models.CharField(max_length=2048, null=True)
	link = models.CharField(max_length=128)
	interested_in = models.CharField(max_length=1024, null=True)
	relationship_status = models.CharField(max_length=1024, null=True)
	religion = models.CharField(max_length=1024, null=True)
	photo_url = models.CharField(max_length=1024)
	
	birthday = models.DateField(null=True)
	education = models.TextField(null=True)
	political = models.TextField(null=True)
	work = models.TextField(null=True)
	
	#json encoded strings
	friends = models.TextField()
	movies = models.TextField()
	
	last_fetched = models.DateTimeField()
	last_updated_movies = models.DateTimeField()
	movie = models.ManyToManyField(Movie, through = "Vote")
	
	"""Returns a boolean signifying if an actual fetch/update takes place""" 
	def update_movies(self):
		if self.last_updated_movies < datetime.now() - timedelta(days = 30):
			self.last_updated_movies = datetime.now() #update timestamp
			self.save()
			m = json.loads(self.movies)
			for i in m:
				try:
					M = Movie.search(i["name"])
					if len(M) < 1:
						continue
					self.add_movie( Movie.getMovieInfo(M[0]['id']), 1 )
				except Exception, e:
					logging.exception(e)
			return True
		return False

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
		
		birthday = None
		if profile.get('birthday'):
			mm, dd, yy = profile.get('birthday').split('/')
			mm, dd, yy = int(mm), int(dd), int(yy)
			birthday = date(yy, mm, dd)
		x = User( 	username = profile.get('username'),
					first_name = profile.get('first_name'),
					last_name = profile.get('last_name'),
					gender = profile.get('gender'),
					uid = profile.get('id'),
					hometown = profile.get('hometown'),
					languages = json.dumps(profile.get('languages')),
					link = profile.get('link'),
					interested_in = json.dumps(profile.get('interested_in')),
					relationship_status = profile.get('relationship_status'),
					religion = profile.get('religion'),
					photo_url = 'http://todo.com',
					birthday = birthday,
					education = json.dumps(profile.get('education')),
					political = json.dumps(profile.get('political')),
					work = json.dumps(profile.get('work')),
					friends = json.dumps(friends),
					movies = json.dumps(likes),
					last_fetched = datetime.now(),
					last_updated_movies = datetime.now() - timedelta(days = 1000)
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
				return r
		r = User.fetch(id, access_token)
		r.save()
		
		return r
	get_by_id = staticmethod(get_by_id)

	def get_friends(self):
		return json.loads(self.friends)
	
	def get_likes(self):
		return json.loads(self.movies)
		
	""" add_movie function is called when a user likes/dislikes a movie. It relates a movie with a user 
		r = 0 means dislike
		r = 1 means like """
	def add_movie(self, mov, rating):
		try:
			if mov == None:
				return
			cursor = connection.cursor()
			cursor.execute('DELETE FROM fbcon_vote WHERE movie_id = %s and user_id = %s', [mov.mid, self.uid])
			transaction.commit_unless_managed()
			#Vote.objects.filter(movie__mid = mov.mid, user__uid = self.uid).delete()
			#if len(a) > 0:
				#a.delete()
			v = Vote(movie = mov, user = self, last_updated = datetime.now(), rating = rating)
			v.save()
		
		except Exception, e:
			logging.exception(e)
			
	""" get_friends_like function is used to find all the friends which like the given Movie mov """	
	def get_friends_who_like(self, mov):
		#print "inside, for movie : ", mov.name, mov.mid
		try:
			fr = self.get_friends()
			ids = []
			for f in fr:
				z = User.objects.filter(uid=f['id'])
				if len(z) > 0:
					ids.append(z[0])
			
			"""ans = []
			query = "SELECT uid from fbcon_user, fbcon_vote, fbcon_movie WHERE fbcon_vote.movie_id = fbcon_movie.mid and fbcon_user.uid = fbcon_vote.user_id and fbcon_movie.mid = %s and fbcon_vote.rating = 1 and uid in (%s"
			for i in range(2, len(ids)):
				query = query + ", %s"
			query = query + ")"
			ret = User.objects.raw(query, ids)
			#print ret
			for i in ret:
				ans.append(i)
			print "return : ", len(ans)"""
			ans = User.objects.filter(vote__user__in = ids, vote__movie__mid = mov.mid, vote__rating = 1)
			#print "Return : ", len(ans)
			return ans
		except Exception, e:
			logging.exception(e)
			return []
			
	def get_movies_liked_by_friends(self):
		try:
			fr = self.get_friends()
			ids = []
			for f in fr:
				#ids.append(f['id'])
				z = User.objects.filter(uid = f['id'])
				if len(z) > 0:
					ids.append(z[0])
			ans = Movie.objects.filter(vote__user__in = ids, vote__rating = 1)
			
			""" ans = []
			query = "SELECT * FROM fbcon_movie WHERE mid in (SELECT DISTINCT x.mid FROM fbcon_movie as x, fbcon_user as y, fbcon_vote as z WHERE z.movie_id = x.mid and y.uid = z.user_id and z.rating = 1 and y.uid in (%s"
			for i in range(1, len(ids)):
				query = query + ", %s"
			query = query + ")) and mid not in (SELECT mid from fbcon_movie, fbcon_user, fbcon_vote where fbcon_vote.user_id = %s and fbcon_vote.movie_id = fbcon_movie.mid and fbcon_user.uid = fbcon_vote.user_id and fbcon_vote.rating = 1)"
			ids.append(self.uid)
			ret = Movie.objects.raw(query, ids)
			for i in ret:
				ans.append(i) """
			return list(set(ans))
		except Exception, e:
			logging.exception(e)
			return []
		
	def get_movie_likes(self):
		try:
			"""ret = Movie.objects.raw('SELECT * FROM fbcon_movie WHERE mid in (SELECT mid from fbcon_movie, fbcon_user, fbcon_vote where fbcon_vote.user_id = %s and fbcon_vote.movie_id = fbcon_movie.mid and fbcon_user.uid = fbcon_vote.user_id and fbcon_vote.rating = 1)', [self.uid])
			ans = []
			for i in ret:
				ans.append(i)"""
			ans = Movie.objects.filter(vote__user__uid = self.uid, vote__rating = 1)
			return ans
		except Exception, e:
			logging.exception(e)
			return []
		
	def get_age(self):
		if self.birthday == None:
			return None
		return (date.today() - self.birthday).days / 365.0
		
	def convert_to_libsvm(self):
		gender = self.gender if self.gender else ""
		relationship_status = self.relationship_status if self.relationship_status else ""
		interested_in = ""
		languages_spoken = ""
		education = ""
		work = "0"
		age = ""
		hi = 0
		col = 0
		grad = 0
		
		
		try:
			for i in json.loads(self.interested_in):
				interested_in = interested_in + i + " "
		except Exception, e:
			pass
		
		try:
			for i in json.loads(self.languages):
				languages_spoken = languages_spoken + i['name'] + " "
		except Exception, e:
			pass
			
		try:
			for i in json.loads(self.education):
				x = i['type']
				if x == 'High School':
					hi = 1
				if x == 'College':
					col = 1
				if x == 'Graduate School':
					grad = 1
		except Exception, e:
			pass
				
		education = str(grad) + " " + str(col) + " " + str(hi)
		try:
			work = str(len(json.loads(self.work)))
		except Exception, e:
			pass
		if self.get_age():
			age = str(self.get_age())
	
		"""print "Gender : ", gender
		print "Rel Stat : ", relationship_status
		print "int in : ", interested_in
		print "languages : ", languages_spoken
		print "education : ", education
		print "work : ", work
		print "Age : ", age"""
		
		process = subprocess.Popen('/home/purav/Desktop/socmov/svm/svm', shell=False, stdin = subprocess.PIPE, stdout = subprocess.PIPE)
		input = gender + "\n" + relationship_status + "\n" + interested_in + "\n" + languages_spoken + "\n" + education + "\n" + work + "\n" + age
		output = process.communicate(input)
		#print output[0]
		return output[0]

class Vote(models.Model):
	movie = models.ForeignKey(Movie)
	user = models.ForeignKey(User)
	last_updated = models.DateTimeField()
	rating = models.IntegerField()


class MovieBrowser(models.Model):
	id = models.CharField(max_length=128, primary_key=True)
	text = models.TextField(null=True)
	last_fetched = models.DateTimeField()
	
	def decode(self):
		return json.loads(self.text)
	
	
	def browse(order_by="rating", order="desc", top_x=12, min_votes = 70, genre=[]):
		idx = order_by , "#", order , "#", top_x , "#", min_votes , "#", genre
		idx = str(idx)
		#print "browsing invoked with params", idx
		res = MovieBrowser.objects.filter(id=idx)
		cached = True
		if len(res) == 0:
			cached = False
		else:
			res = res[0]
			if res.last_fetched < datetime.now() - timedelta(hours=6):
				cached = False
			else:
				#print "returning cached values"
				return res.decode()
		#print "uncached searching again"
		search_res = Movie.browse(order_by=order_by, order=order, top_x=top_x, min_votes = min_votes, genre=genre) 
		ids = []
		for mov in search_res:
			ids.append( mov.get("id") )
		res = MovieBrowser( id = idx, 
							text = json.dumps(ids),
							last_fetched = datetime.now() )
		res.save()
		return ids
	browse = staticmethod(browse) 
