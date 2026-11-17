from django.db import models
class Donor(models.Model):

    user = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='donor_profile'
    )

    BLOOD_GROUPS = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    blood_group = models.CharField(
        max_length=3,
        choices=BLOOD_GROUPS
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    age = models.PositiveIntegerField()
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()

    last_donation_date = models.DateField(
        null=True,
        blank=True
    )

    available_for_emergency = models.BooleanField(
        default=True
    )

    registered_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.full_name} - {self.blood_group}"


class EmergencyRequest(models.Model):

    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='emergency_requests'
    )

    BLOOD_GROUPS = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    patient_name = models.CharField(max_length=100)

    blood_group = models.CharField(
        max_length=3,
        choices=BLOOD_GROUPS
    )

    units_required = models.PositiveIntegerField(default=1)

    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    hospital_name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=15)

    required_date = models.DateField()
    emergency_message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Contacted', 'Donor Contacted'),
        ('Fulfilled', 'Fulfilled'),
        ('Cancelled', 'Cancelled'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    def __str__(self):
        return f"{self.patient_name} - {self.blood_group}"
    
class ContactRequest(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    requester = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='sent_contact_requests'
    )

    donor = models.ForeignKey(
        Donor,
        on_delete=models.CASCADE,
        related_name='received_contact_requests'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.requester.username} → {self.donor.full_name} ({self.status})"    
class LabTestBooking(models.Model):

    COLLECTION_CHOICES = [
        ('Lab Visit', 'Lab Visit'),
        ('Home Collection', 'Home Collection'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='lab_bookings'
    )

    patient_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    test_name = models.CharField(max_length=150)

    preferred_date = models.DateField()

    collection_type = models.CharField(
        max_length=30,
        choices=COLLECTION_CHOICES
    )

    address = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} - {self.test_name}"

class HealthCamp(models.Model):

    STATUS_CHOICES = [
        ('Upcoming', 'Upcoming'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    camp_name = models.CharField(max_length=150)
    description = models.TextField()

    organizer = models.CharField(max_length=150)

    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    location = models.TextField()

    camp_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    services = models.TextField(
        help_text="Example: Blood Test, Blood Donation, Free Checkup"
    )

    contact_number = models.CharField(max_length=15)

    is_free = models.BooleanField(default=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Upcoming'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.camp_name

class HealthCampRegistration(models.Model):

    STATUS_CHOICES = [
        ('Registered', 'Registered'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='health_camp_registrations'
    )

    camp = models.ForeignKey(
        HealthCamp,
        on_delete=models.CASCADE,
        related_name='registrations'
    )

    participant_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    registration_date = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Registered'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'camp'],
                name='unique_user_health_camp'
            )
        ]

    def __str__(self):
        return f"{self.participant_name} - {self.camp.camp_name}"
        