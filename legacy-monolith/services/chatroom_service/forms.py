from django import forms
from . models import Room, Message


class RoomForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)

        self.fields['description'].widget.attrs.update({'placeholder':'First 300 Characters Will Display...'})

    class Meta:
        model = Room
        fields = ['name', 'description']



class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']
