from allauth.account.adapter import DefaultAccountAdapter
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

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
        user = super().save_user(request, user, form, commit=False)
        user.email = self.clean_email(form.cleaned_data['email'])
        if commit:
            user.save()
        return user