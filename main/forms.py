from django import forms
from django.forms import ModelForm
from .models import TextComment, Location
from .widgets import GoogleMapPointWidget



class TextCommentForm(forms.ModelForm):
    class Meta:
        model = TextComment
        fields = ('message',)


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'
        widgets = {
            'lnglat': GoogleMapPointWidget,
        }
