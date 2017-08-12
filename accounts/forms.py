from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    get_user_model,)

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    # login form validation
    def clean(self, *args, **kwargs): #the clean method is called in the view using form.is_valid()
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            #method 1
            user = authenticate(username=username, password=password) # checks if the username matches any in the db(User model)
            #method 2
	        #user_qs = User.objects.filter(username=username)
            #if user_qs.count() == 1:
            #    user = user_qs.first()
            #else:
            #    user = None
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect Password")
            if not user.is_active:
                raise forms.ValidationError("This user is no longer active")
        #if no errors, return the data from the form
        return super(UserLoginForm, self).clean(*args, **kwargs)