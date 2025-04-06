from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CustomAccountAdapter(DefaultAccountAdapter):
    def clean_email(self, email):
        email = super().clean_email(email)
        User = get_user_model()

        # Only check email uniqueness during registration
        if self.request and self.request.path.startswith('/api/v1/auth/registration/'):
            if email and User.objects.filter(email=email).exists():
                raise ValidationError(
                    _('A user is already registered with this email address.')
                )

        return email

    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the signup form.
        """
        user = super().save_user(request, user, form, commit=False)
        
        # Set default avatar
        if not user.avatar:
            user.avatar = "https://res.cloudinary.com/dloeqfbwm/image/upload/v1742014468/ztudy/avatars/default_avatar.jpg"
            
        user.email = self.clean_email(form.cleaned_data['email'])
        if commit:
            user.save()
        return user


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        """
        Populate user instance using data from social provider.
        """
        user = super().populate_user(request, sociallogin, data)
        
        # Get profile picture from social account
        if sociallogin.account.provider == 'google':
            extra_data = sociallogin.account.extra_data
            if extra_data.get('picture'):
                user.avatar = extra_data['picture']
                
        return user

    def save_user(self, request, sociallogin, form=None):
        """
        Save the newly created user instance.
        """
        user = super().save_user(request, sociallogin, form)
        
        # Update user info after saving
        if sociallogin.account.provider == 'google':
            extra_data = sociallogin.account.extra_data
            if extra_data.get('picture'):
                user.avatar = extra_data['picture']
                user.save()
                
        return user
