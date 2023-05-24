from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('edit-profile',views.editProfile,name='edit-profile')
]
