from django.conf.urls import include, url
from django.contrib import admin
from op_app import views

urlpatterns = [

    url('^', include('django.contrib.auth.urls')),
    url(r'^index/', views.index),
    url(r'^rate/(?P<pk>\d+)/?', views.rate, name="rate"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings', app_name='ratings')),
    url(r'^search/', views.index),
    url(r'^add/', views.addLecturer),
    url(r'^register/', views.registration)
]
