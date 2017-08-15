# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,)

from django.shortcuts import render, redirect

from .forms import UserLoginForm, UserRegisterForm

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
# Create your views here.
def login_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password) #this authentication is redundant because the form has don this
        login(request, user) #this logs in the user
        print(request.user.is_authenticated())
        #since the user has been authenticated, we can redirect him to the right page
        return redirect("/") #redirect to the home page
    return render(request, "accounts/form.html", {"form":form, "title":title})

def logout_view(request):
    logout(request) #this logs out a user
    return redirect("/")

def register_view(request):
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
    	user = form.save(commit=False)
    	password = form.cleaned_data.get('password')
    	user.set_password(password)
    	user.save()

    	new_user = authenticate(username=user.username, password=password)
    	login(request, new_user)

    	#since the user has been registered andauthenticated, we can redirect him to the right page
        return redirect("/")

    context = {
    "form": form,
    "title": title
    }
    return render(request, "accounts/form.html", context)

@login_required(login_url='/login/')
def home_view(request):
	if request.user.is_authenticated():
		print dir(request.user)

	language = 'en-gb' #store the language type for cookie
	session_language = 'en-gb' #store the language type for session
	if 'lang' in request.COOKIES:
		language = request.COOKIES['lang']

	if 'lang' in request.session:
		language = request.session['lang']
	return render(request, "app/index.html", {"language": language, "session_language": session_language})

def language(request, language='en-gb'):
	response = HttpResponse("setting language to %s" % language)
	response.set_cookie('lang', language)

	request.session['lang'] = language
	return response
