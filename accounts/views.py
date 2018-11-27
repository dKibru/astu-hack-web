from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Profile
from events.models import Category, Event, Interest, EventTag

User = get_user_model()

@login_required
def myaccount(request):
	# return request.user.Organizer
	u = request.user
	c = Category.objects.all()
	# filter(user = u).only("category").values()
	ids = Interest.objects.values_list('category_id', flat=True)
	mc = Category.objects.filter(pk__in=set(ids))
	c = set(c).difference(mc)

	context = {'categories' : c,'mycategories': mc}
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
		num_results = Profile.objects.filter(user = u).count()
		if num_results == 1:
			p = Profile.objects.filter(user = u)[0]
			p.email=e
			p.save()
		else:
			Profile(user=u, email= e).save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))