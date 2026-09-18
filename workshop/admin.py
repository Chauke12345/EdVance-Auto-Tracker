from django.contrib import admin

from .models import (
    Workshop,
    StaffProfile,
    Customer,
    Vehicle,
    RepairJob,
    JobPhoto,
    JobNote,
)


# =========================================================
# WORKSHOP ADMIN
# =========================================================

@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "workshop_type",
        "location",
        "phone_number",
        "is_active",
        "created_at",
    )

    list_filter = (
        "workshop_type",
        "is_active",
    )

    search_fields = (
        "name",
        "location",
        "phone_number",
    )


# =========================================================
# STAFF PROFILE ADMIN
# =========================================================

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "workshop",
        "role",
        "is_active",
    )

    list_filter = (
        "workshop",
        "role",
        "is_active",
    )

    search_fields = (
        "user__username",
        "workshop__name",
    )


# =========================================================
# CUSTOMER ADMIN
# =========================================================

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = (
        "full_name",
        "phone_number",
        "workshop",
        "created_at",
    )

    list_filter = (
        "workshop",
    )

    search_fields = (
        "full_name",
        "phone_number",
        "email",
    )


# =========================================================
# VEHICLE ADMIN
# =========================================================

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):

    list_display = (
        "registration_number",
        "make",
        "model",
        "year",
        "customer",
    )

    search_fields = (
        "registration_number",
        "make",
        "model",
        "vin_number",
        "customer__full_name",
    )


# =========================================================
# REPAIR JOB ADMIN
# =========================================================

@admin.register(RepairJob)
class RepairJobAdmin(admin.ModelAdmin):

    list_display = (
        "tracking_number",
        "vehicle",
        "workshop",
        "status",
        "assigned_to",
        "estimated_completion_date",
        "created_at",
    )

    list_filter = (
        "workshop",
        "status",
        "created_at",
    )

    search_fields = (
        "tracking_number",
        "vehicle__registration_number",
        "vehicle__make",
        "vehicle__model",
        "vehicle__customer__full_name",
    )

    readonly_fields = (
        "tracking_number",
        "created_at",
        "updated_at",
    )


# =========================================================
# JOB PHOTO ADMIN
# =========================================================

@admin.register(JobPhoto)
class JobPhotoAdmin(admin.ModelAdmin):

    list_display = (
        "repair_job",
        "photo_type",
        "description",
        "uploaded_at",
    )

    list_filter = (
        "photo_type",
    )


# =========================================================
# JOB NOTE ADMIN
# =========================================================

@admin.register(JobNote)
class JobNoteAdmin(admin.ModelAdmin):

    list_display = (
        "repair_job",
        "staff",
        "created_at",
    )

    search_fields = (
        "repair_job__tracking_number",
        "note",
    )