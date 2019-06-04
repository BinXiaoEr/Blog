from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^login$', login, name='login'),
    url(r'^register$', register, name='register'),
    url(r'^$', home, name='home'),
]
