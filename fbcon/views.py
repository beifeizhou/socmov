# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response

import urllib2
import urllib
import json

import facebook
import settings

from fbcon.models import *
from cgi import parse_qs
from django.http import *
from random import shuffle
from math import *

FACEBOOK_API_KEY=settings.FACEBOOK_API_KEY    		# change to your facebook api key
FACEBOOK_SECRET_KEY=settings.FACEBOOK_SECRET_KEY 	# change to your facebook app secret key


def adhoc_ranking_algorithm(mov_list, user):
	movies = []
	res = {}
	for mid in mov_list:
		mov = Movie.getMovieInfo(mid)
		movies.append( mov )
		#calc score
		genre_count = 0
		genres = mov.get_genres()
		if user.relationship_status:
			if user.relationship_status != 'Single':
				genre_count += len( set(["Drama", "Romance"]) & set(genres) )
			if user.relationship_status == 'Married':
				genre_count += len( set(["Family"]) & set(genres) )
		
		if user.gender:
			if user.gender == 'male':
				genre_count += len( set(['Action', 'Action & Adventure', 'Adventure']) & set(genres) ) 
			if user.gender == 'female':
				genre_count += len( set(['Fantasy']) & set(genres) )
		"""
		age = user.get_age()
		if age:
			"""
		
		score = 300* pow(genre_count, 4.0)
		score += 2 * pow(mov.rating_percent()/10., 1.5)
		score += 0.005 * mov.rating_percent() * (1 + mov.votes)
		
		#social factor
		score += 400* pow( len(user.get_friends_who_like(mov)), 3.0 )
		
		res[mid] = score
	print res
	return sorted(res, key=lambda z : -res[z])

	
"""
Converts a list of movie MIDs, into a n*3 2D array
""" 
def transform_to_grid(res, user=None):
	#shuffle(res)
	movies = []
	for i in xrange(0, len(res), 3):
		row = res[i : min([i+3, len(res)]) ]
		tmp = []
		count = 0
		for mid in row:
			mov = Movie.getMovieInfo(mid)
			dic = mov.get_render_compact_dict()
			count += 1
			dic['column'] = count
			dic['friends'] = user.get_friends_who_like( mov ) if user else None
			tmp.append( dic )
		movies.append( tmp )
	return movies

"""Takes the cookies and parses user details from it to return
- profile
- friend list
- movie likes""" 
def get_fb_details(cookies):
	cookie = facebook.get_user_from_cookie(	cookies,
											FACEBOOK_API_KEY,
											FACEBOOK_SECRET_KEY)
	profile = None
	friends = []
	likes = []
	if cookie:
		# Store a local instance of the user data so we don't need
		# a round-trip to Facebook on every request
		x = User.get_by_id(cookie['uid'], cookie["access_token"])
		profile = x
		friends = x.get_friends()
		likes = x.get_likes()
	return profile, friends, likes


def index(request):
	profile, friends, likes = get_fb_details(request.COOKIES)
	
	search_res = Movie.browse(order_by="rating", order="desc", top_x=100, genre=[]) 
	res = []
	for mov in search_res:
		res.append( mov.get("id") )
	res = adhoc_ranking_algorithm(res, profile)
	res = res[0:30]
	movies = transform_to_grid(res, user=profile)
	return render_to_response('index.html', {'movies' : movies, "user" : profile})
	
def profile_user(request):
	profile, friends, likes = get_fb_details(request.COOKIES)
	search_res = profile.get_movie_likes()
	res = []
	for mov in search_res:
		res.append(mov.mid)
	movies = transform_to_grid(res, user=profile)
	return render_to_response('user.html', {'movies' : movies, "user" : profile})
	
def search_movies(request):
	profile, friends, likes = get_fb_details(request.COOKIES)
	params = request.REQUEST
	res = []
	if params.get("query"):
		search_res = Movie.search( params.get("query") )
		res = []
		for mov in search_res:
			res.append( mov.get("id") )
		movies = transform_to_grid(res)
		return render_to_response('search.html', {'movies' : movies, "user" : profile})
	

def login(request):
	return render_to_response('login.html')

def show(request):
	profile, friends, likes = get_fb_details(request.COOKIES)
	if not profile :
		return HttpResponseRedirect("/login/")
	return render_to_response('show.html', {"user" : profile, "friends" : friends, "likes" : likes})

def detail_mov(request):
	params = request.REQUEST
	if params.get("id"):
		mov = Movie.getMovieInfo(long(params.get("id")))
		return render_to_response('movie_detail.html', 
									mov.get_render_dict()
								 )
	return render_to_response('index.html')

#for testing alone
def compact_mov(request):
	params = request.REQUEST
	if params.get("id"):
		mov = Movie.getMovieInfo(long(params.get("id")))
		return render_to_response('movie_compact.html', 
									mov.get_render_compact_dict())
	return render_to_response('index.html')

def vote(request):
	params = request.REQUEST
	cookies = request.COOKIES
	user = get_fb_details(cookies)[0] 
	if user:
		if params.get("movieid"):
			vote = 1 if params.get("type") == "true" else 0
			mov = Movie.getMovieInfo( params.get("movieid") )
			if mov:
				user.add_movie( mov=mov, rating=vote )
		resp_string = "Vote successfully added for movie ", mov.name , " (", mov.mid ,")"
		return HttpResponse(resp_string)
	return HttpResponseForbidden("You're not allowed to make this vote. Probably because you've logged out.")
