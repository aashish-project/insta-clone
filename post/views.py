from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.
from post.models import Tag,Stream,Follow,Post,Like
from django.contrib.auth.decorators import login_required
from post.forms import NewPostForm
from userauths.models import Profile
from comment.models import Comment
from comment.forms import CommentForm

def index(request):
    user=request.user
    posts=Stream.objects.filter(user=user)
    group_ids=[]
    for post in posts:
        group_ids.append(post.post.id)


    post_items=Post.objects.filter(id__in=group_ids).all().order_by('-posted')
    context={
        'post_items':post_items,
    }
    return render(request,'index.html',context)

def NewPost(request):
    user=request.user
    tags_objs=[]
    if request.method=="POST":
        form=NewPostForm(request.POST,request.FILES)
        if form.is_valid():
            picture=form.cleaned_data.get('picture')
            caption=form.cleaned_data.get('caption')
            tag_form=form.cleaned_data.get('tag')
            tags_list=list(tag_form.split(',')) #one piece , roronoa zor -> [one piece , roronoa zoro]
            for tag in tags_list:
                t,created=Tag.objects.get_or_create(title=tag)
                tags_objs.append(t)
            p,created=Post.objects.get_or_create(picture=picture,caption=caption,user_id=user.id)
            p.tag.set(tags_objs)
            p.save()
            return redirect('index')
    else:
        form=NewPostForm()
    context={
        'form':form,
    }
    return render(request,'newpost.html',context)


def PostDetail(request,post_id):
    post=get_object_or_404(Post,id=post_id)

    comments=Comment.objects.filter(post=post).order_by("-date")
    if request.method == "POST":
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=post
            comment.user=request.user
            comment.save()
            return HttpResponseRedirect(reverse('post-detail',args=[post_id]))
    else:
        form=CommentForm()
    context={
        'post':post,
        'comments':comments,
        'form':form,
    }
    return render(request,'post-details.html',context)
    pass
def LikeFunction(request,post_id):
    user=request.user
    post=Post.objects.get(id=post_id)
    current_like=post.like
    liked=Like.objects.filter(user=user,post=post).count()
    if not liked:
        liked=Like.objects.create(user=user,post=post)
        current_like=current_like+1

    else:
        liked=Like.objects.filter(user=user,post=post).delete()
        current_like=current_like-1

    post.like=current_like
    post.save()
    return HttpResponseRedirect(reverse('post-detail',args=[post_id]))
    pass

def favouritePost(request,post_id):
    user=request.user
    post=Post.objects.get(id=post_id)
    profile=Profile.objects.get(user=request.user)
    if profile.favourite.filter(id=post_id).exists():
        profile.favourite.remove(post)
    else:
        profile.favourite.add(post)
    profile.save()

    return HttpResponseRedirect(reverse('post-detail',args=[post_id]))