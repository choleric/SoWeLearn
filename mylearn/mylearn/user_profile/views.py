from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext

from models import *

# Create your views here.

#user_db = models.User()

def test(request):
    return HttpResponse("hello world")

def welcome(request):
    return render_to_response('welcome.html')

def register_(request):
    if request.method == 'GET':
        return render_to_response('register.html', context_instance=RequestContext(request))
    else:
        print request.POST
        user_email = request.POST.get('user_email')
        error = []
        print 'got:', user_email
        if not user_db.get_user(user_email):
            context = {'user_info': request.POST}
            print request.user
            user_info = request.POST
            user_db.add_user(user_name=user_info.get('user_name'), user_email=user_info.get('user_email'),
                    user_location=user_info.get('user_location'))
            return render_to_response('welcome.html', context)
        else:
            error.append('%s already exists, please login' % user_email)
            context = {'errors': error}
            context.update(csrf(request))
            return render_to_response('welcome.html', context)
            #return HttpResponseRedirect('login.html')


def login1(request):
    if request.method == 'GET':
        return render_to_response('login.html', context_instance=RequestContext(request))
    else:
        user_email= request.POST.get('user_email')
        print 'email:', user_email
        user = user_db.get_user(user_email)
        if not user:
            context = { 'errors': '%s is not exist' % user_email}
        else:
            context = {'user_info': user}
        #return HttpResponseRedirect('welcome.html', context)
        return render_to_response('welcome.html', context)


def login_old(request):
    if request.method == 'GET':
        return render_to_response('login.html', context_instance=RequestContext(request))
    else:
        user_email= request.POST.get('user_email')
        print 'email:', user_email
        user = user_db.get_user(user_email)
        if not user:
            context = { 'errors': '%s is not exist' % user_email}
        else:
            #context = {'user_info': user}
            context = {'userPersonalProfile': user.get('userPersonalProfile', {})}
        #return HttpResponseRedirect('welcome.html', context)
        return render_to_response('userProfile.html',  context)

def login(request):
    if request.method == 'GET':
        return render_to_response('login.html', context_instance=RequestContext(request))
    else:
        user_email= request.POST.get('user_email')
        print 'email:', user_email
        user=User.objects(user_email=user_email).first()
        print user
        if not user:
            context = { 'errors': '%s is not exist' % user_email}
        else:
            #context = {'user_info': user}
            context = {'userPersonalProfile': user.userPersonalProfile}
        #return HttpResponseRedirect('welcome.html', context)
        return render_to_response('userProfile.html',  context)


