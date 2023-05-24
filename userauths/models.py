from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from post.models import Post 


# Uploading user file to a specific directory
def user_directory_path(isinstance,filename):
    return 'user_{0}/{1}'.format(isinstance.user.id,filename) 

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100,null=True,blank=True)
    last_name=models.CharField(max_length=100,null=True,blank=True)
    location=models.CharField(max_length=100,null=True,blank=True)
    url=models.URLField(max_length=100,null=True,blank=True)
    bio=models.TextField(max_length=1000,null=True,blank=True)
    created=models.DateField( auto_now=True, auto_now_add=False)
    picture=models.ImageField(upload_to=user_directory_path, blank=True,null=True,verbose_name='profile-pic' )
    favourite=models.ManyToManyField(Post,blank=True)

    def __str__(self):
        return self.user.username