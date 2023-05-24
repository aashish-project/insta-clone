from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.db.models import Max

class Message(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name='user')
    sender=models.ForeignKey(User, on_delete=models.CASCADE,related_name="from_user")
    reciever=models.ForeignKey(User, on_delete=models.CASCADE,related_name="reciever")
    body=models.TextField()
    date=models.DateTimeField(auto_now=False, auto_now_add=True)
    is_read=models.BooleanField()

    def send_message(from_user,to_user,body):
        sender_message=Message(
            user=from_user,
            sender=from_user,
            reciever=to_user,
            body=body,
            is_read=True,
        )
        sender_message.save()
        
        reciever_message=Message(
            user=to_user,
            sender=to_user,
            reciever=from_user,
            body=body,
            is_read=False,
        )
        reciever_message.save()
        return reciever_message
    
    def get_message(user):
        users=[]
        messages=Message.objects.filter(user=user).values('reciever').annotate(last=Max('date')).order_by("-last")
        for message in messages:
            users.append({
                'user':User.objects.get(pk=message['reciever']),
                'last':message['last'],
                'unread':Message.objects.filter(user=user,reciever__pk=message['reciever'],is_read=False).count(),

            })
        return users
