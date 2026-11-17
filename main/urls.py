from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'donor/register/',
        views.donor_register,
        name='donor_register'
    ),

    path(
        'donor/success/',
        views.donor_success,
        name='donor_success'
    ),
    
    path(
    'blood-search/',
    views.blood_search,
    name='blood_search'
    ),
    
    path(
    'emergency/',
    views.emergency_request,
    name='emergency_request'
),

path(
    'emergency/success/',
    views.emergency_success,
    name='emergency_success'
),
path(
    'signup/',
    views.signup,
    name='signup'
),

path(
    'login/',
    views.user_login,
    name='login'
),
path(
    'dashboard/',
    views.dashboard,
    name='dashboard'
),
path(
    'logout/',
    views.user_logout,
    name='logout'
),
path(
    'my-emergency-requests/',
    views.my_emergency_requests,
    name='my_emergency_requests'
),

path(
    'my-profile/',
    views.my_profile,
    name='my_profile'
),

path(
    'my-profile/edit/',
    views.edit_donor_profile,
    name='edit_donor_profile'
),
path(
    'request-contact/<int:donor_id>/',
    views.request_contact,
    name='request_contact'
),
path(
    'request-contact/<int:donor_id>/',
    views.request_donor_contact,
    name='request_donor_contact'
),
path(
    'my-contact-requests/',
    views.my_contact_requests,
    name='my_contact_requests'
),
path(
    'received-contact-requests/',
    views.received_contact_requests,
    name='received_contact_requests'
),

path(
    'update-contact-request/<int:request_id>/',
    views.update_contact_request,
    name='update_contact_request'
),
path(
    'lab-test-booking/',
    views.lab_test_booking,
    name='lab_test_booking'
),
path(
    'my-lab-bookings/',
    views.my_lab_bookings,
    name='my_lab_bookings'
),
path(
    'health-camps/',
    views.health_camps,
    name='health_camps'
),
path(
    'register-health-camp/<int:camp_id>/',
    views.register_health_camp,
    name='register_health_camp'
),
path(
    'my-health-camp-registrations/',
    views.my_health_camp_registrations,
    name='my_health_camp_registrations'
),
    # FORGOT PASSWORD

    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='main/password_reset.html',
           email_template_name='registration/password_reset_email.html',
subject_template_name='registration/password_reset_subject.txt',
            success_url='/password-reset/done/'
        ),
        name='password_reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',
            success_url='/reset/done/'
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
    
]