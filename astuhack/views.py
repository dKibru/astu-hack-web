from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from events.models import Category, Event, Interest, EventTag

@login_required
def index(request):
	c = Category.objects.all()
	e = Event.objects.all()
	context = {'categories' : c,'events': e}
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
