from django.forms import ModelForm, fields
from .models import Washing


class WashingForm(ModelForm):
    class Meta:
        model = Washing
        fields = ['date', 'intensity']
