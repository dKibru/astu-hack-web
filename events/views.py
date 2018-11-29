from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from accounts.models import Profile, FreeTime
from .models import Category, Event, Interest, EventTag
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.core.files.storage import FileSystemStorage
# from dateutil import parser
from dateutil.parser import *
User = get_user_model()

@login_required
def event(request):
	u = request.user
	if request.method == 'POST':
		t = request.POST['title']
		d = request.POST['detail']
		dt = request.POST['datetime']
		e = Event(created_by = u, title = t, detail = d, event_datetime= parse(dt))
		e.save()
		for x in request.POST.getlist('categories'):
			cat = Category.objects.get(pk=x)
			EventTag(event = e, category=cat).save()
		if request.FILES['myimage']:
			myfile = request.FILES['myimage']
			fs = FileSystemStorage()
			filename = fs.save('event/'+str(e.id)+".jpg", myfile)
			uploaded_file_url = fs.url(filename)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def api_event(request):
	e = Event.objects.all()
	data = serializers.serialize('json', e)
	return HttpResponse(data, content_type="application/json")
	# return JsonResponse({'foo':e})


def game(request):
	return render(request, 'game.html')


def category(request, category_id):
	thisc = Category.objects.filter(id=category_id)[0]
	if Event.objects.filter(featured=True).count()!=0:
		featured = Event.objects.filter(featured=True)[0]
	else:
		featured = None
	c = Category.objects.all()
	# e = Event.objects.filter(category = thisc)
	ids = EventTag.objects.filter(category = thisc).values_list('event', flat=True)
	my_models = Event.objects.filter(pk__in=set(ids))
	context = {'categories' : c,'events': my_models}
	return render(request, 'index.html',context)