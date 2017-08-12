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

class UserRegisterForm(forms.ModelForm):
    error_css_class = "error"
    email =forms.EmailField(label='Email address')
    email2 = forms.EmailField(label='Confirm Email')
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password'
        ]
    #write a clean method for email2 field. Note the order of email and email2 matters here
    #def clean_email2(self): #note, we used email2 not email. otherwise, it will never match
    #	email = self.cleaned_data.get('email')
    #	email2 = self.cleaned_data.get('email2')
    #	if email != email2:
    #		raise forms.ValidationError("Emails must match")
    #    emal_qs = User.objects.filter(email=email)
    #    if emal_qs.exists():
    #    	raise forms.ValidationError("This email has already been registered")
    # 	return email

    #To override the whole clean method. This is better because the order of email and email2 does not matter
    def clean(self, *args, **kwargs): #note, we used email2 not email. otherwise, it will never match
    	email = self.cleaned_data.get('email')
    	email2 = self.cleaned_data.get('email2')
    	if email != email2:
    		raise forms.ValidationError("Emails must match")
        emal_qs = User.objects.filter(email=email)
        if emal_qs.exists():
        	raise forms.ValidationError("This email has already been registered")
    	return super(UserRegisterForm, self).clean(*args, **kwargs)