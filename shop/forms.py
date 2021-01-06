from django import forms

from users.models import Profile


class EditProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'surname', 'phone', 'birthday', 'image']
