from django import forms
from .models import *


class AddProjectForm(forms.ModelForm):
    class Meta:
        model = Pins
        fields = ['title', 'description', 'collection', 'video', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'collection': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        user_collections = Collections.objects.filter(author=self.user)
        choices = [(collection.id, collection.title) for collection in user_collections]
        self.fields['collection'].widget.choices = choices


class ChangeProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'about']
        widgets = {
            'about': forms.Textarea(attrs={'rows': 4}),
        }
