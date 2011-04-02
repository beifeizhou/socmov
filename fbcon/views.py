# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response

import urllib2
import urllib
import json

import facebook
import settings

from fbcon.models import *

FACEBOOK_API_KEY=settings.FACEBOOK_API_KEY    		# change to your facebook api key
FACEBOOK_SECRET_KEY=settings.FACEBOOK_SECRET_KEY 	# change to your facebook app secret key

def index(request):
	return render_to_response('login.html')
	

def show(request):
	cookie = facebook.get_user_from_cookie(	request.COOKIES,
											FACEBOOK_API_KEY,
											FACEBOOK_SECRET_KEY)
	profile = {}
	friends = []
	likes = []
	print request.COOKIES
	if cookie:
		# Store a local instance of the user data so we don't need
		# a round-trip to Facebook on every request
		x = User.get_current(cookie["access_token"])
		#graph = facebook.GraphAPI(cookie["access_token"])
		#make a batch request
		#profile = graph.get_object("me")
		#friends = graph.get_connections("me", "friends")
		#likes = graph.get_object("me/movies")
		"""
		batchstr  = [{"method":"get","relative_url":"me","access_token":cookie["access_token"]},
					 {"method":"get","relative_url":"me/friends","access_token":cookie["access_token"]},
					 {"method":"get","relative_url":"me/movies","access_token":cookie["access_token"]}]
		args = { "batch" : batchstr,
				 "method" : "POST", 
				 "access_token" : cookie["access_token"], 
				}
		
		file = urllib2.urlopen("https://graph.facebook.com/", urllib.urlencode(args))
		resp = _parse_json(file.read())
		
		profile = _parse_json(resp[0]['body'])
		friends = _parse_json(resp[1]['body'])['data']
		likes = _parse_json(resp[2]['body'])['data']
		
		print type(profile), type(friends), type(likes)
		#check on the development console
		"""
	else :
		friends = "Please log in :)"
	return render_to_response('show.html', {"user": profile, "friends"  : friends, "likes" : likes} )
