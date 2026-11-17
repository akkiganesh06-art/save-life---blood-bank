
from django.contrib import admin
from .models import (
    Donor,
    EmergencyRequest,
    ContactRequest,
    LabTestBooking,
    HealthCamp,
    HealthCampRegistration
)

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'blood_group',
        'phone',
        'city',
        'district',
        'available_for_emergency',
    )

    list_filter = (
        'blood_group',
        'state',
        'available_for_emergency',
    )

    search_fields = (
        'full_name',
        'phone',
        'city',
        'district',
    )


@admin.register(EmergencyRequest)
class EmergencyRequestAdmin(admin.ModelAdmin):
    list_display = (
        'patient_name',
        'blood_group',
        'units_required',
        'hospital_name',
        'required_date',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'blood_group',
        'state',
    )

    search_fields = (
        'patient_name',
        'hospital_name',
        'contact_number',
    )

    list_editable = ('status',)
    readonly_fields = ('created_at',)


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = (
        'requester',
        'donor',
        'status',
        'created_at',
        'updated_at',
    )

    list_filter = (
        'status',
        'created_at',
    )

    search_fields = (
        'requester__username',
        'donor__full_name',
        'donor__phone',
    )

    readonly_fields = (
        'requester',
        'donor',
        'created_at',
        'updated_at',
    )
@admin.register(LabTestBooking)
class LabTestBookingAdmin(admin.ModelAdmin):

    list_display = (
        'patient_name',
        'test_name',
        'phone',
        'preferred_date',
        'collection_type',
        'status',
    )

    list_filter = (
        'status',
        'collection_type',
        'preferred_date',
    )

    search_fields = (
        'patient_name',
        'phone',
        'test_name',
    )
@admin.register(HealthCamp)
class HealthCampAdmin(admin.ModelAdmin):

    list_display = (
        'camp_name',
        'organizer',
        'state',
        'district',
        'camp_date',
        'start_time',
        'status',
        'is_free',
    )

    list_filter = (
        'status',
        'is_free',
        'state',
        'camp_date',
    )

    search_fields = (
        'camp_name',
        'organizer',
        'state',
        'district',
        'location',
    )

    list_editable = (
        'status',
        'is_free',
    )    
@admin.register(HealthCampRegistration)
class HealthCampRegistrationAdmin(admin.ModelAdmin):

    list_display = (
        'participant_name',
        'camp',
        'phone',
        'email',
        'registration_date',
        'status',
    )

    list_filter = (
        'status',
        'registration_date',
        'camp',
    )

    search_fields = (
        'participant_name',
        'phone',
        'email',
        'camp__camp_name',
    )

    list_editable = (
        'status',
    )

    readonly_fields = (
        'registration_date',
    )    