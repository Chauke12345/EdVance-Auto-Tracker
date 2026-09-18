from django.db import models
from django.contrib.auth.models import User
import uuid


# =========================================================
# WORKSHOP
# =========================================================

class Workshop(models.Model):

    WORKSHOP_TYPE_CHOICES = [
        ("mechanical", "Mechanical Workshop"),
        ("panel_beater", "Panel Beater"),
        ("both", "Mechanical & Panel Beater"),
    ]

    name = models.CharField(max_length=150)

    workshop_type = models.CharField(
        max_length=20,
        choices=WORKSHOP_TYPE_CHOICES,
        default="mechanical"
    )

    phone_number = models.CharField(max_length=20)

    email = models.EmailField(blank=True)

    location = models.CharField(max_length=150)

    address = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# =========================================================
# STAFF PROFILE
# =========================================================

class StaffProfile(models.Model):

    ROLE_CHOICES = [
        ("owner", "Owner"),
        ("manager", "Manager"),
        ("advisor", "Service Advisor"),
        ("technician", "Technician"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="workshop_staff_profile"
    )

    workshop = models.ForeignKey(
        Workshop,
        on_delete=models.CASCADE,
        related_name="staff"
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="technician"
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.workshop.name}"


# =========================================================
# CUSTOMER
# =========================================================

class Customer(models.Model):

    workshop = models.ForeignKey(
        Workshop,
        on_delete=models.CASCADE,
        related_name="customers"
    )

    full_name = models.CharField(max_length=150)

    phone_number = models.CharField(max_length=20)

    email = models.EmailField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


# =========================================================
# VEHICLE
# =========================================================

class Vehicle(models.Model):

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="vehicles"
    )

    registration_number = models.CharField(max_length=30)

    make = models.CharField(max_length=80)

    model = models.CharField(max_length=80)

    year = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    colour = models.CharField(
        max_length=50,
        blank=True
    )

    vin_number = models.CharField(
        max_length=50,
        blank=True
    )

    def __str__(self):
        return (
            f"{self.registration_number} - "
            f"{self.make} {self.model}"
        )


# =========================================================
# REPAIR JOB
# =========================================================

class RepairJob(models.Model):

    STATUS_CHOICES = [
        ("check_in", "Checked In"),
        ("assessment", "Assessment"),
        ("awaiting_approval", "Awaiting Approval"),
        ("awaiting_parts", "Awaiting Parts"),
        ("repair", "Repair In Progress"),
        ("quality_check", "Quality Check"),
        ("ready", "Ready For Collection"),
        ("collected", "Collected"),
    ]

    workshop = models.ForeignKey(
        Workshop,
        on_delete=models.CASCADE,
        related_name="repair_jobs"
    )

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="repair_jobs"
    )

    tracking_number = models.CharField(
        max_length=30,
        unique=True,
        editable=False
    )

    problem_description = models.TextField()

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="check_in"
    )

    mileage = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    assigned_to = models.ForeignKey(
        StaffProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_jobs"
    )

    estimated_completion_date = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        if not self.tracking_number:
            self.tracking_number = (
                f"ATC-{uuid.uuid4().hex[:8].upper()}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.tracking_number} - "
            f"{self.vehicle.registration_number}"
        )


# =========================================================
# JOB PHOTO
# =========================================================

class JobPhoto(models.Model):

    PHOTO_TYPE_CHOICES = [
        ("check_in", "Check-In"),
        ("damage", "Damage"),
        ("progress", "Repair Progress"),
        ("completed", "Completed Repair"),
    ]

    repair_job = models.ForeignKey(
        RepairJob,
        on_delete=models.CASCADE,
        related_name="photos"
    )

    image = models.ImageField(
        upload_to="repair_jobs/"
    )

    photo_type = models.CharField(
        max_length=20,
        choices=PHOTO_TYPE_CHOICES,
        default="progress"
    )

    description = models.CharField(
        max_length=255,
        blank=True
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.repair_job.tracking_number} - "
            f"{self.get_photo_type_display()}"
        )


# =========================================================
# JOB NOTE
# =========================================================

class JobNote(models.Model):

    repair_job = models.ForeignKey(
        RepairJob,
        on_delete=models.CASCADE,
        related_name="notes"
    )

    staff = models.ForeignKey(
        StaffProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    note = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note - {self.repair_job.tracking_number}"

    # =========================================================
# JOB STATUS HISTORY
# =========================================================

class JobStatusHistory(models.Model):

    repair_job = models.ForeignKey(
        RepairJob,
        on_delete=models.CASCADE,
        related_name="status_history"
    )

    status = models.CharField(
        max_length=30,
        choices=RepairJob.STATUS_CHOICES
    )

    changed_by = models.ForeignKey(
        StaffProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="status_changes"
    )

    changed_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.repair_job.tracking_number} - "
            f"{self.get_status_display()}"
        )