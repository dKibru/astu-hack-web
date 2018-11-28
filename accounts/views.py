from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from .models import Profile, FreeTime
from events.models import Category, Event, Interest, EventTag
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from pathlib import Path

User = get_user_model()

@login_required
def myaccount(request):
	# return request.user.Organizer
	u = request.user
	c = Category.objects.all()
	# filter(user = u).only("category").values()
	ids = Interest.objects.values_list('category_id', flat=True).filter(user = u)
	mc = Category.objects.filter(pk__in=set(ids))
	c = set(c).difference(mc)
	f = FreeTime.objects.filter(user= u)
	context = {'categories' : c,'mycategories': mc,'freetimes': f}
	return render(request, 'accounts/myaccount.html',context)


@login_required
def usertype(request):
	if request.method == 'POST':
		u = request.user
		o = request.POST['type']
		if o=="o":
			Profile(user=u, organizer= True).save()
		else :
			Profile(user = u, attendant=True).save()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def profile(request):
	u = request.user
	if request.method == 'POST':
		e = request.POST['email']
		Interest.objects.filter(user = u).delete()
		for x in request.POST.getlist('interests'):
			cat = Category.objects.get(pk=x)
			if Interest.objects.filter(user = u, category =cat).count()==0:
				Interest(user=u,category=cat).save()

		freetimes = FreeTime.objects.filter(user= u)
		for x in freetimes:
			x1 = request.POST['from'+str(x.id)]
			x2 = request.POST['to'+str(x.id)]
			x3 = request.POST['ampm1'+str(x.id)]
			x4 = request.POST['ampm2'+str(x.id)]
			if x1!='' and x2!='' and x3 !='' and x4!='':
				if request.POST.get('all'+str(x.id)) in request.POST:
					x.allday = True
				else:
					x.start = x1
					x.end = x2
					x.startampm = x3
					x.endampm = x4
					x.allday = False
				x.save()

		num_results = Profile.objects.filter(user = u).count()
		if num_results == 1:
			p = Profile.objects.filter(user = u)[0]
			p.email=e
			p.save()
		else:
			Profile(user=u, email= e).save()

		if 'myimage' in request.FILES:
			my_file = Path('media/profile/'+str(u.id)+".jpg")
			if my_file.is_file():
				os.remove('media/profile/'+str(u.id)+".jpg")
			myfile = request.FILES['myimage']
			fs = FileSystemStorage()
			filename = fs.save('profile/'+str(u.id)+".jpg", myfile)
			uploaded_file_url = fs.url(filename)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
