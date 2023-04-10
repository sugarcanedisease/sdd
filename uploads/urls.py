from django.urls import path

from . import views

urlpatterns  = [
    path('',views.index, name='home'),
    path('about',views.about, name='about'),
    path('service',views.service, name='service'),
    path('prediction',views.prediction, name='prediction'),
    path('contact',views.contact, name='contact'),
    path('after_proccess',views.after_proccess, name='after_proccess'),
    path('uploaded', views.uploaded, name = 'uploaded'),
    path('piechart', views.piechart, name = 'piechart'),
    path('logout_Page', views.logout_Page, name = 'logout_Page'),
    path('register', views.register, name = 'register'),
]