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

FACEBOOK_API_KEY=settings.FACEBOOK_API_KEY    		# change to your facebook api key
FACEBOOK_SECRET_KEY=settings.FACEBOOK_SECRET_KEY 	# change to your facebook app secret key

def index(request):
	return render_to_response('index.html')

def login(request):
	return render_to_response('login.html')

def show(request):
	cookie = facebook.get_user_from_cookie(	request.COOKIES,
											FACEBOOK_API_KEY,
											FACEBOOK_SECRET_KEY)
	profile = None
	friends = []
	likes = []
	print request.COOKIES
	if cookie:
		# Store a local instance of the user data so we don't need
		# a round-trip to Facebook on every request
		x = User.get_by_id(cookie['uid'], cookie["access_token"])
		profile = x
		friends = x.get_friends()
		likes = x.get_likes()
	else :
		friends = "Please log in :)"
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
