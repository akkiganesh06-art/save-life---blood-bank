from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate 
from .models import Donor
from .forms import (
    DonorRegistrationForm,
    EmergencyRequestForm,
    SignupForm,
    LabTestBookingForm,
    HealthCampRegistrationForm
)
from django.contrib import messages
from .models import (
    Donor,
    ContactRequest,
    EmergencyRequest,
    LabTestBooking,
    HealthCamp,
    HealthCampRegistration)

def home(request):
    return render(request, 'main/home.html')

@login_required
def donor_register(request):

    try:
        donor = request.user.donor_profile
        return redirect('my_profile')

    except Donor.DoesNotExist:
        pass

    if request.method == 'POST':
        form = DonorRegistrationForm(request.POST)

        if form.is_valid():
            donor = form.save(commit=False)
            donor.user = request.user
            donor.save()

            return redirect('my_profile')

    else:
        form = DonorRegistrationForm()

    return render(
        request,
        'main/donor_register.html',
        {'form': form}
    )


def donor_success(request):
    return render(
        request,
        'main/donor_success.html'
    )
    

@login_required
def blood_search(request):

    donors = Donor.objects.all().order_by('-registered_at')

    blood_group = request.GET.get('blood_group', '').strip()
    state = request.GET.get('state', '').strip()
    district = request.GET.get('district', '').strip()
    city = request.GET.get('city', '').strip()
    emergency_only = request.GET.get('emergency_only')

    if blood_group:
        donors = donors.filter(
            blood_group=blood_group
        )

    if state:
        donors = donors.filter(
            state__icontains=state
        )

    if district:
        donors = donors.filter(
            district__icontains=district
        )

    if city:
        donors = donors.filter(
            city__icontains=city
        )

    if emergency_only == 'yes':
        donors = donors.filter(
            available_for_emergency=True
        )

    return render(
        request,
        'main/blood_search.html',
        {
            'donors': donors,
            'blood_group': blood_group,
            'state': state,
            'district': district,
            'city': city,
            'emergency_only': emergency_only,
            'total_donors': donors.count(),
        }
    )

@login_required
def emergency_request(request):

    if request.method == 'POST':

        form = EmergencyRequestForm(request.POST)

        if form.is_valid():

            emergency = form.save(commit=False)

            emergency.user = request.user

            emergency.save()

            return redirect('emergency_success')

    else:

        form = EmergencyRequestForm()

    return render(
        request,
        'main/emergency_request.html',
        {'form': form}
    )
    

def emergency_success(request):

    return render(
        request,
        'main/emergency_success.html'
    )    
def signup(request):

    if request.method == 'POST':

        form = SignupForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('login')

    else:
        form = SignupForm()

    return render(
        request,
        'main/signup.html',
        {'form': form}
    )
def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('dashboard')

        else:

            return render(
                request,
                'main/login.html',
                {
                    'error': 'Invalid username or password.'
                }
            )

    return render(
        request,
        'main/login.html'
    )
    
@login_required
def dashboard(request):
    try:
        donor_profile = request.user.donor_profile
    except Donor.DoesNotExist:
        donor_profile = None

    pending_contact_count = ContactRequest.objects.filter(
        donor__user=request.user,
        status='Pending'
    ).count()

    return render(
        request,
        'main/dashboard.html',
        {
            'donor_profile': donor_profile,
            'pending_contact_count': pending_contact_count,
        }
    )
def user_logout(request):

    logout(request)

    return redirect('home')
    
@login_required
def my_emergency_requests(request):

    requests = request.user.emergency_requests.all().order_by('-created_at')

    return render(
        request,
        'main/my_emergency_requests.html',
        {
            'requests': requests,
        }
    )

@login_required
def my_profile(request):

    try:
        donor_profile = request.user.donor_profile
    except Donor.DoesNotExist:
        donor_profile = None

    return render(
        request,
        'main/my_profile.html',
        {
            'donor_profile': donor_profile,
        }
    )
@login_required
def edit_donor_profile(request):

    try:
        donor_profile = request.user.donor_profile
    except Donor.DoesNotExist:
        return redirect('donor_register')

    if request.method == 'POST':
        form = DonorRegistrationForm(
            request.POST,
            instance=donor_profile
        )

        if form.is_valid():
            form.save()
            return redirect('my_profile')

    else:
        form = DonorRegistrationForm(
            instance=donor_profile
        )

    return render(
        request,
        'main/edit_donor_profile.html',
        {
            'form': form,
            'donor_profile': donor_profile,
        }
    )
@login_required
def request_contact(request, donor_id):

    if request.method != 'POST':
        return redirect('blood_search')

    donor = get_object_or_404(Donor, id=donor_id)

    # Prevent users from requesting their own contact details
    if donor.user_id == request.user.id:
        messages.error(request, "You cannot request your own contact details.")
        return redirect('blood_search')

    # Check whether a request already exists
    existing_request = ContactRequest.objects.filter(
        requester=request.user,
        donor=donor
    ).first()

    if existing_request:

        messages.info(
            request,
            f"You have already sent a request. Current status: {existing_request.status}."
        )

    else:

        ContactRequest.objects.create(
            requester=request.user,
            donor=donor
        )

        messages.success(
            request,
            "Your contact request has been sent to the donor successfully!"
        )

    return redirect('blood_search')    
