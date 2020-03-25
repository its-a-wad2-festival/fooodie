from django import forms
from fooodie.models import UserProfile, Photo
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)

class UserSearchBarForm(forms.Form):
    username=forms.CharField()

class ChangeUsername(forms.Form):
    username=forms.CharField()

class ChangeEmail(forms.Form):
    email = forms.EmailField()

class ChangePassword(forms.Form):
    password = forms.PasswordInput()

    oldpassword = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'type':'password', 'placeholder':'your old Password',  'class' : 'span'}))
    newpassword1 = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'type':'password', 'placeholder':'New Password',  'class' : 'span'}))
    newpassword2 = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'type':'password', 'placeholder':'Confirm New Password',  'class' : 'span'}))


    def clean(self):
        if 'newpassword1' in self.cleaned_data and 'newpassword2' in self.cleaned_data:
            if self.cleaned_data['newpassword1'] != self.cleaned_data['newpassword2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data

class ChangePicture(forms.ModelForm):
    #picture = forms.ImageField()
    class Meta:
        model = UserProfile
        fields = ('picture',)

class PhotoForm(forms.ModelForm):
    class Meta:
        model=Photo
        fields=('name', 'photo',)
