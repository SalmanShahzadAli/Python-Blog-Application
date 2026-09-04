from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import redirect
from django.contrib import messages


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Called after a user authenticates via Google/Facebook,
        but BEFORE they're logged into our site.
        We use this hook to enforce our admin-approval rule.
        """
        user = sociallogin.user

        # If this is a brand new social signup, is_approved defaults to False
        # (handled by our CustomUser model default). Existing users: check their flag.
        if user.pk and not user.is_approved:
            messages.error(
                request,
                "Your account is pending admin approval. Please check back later."
            )
            raise ImmediateHttpResponse(redirect('accounts:login'))