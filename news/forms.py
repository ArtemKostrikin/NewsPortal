from django import forms
from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'author',
            'type',
            'categories',
            'title',
            'text',
        ]


class BaseSignupForm(SignupForm):


    def save(self, request):
        user = super(BaseSignupForm, self).save(request)
        common_group, created = Group.objects.get_or_create(name='common')
        user.groups.add(common_group)
        return user