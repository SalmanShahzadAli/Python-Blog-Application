from django.dispatch import receiver
from django.contrib.auth import logout
from django.contrib import messages
from allauth.account.signals import user_signed_up


@receiver(user_signed_up)
def block_unapproved_signup(request, user, **kwargs):
    """
    Fires immediately after ANY new signup completes (email OR social).
    If the new user isn't approved yet, log them out right away
    so they can't use the one-request window before approval.
    """
    if not user.is_approved:
        logout(request)
        messages.error(
            request,
            "Your account has been created but is pending admin approval. "
            "Please check back later."
        )