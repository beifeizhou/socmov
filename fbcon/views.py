# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response


import facebook

FACEBOOK_API_KEY='188365901207571'    		# change to your facebook api key
FACEBOOK_SECRET_KEY='f09191489ff3faff4d3c056838f6339b' 	# change to your facebook app secret key

def index(request):
	
	
	return render_to_response('login.html')
	

def show(request):
	
	cookie = facebook.get_user_from_cookie(	request.COOKIES,
											FACEBOOK_API_KEY,
											FACEBOOK_SECRET_KEY)
	#print request.COOKIES
	if cookie:
		# Store a local instance of the user data so we don't need
		# a round-trip to Facebook on every request
		#print cookie, " kemcho"
		graph = facebook.GraphAPI(cookie["access_token"])
		profile = graph.get_object("me")
		print profile
		#check on the development console
	
	return render_to_response('show.html')

