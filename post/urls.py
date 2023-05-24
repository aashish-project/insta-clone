from django.contrib import admin
from django.urls import path
from post import views
from django.urls import reverse
# import uuid
from userauths.models import Profile 
from userauths.views import userProfile,follow 

urlpatterns = [
    path('',views.index,name='index'),
    path('newpost/',views.NewPost,name='newpost'),
    path('post-details/<uuid:post_id>',views.PostDetail, name="post-detail"),
    path('post/<uuid:post_id>/like',views.LikeFunction, name="like"),
    path('post/<uuid:post_id>/save',views.favouritePost, name="save"),

    # profile section
    path('<username>/',userProfile,name="profile"),
    path('<username>/favourite/',userProfile,name="favourite"),
    path('<username>/follow/<option>',follow,name="follow"),
]
