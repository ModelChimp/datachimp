from datachimp.models.profile import Profile
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class DatachimpSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        print(data)
