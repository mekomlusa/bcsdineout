from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Category, Restaurant, Hour, YelpReview, BookmarkBase, BookmarkRestaurant, NoteBase, NoteRestaurant
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        
class NoteForm(forms.ModelForm):
    note = forms.CharField(max_length=1000,
                           help_text="Enter your note to the restaurant here. Maximum length 1000.",
                           required=True, widget = forms.Textarea)

    def clean_note(self):
        data = self.cleaned_data['note']
        
        #Check the length of the note.
        if len(data) > 1000:
            raise ValidationError(_('Invalid input - maximum characters allowed: 1000'))

        # Remember to always return the cleaned data.
        return data
    
    class Meta:
        model = NoteRestaurant
        fields = ('note', )