from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from accounts.models import Profile
from .models import Category, Event, Interest, EventTag

User = get_user_model()

@login_required
def event(request):
	u = request.user
	if request.method == 'POST':
		t = request.POST['title']
		d = request.POST['detail']
		e = Event(created_by = u, title = t, detail = d).save()
		for x in request.POST.getlist('categories'):
			cat = Category.objects.get(pk=x)
			EventTag(event = e, category=cat).save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))