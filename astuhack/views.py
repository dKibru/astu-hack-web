from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from events.models import Category, Event, Interest, EventTag
from pathlib import Path
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


# .latest('id')

@login_required
def index(request):
	u = request.user
	ids = []
	for x in Interest.objects.filter(user=u):
		eventags = EventTag.objects.filter(category=x.category)
		for eventag in eventags:
			# event = EventTag.objects.get(pk=x).event
			ids.append(eventag.event.id)
	if Event.objects.filter(featured=True).count()!=0:
		featured = Event.objects.filter(featured=True)[0]
	else:
		featured = None
	c = Category.objects.all()
	e = Event.objects.all()

	allEvents = Event.objects.filter(id__in=ids).order_by('-id')
	paginator = Paginator(allEvents, 3)
	page = request.GET.get('page')
	events = paginator.get_page(page)
	context = {'categories' : c,'events': events}
	return render(request, 'index.html',context)

def register(request):
	if request.user.is_authenticated:
		return redirect('index')
	else:
		if request.method == 'POST':
			form = UserCreationForm(request.POST)
			if form.is_valid():
				form.save()
				user = authenticate(username = form.cleaned_data['username'],password =form.cleaned_data['password1'])
				login(request,user)
				return redirect('index')
		else:
			form = UserCreationForm()
			context = {'form' : form}
			return render(request, 'registration/register.html', context)


def registerLogin(request):
	if request.user.is_authenticated:
		return redirect('index')
	else:
		form = UserCreationForm()
		context = {'form' : form}
		return render(request, 'registration/login_register.html', context)

def secureImage(request,path,id):
	response = HttpResponse()
	ff = "media/"+path+"/"+str(id)+".jpg"
	my_file = Path(ff)
	if my_file.is_file():
		image_data = open(ff, "rb").read()
		return HttpResponse(image_data, content_type="image/jpg")
	else:
		if path=="profile":
			return HttpResponse(open("media/profile/avatar.png", "rb").read(), content_type="image/png")
		return HttpResponse(open("media/profile/3.jpg", "rb").read(), content_type="image/jpg")
    # image_data = open("/home/moneyman/public_html/media/img/main_bg.jpg","rb").read()
    # return render_to_response(‘loans/loan_reports.html’, {image_data:’image_data’}, mimetype=”image/jpeg”)
    # response = HttpResponse(mimetype="image/jpeg")
    # img = Image.open(path+"/"+str(id)+".jpg")
    # img.save(response,'jpg')
    # return response