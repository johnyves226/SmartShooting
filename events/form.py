from django import forms
from django.forms import TextInput, CheckboxInput

from .models import Event


class EventCreateForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['name','description','is_active','author']
        widgets = {'author': forms.HiddenInput(),
                   'name': TextInput(attrs={
                       'class': "form-control form-control-lg",
                       'style': 'max-width: 300px;',
                       'placeholder': 'Name'
                   }),
                   'description': TextInput(attrs={
                       'class': "form-control form-control-lg",
                       'placeholder': "Description de l'evenement"
                   }),

                   'is_active': CheckboxInput(attrs={
                       'class': "form-check-input me-2",
                   }),


                   }
        labels = {
            'name': 'Event Name',
            'description': 'Event Description',
            'is_active':'active event'
        }


class ImageForm(forms.ModelForm):
    event_id = forms.IntegerField(required=False)
    images =  forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),required=False)
    tags = forms.CharField(max_length=50, required=False)

    class Meta(EventCreateForm.Meta):
        fields = EventCreateForm.Meta.fields + ['images','event_id','tags']