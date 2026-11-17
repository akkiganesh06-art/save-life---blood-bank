from django import forms
from django.contrib.auth.models import User

from .models import (
    Donor,
    EmergencyRequest,
    LabTestBooking,
    HealthCampRegistration
)
class DonorRegistrationForm(forms.ModelForm):

    class Meta:
        model = Donor

        fields = [
            'full_name',
            'email',
            'phone',
            'blood_group',
            'gender',
            'age',
            'state',
            'district',
            'city',
            'address',
            'last_donation_date',
            'available_for_emergency',
        ]

        widgets = {
            'last_donation_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }
        
class DonorRegistrationForm(forms.ModelForm):

    class Meta:
        model = Donor

        fields = [
            'full_name',
            'email',
            'phone',
            'blood_group',
            'gender',
            'age',
            'state',
            'district',
            'city',
            'address',
            'last_donation_date',
            'available_for_emergency',
        ]

        widgets = {
            'last_donation_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }


class EmergencyRequestForm(forms.ModelForm):

    class Meta:
        model = EmergencyRequest

        fields = [
            'patient_name',
            'blood_group',
            'units_required',
            'state',
            'district',
            'city',
            'hospital_name',
            'contact_number',
            'required_date',
            'emergency_message',
        ]

        widgets = {
            'required_date': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'emergency_message': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Enter emergency details'
                }
            ),
        }        
class SignupForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'password',
        ]

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError(
                    "Passwords do not match."
                )

        return cleaned_data

    def save(self, commit=True):

        user = super().save(commit=False)

        user.set_password(
            self.cleaned_data['password']
        )

        if commit:
            user.save()

        return user        
class LabTestBookingForm(forms.ModelForm):

    class Meta:
        model = LabTestBooking

        fields = [
            'patient_name',
            'phone',
            'test_name',
            'preferred_date',
            'collection_type',
            'address',
        ]

        widgets = {
            'preferred_date': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'address': forms.Textarea(
                attrs={'rows': 3}
            ),
        }    

class HealthCampRegistrationForm(forms.ModelForm):

    class Meta:
        model = HealthCampRegistration

        fields = [
            'participant_name',
            'phone',
            'email',
        ]

        widgets = {
            'participant_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter your full name'
                }
            ),

            'phone': forms.TextInput(
                attrs={
                    'placeholder': 'Enter your mobile number'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Enter your email address'
                }
            ),
        }
        