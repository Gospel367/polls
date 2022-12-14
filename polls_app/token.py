from ast import Pass
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class AccountActivation(PasswordResetTokenGenerator):
    def _make_hash_value(self, user,  timestamp):
        return (
            six.text_type(user.pk)  + six.text_type(user.is_active) + six.text_type(timestamp)
        )
        
account_activation_token =AccountActivation()
    
