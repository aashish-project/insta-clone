from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete


from django.urls import reverse
from django.utils.text import slugify
import uuid

# Create your models here.


# Uploading user file to a specific directory
def user_directory_path(isinstance,filename):
    return 'user_{0}/{1}'.format(isinstance.user.id,filename) 

class Tag(models.Model):
    title=models.CharField(max_length=100,verbose_name="Tag")
    slug=models.SlugField(null=False,unique=True,default=uuid.uuid1)
    class Meta:
        verbose_name="Tag"
        verbose_name_plural="Tags"
    
    def get_absolute_url(self):
        return reverse('tags',args=[self.slug])
    def __str__(self) -> str:
        return self.title
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.slug)#could be error
        return super().save(*args, **kwargs)

class Post(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,unique=True)
    picture=models.ImageField(upload_to=user_directory_path, null=True,verbose_name="Picture")
    caption=models.CharField(max_length=10000,verbose_name="captions")
    posted=models.DateTimeField(auto_now=True, auto_now_add=False)
    tag=models.ManyToManyField(Tag, related_name="Tags")
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    like=models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse("post-detail", args=[str(self.id)] )
    def __str__(self):
        return self.caption
    
class Follow(models.Model):
    follower=models.ForeignKey(User,on_delete=models.CASCADE,related_name="follower")    
    following=models.ForeignKey(User,on_delete=models.CASCADE,related_name="following")    

class Stream(models.Model):
    following=models.ForeignKey(User,on_delete=models.CASCADE,related_name="stream_following")    
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="stream_user")
    post=models.ForeignKey(Post,on_delete=models.CASCADE,null=True)    
    date=models.DateTimeField(auto_now=True, auto_now_add=False)

    def add_post(sender,instance,*args, **kwargs):
        post=instance
        user=post.user
        followers=Follow.objects.all().filter(following=user)
        for follower in followers:
            stream=Stream(post=post,user=follower.follower,following=user)#can be post=post.posted
            stream.save()

    


post_save.connect(Stream.add_post,sender=Post)


class Like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_like")  
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="post_like")  

