from django.conf import settings
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from allauth.account.adapter import DefaultAccountAdapter

class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)
