from django.forms import  ModelForm
from .models import Newsletter, User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    class Meta:
        model =User
        fields = ['username', 'first_name',  'last_name', 'email', 'password1', 'password2',]
        
        
        
class NewsletterForm(ModelForm):
    class Meta:
        model =Newsletter
        fields = '__all__'
        