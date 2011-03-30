from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext

def index(request):
    user = ''

    if request.user.is_authenticated():
        user = request.user.facebook_profile


    return render_to_response(
        "index.html",
        {
        'USER_LOGGED_IN': request.user.is_authenticated(),
        'user': user,
        },
        context_instance=RequestContext(request)
    )



def profile(request):
    page = 'profile'
    user = ''

    if request.user.is_authenticated():
        user = request.user.facebook_profile
        friendList = request.user.facebook_profile.get_friends_profiles()
        friendIds = request.user.facebook_profile.get_friends_ids()
    else:
        print "REDIRECTING"
        return HttpResponseRedirect("/")


    return render_to_response(
        "profile.html",
        {
            'page': page,
            'USER_LOGGED_IN': request.user.is_authenticated(),
            'user': user,
            'friendList': friendList,
            'friendIds' : friendIds,
        },
        context_instance=RequestContext(request)
    )


def xd_receiver(request):
    return render_to_response('xd_receiver.html')