@login_required
def request_donor_contact(request, donor_id):

    if request.method != 'POST':
        return redirect('blood_search')

    donor = get_object_or_404(Donor, id=donor_id)

    # Prevent users from requesting their own contact details
    if donor.user_id == request.user.id:
        messages.warning(
            request,
            "You cannot request your own contact details."
        )
        return redirect('blood_search')

    # Check whether a request already exists
    contact_request = ContactRequest.objects.filter(
        requester=request.user,
        donor=donor
    ).first()

    if contact_request:

        if contact_request.status in ['Pending', 'Approved']:
            messages.info(
                request,
                "You have already requested this donor's contact details."
            )
            return redirect('blood_search')

        # Allow a new request after an earlier rejection
        contact_request.status = 'Pending'
        contact_request.save()

    else:

        ContactRequest.objects.create(
            requester=request.user,
            donor=donor,
            status='Pending'
        )

    messages.success(
        request,
        "Your contact request has been sent to the donor."
    )

    return redirect('blood_search')    

@login_required
def my_contact_requests(request):
    contact_requests = ContactRequest.objects.filter(
        requester=request.user
    ).select_related('donor').order_by('-created_at')

    return render(
        request,
        'main/my_contact_requests.html',
        {
            'contact_requests': contact_requests
        }
    )


@login_required
def received_contact_requests(request):
    try:
        donor = request.user.donor_profile
    except Donor.DoesNotExist:
        messages.warning(
            request,
            "Please register as a donor before viewing contact requests."
        )
        return redirect('donor_register')

    contact_requests = ContactRequest.objects.filter(
        donor=donor
    ).select_related('requester').order_by('-created_at')

    return render(
        request,
        'main/received_contact_requests.html',
        {
            'contact_requests': contact_requests
        }
    )


@login_required
def update_contact_request(request, request_id):
    if request.method != 'POST':
        return redirect('received_contact_requests')

    try:
        donor = request.user.donor_profile
    except Donor.DoesNotExist:
        messages.error(request, "You are not registered as a donor.")
        return redirect('dashboard')

    contact_request = get_object_or_404(
        ContactRequest,
        id=request_id,
        donor=donor
    )

    action = request.POST.get('action')

    if contact_request.status != 'Pending':
        messages.info(
            request,
            "This request has already been processed."
        )
        return redirect('received_contact_requests')

    if action == 'approve':
        contact_request.status = 'Approved'
        contact_request.save(update_fields=['status'])
        messages.success(
            request,
            "You approved the contact request."
        )

    elif action == 'reject':
        contact_request.status = 'Rejected'
        contact_request.save(update_fields=['status'])
        messages.success(
            request,
            "You rejected the contact request."
        )

    else:
        messages.error(request, "Invalid request action.")

    return redirect('received_contact_requests')
@login_required
def lab_test_booking(request):

    if request.method == 'POST':
        form = LabTestBookingForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()

            messages.success(
                request,
                "Your lab test booking has been submitted successfully!"
            )

            return redirect('lab_test_booking')

    else:
        form = LabTestBookingForm()

    return render(
        request,
        'main/lab_test_booking.html',
        {'form': form}
    )    
@login_required
def my_lab_bookings(request):

    bookings = LabTestBooking.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'main/my_lab_bookings.html',
        {'bookings': bookings}
    )    
def health_camps(request):

    camps = HealthCamp.objects.filter(
        status__in=['Upcoming', 'Ongoing']
    ).order_by('camp_date')

    return render(
        request,
        'main/health_camps.html',
        {'camps': camps}
    )    
@login_required
def register_health_camp(request, camp_id):

    camp = get_object_or_404(HealthCamp, id=camp_id)

    # Check whether the user has already registered
    already_registered = HealthCampRegistration.objects.filter(
        user=request.user,
        camp=camp
    ).exists()

    if already_registered:
        messages.info(
            request,
            "You have already registered for this health camp."
        )
        return redirect('health_camps')

    if request.method == 'POST':
        form = HealthCampRegistrationForm(request.POST)

        if form.is_valid():
            registration = form.save(commit=False)
            registration.user = request.user
            registration.camp = camp
            registration.save()

            messages.success(
                request,
                "You have successfully registered for this health camp!"
            )

            return redirect('health_camps')

    else:
        form = HealthCampRegistrationForm()

    return render(
        request,
        'main/health_camp_register.html',
        {
            'form': form,
            'camp': camp
        }
    )
@login_required
def my_health_camp_registrations(request):

    registrations = HealthCampRegistration.objects.filter(
        user=request.user
    ).select_related('camp').order_by('-registration_date')

    return render(
        request,
        'main/my_health_camp_registrations.html',
        {
            'registrations': registrations
        }
    )
            