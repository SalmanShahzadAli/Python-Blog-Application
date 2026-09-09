from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.views import ConnectionsView

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Account created! Please wait for admin approval before logging in."
            )
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

class StyledAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Email",
        widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = StyledAuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_approved:
            messages.error(
                self.request,
                "Your account is pending admin approval. Please check back later."
            )
            return redirect('accounts:login')
        return super().form_valid(form)

class CustomConnectionsView(ConnectionsView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registered_providers'] = list(
            SocialApp.objects.values_list('provider', flat=True)
        )
        return context