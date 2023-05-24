from django import forms
from post.models import Post
class NewPostForm(forms.ModelForm):
    picture=forms.ImageField(required=True)
    caption=forms.CharField( widget=forms.TimeInput(attrs= {'class':'input' , 'placeholder':'Caption'}), required=True)
    tag=forms.CharField( widget=forms.TimeInput(attrs={'class':'input','placeholder':'Tags - Seperate tag with comma'}), required=True)

    class Meta:
        model=Post
        fields=['picture','caption','tag']

