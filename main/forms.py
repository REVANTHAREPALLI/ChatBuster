from django.forms import ModelForm
from .models import Room

class FormRoom(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'