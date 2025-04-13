from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.urls import reverse
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetConfirmView,
    PasswordResetDoneView, PasswordResetCompleteView
)
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import VendorProfileForm, SignUpForm, LoginForm
from .models import VendorProfile

# ============================
# Home View with Role Redirection
# ============================

@login_required
def home(request):
    user = request.user
    if hasattr(user, 'profile'):
        if user.profile.user_type == 'vendor':
            return redirect(reverse('vendor_dashboard'))
        elif user.profile.user_type == 'customer':
            return redirect(reverse('customer_dashboard'))
    return redirect('login')

# ============================
# Dashboard Views
# ============================

@login_required(login_url='/accounts/login/')
def vendor_dashboard(request):
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'vendor':
        return redirect('login')
    return render(request, 'vendor/dashboard.html')


@login_required(login_url='/accounts/login/')
def customer_dashboard(request):
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'customer':
        return redirect('login')
    return render(request, 'accounts/customer_dashboard.html')

# ============================
# Vendor Registration View
# ============================

@login_required
def register_vendor(request):
    if hasattr(request.user, 'vendorprofile'):
        return redirect('vendor_dashboard')

    if request.method == 'POST':
        form = VendorProfileForm(request.POST)
        if form.is_valid():
            vendor_profile = form.save(commit=False)
            vendor_profile.user = request.user
            vendor_profile.save()
            return redirect('vendor_dashboard')
    else:
        form = VendorProfileForm()

    return render(request, 'accounts/register_vendor.html', {'form': form})

# ============================
# Signup View
# ============================

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            if hasattr(user, 'profile'):
                if user.profile.user_type == 'vendor':
                    return redirect('vendor_dashboard')
                else:
                    return redirect('customer_dashboard')
            else:
                return redirect('register_vendor')
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})

# ============================
# Login View (Role Based)
# ============================

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if hasattr(user, 'profile'):
                if user.profile.user_type == 'vendor':
                    return redirect('vendor_dashboard')
                elif user.profile.user_type == 'customer':
                    return redirect('customer_dashboard')
            else:
                return redirect('register_vendor')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {
        'form': form,
        'social_providers': True  # Used to show social buttons in template
    })

# ============================
# Logout View
# ============================

def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')

# ============================
# Password Reset Flow
# ============================

class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
