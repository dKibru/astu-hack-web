from django.contrib import admin
from django.urls import path, include
from . import views

app_name="events"

urlpatterns = [
    path('event', views.event,  name='event'),
    # path('admin/', admin.site.urls),
    # path('register', views.register,name='register'),
    # path('accounts/', include('django.contrib.auth.urls')),
    # # path('accounts/', include('accounts.urls')),
    # path('events/', include('events.urls')),
]