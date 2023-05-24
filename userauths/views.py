from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponseRedirect
# Create your views here.
from .models import Profile
from django.urls import reverse
from django.contrib.auth.models import User
from django.urls import resolve
from post.models import Post,Follow,Stream
from django.core.paginator import Paginator 
from django.db import transaction
from .forms import EditProfileForm

def userProfile(request,username):
    user=get_object_or_404(User,username=username)
    profile=Profile.objects.get(user=user)
    url_name=resolve(request.path).url_name
    if url_name =='profile':
        post=Post.objects.filter(user=user).order_by('-posted')
    else:
        post=profile.favourite.all()
    
    # 
    post_count=Post.objects.filter(user=user).count()
    following_count=Follow.objects.filter(follower=user).count
    followers_count=Follow.objects.filter(following=user).count
    

    paginator=Paginator(post,3)
    page_number=request.GET.get('page')
    posts_paginator=paginator.get_page(page_number)

    #follow status
    follow_status=Follow.objects.filter(following=user,follower=request.user).exists()

    context={
        'posts_paginator':posts_paginator,
        'posts':post,
        'profile':profile,
        'url_name':url_name,
        'post_count':post_count,
        'following_count':following_count,
        'followers_count':followers_count,
        'follow_status':follow_status,
    }
    return render(request,'profile.html',context)

def follow(request,username,option):
    user=request.user
    following=get_object_or_404(User,username=username)
    try:
        f,created=Follow.objects.get_or_create(follower=user,following=following)
        # following is another and follower is me
        if int(option)==0:
            f.delete()
            Stream.objects.filter(following=following,user=user).all().delete()

        else:
            posts=Post.objects.filter(user=following)[:10]

            with transaction.atomic():
                for post in posts:
                    stream=Stream(post=post,user=user,date=post.posted,following=following)
                    stream.save()
        return HttpResponseRedirect(reverse('profile',args=[username]))
        # return HttpResponseRedirect(reverse('profile',args=[username]))
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile',args=[username]))
    
def editProfile(request):
    user=request.user
    profile=Profile.objects.get(user=user)
    form=EditProfileForm()
    if request.method == "POST":
        form=EditProfileForm(request.POST,request.FILES)
        if form.is_valid():
            profile.picture=form.cleaned_data.get('picture')
            # profile.save()
            profile.first_name=form.cleaned_data.get('first_name')
            profile.last_name=form.cleaned_data.get('last_name')
            profile.location=form.cleaned_data.get('location')
            profile.bio=form.cleaned_data.get('bio')
            # profile.url=form.cleaned_data.get('url')
            profile.created=form.cleaned_data.get('created')
            profile.save()
            print("inside the valid")
            return redirect('profile',profile.user.username)
    else:
        form=EditProfileForm(request.POST,request.FILES)
    context={
        'form':form,
    }
    return render(request,'edit_profile.html',context)