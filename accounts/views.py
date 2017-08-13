from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.views import login as django_login

# Create your views here.

def login(request, template_name='accounts/login.html'):
    if request.method == 'GET':
        response = django_login(request, template_name=template_name)
    elif request.method == 'POST':
        response = django_login(request, template_name=template_name)
    return response
