from django.urls import path
from . import views, auth

urlpatterns = [
    path('', views.index),
    path('register', auth.register),
    path('login/', auth.login),
    path('logout', auth.logout),
    path('travels', views.travels),
    path('travels/new', views.add_travel),
    path('travels/create', views.create_travel),
    path('travels/<int:trip_id>', views.view_travel),
    path('travels/<int:trip_id>/destroy', views.delete_travel)
]