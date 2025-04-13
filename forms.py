import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import VendorProfile

User = get_user_model()

# Custom mobile number validator
def validate_mobile(value):
    if not re.match(r'^[6-9]\d{9}$', value):
        raise ValidationError("Enter a valid 10-digit Indian mobile number.")

# Choices for user type
USER_TYPE_CHOICES = [
    ('vendor', 'Vendor'),
    ('customer', 'Customer'),
]

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email Address")
    contact_number = forms.CharField(
        max_length=10,
        validators=[validate_mobile],
        label="Mobile Number"
    )
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        label="I am a"
    )
    brand_name = forms.CharField(
        required=False,
        max_length=100,
        label="Brand / Shop Name (for vendors only)"
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'contact_number',
            'user_type',
            'brand_name',
        ]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get("user_type")
        brand_name = cleaned_data.get("brand_name")

        if user_type == 'vendor' and not brand_name:
            raise ValidationError("Vendors must provide a brand/shop name.")

        return cleaned_data

    def save(self, request=None, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            profile = user.profile  # Assumes OneToOneField to Profile exists
            profile.contact_number = self.cleaned_data["contact_number"]
            profile.user_type = self.cleaned_data["user_type"]
            profile.brand_name = self.cleaned_data.get("brand_name", "")
            profile.save()
        return user

    def signup(self, request, user):
        """
        Required by django-allauth to handle additional signup logic.
        This method is automatically called during social or normal signups.
        """
        user.email = self.cleaned_data.get("email", "")
        user.save()
        profile = user.profile
        profile.contact_number = self.cleaned_data.get("contact_number", "")
        profile.user_type = self.cleaned_data.get("user_type", "")
        profile.brand_name = self.cleaned_data.get("brand_name", "")
        profile.save()

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        })
    )

class VendorProfileForm(forms.ModelForm):
    class Meta:
        model = VendorProfile
        fields = [
            'business_name',
            'services_offered',
            'location',
            'pricing_info',
            'phone_number',
            'website',
        ]
        widgets = {
            'services_offered': forms.Textarea(attrs={'rows': 3}),
            'pricing_info': forms.Textarea(attrs={'rows': 3}),
        }
