from django import forms

from .models import (
    Customer,
    Vehicle,
    RepairJob,
    JobNote,
    JobPhoto,
)

# =========================================================
# CUSTOMER FORM
# =========================================================

class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer

        fields = [
            "full_name",
            "phone_number",
            "email",
        ]

        widgets = {

            "full_name": forms.TextInput(attrs={
                "placeholder": "Customer full name"
            }),

            "phone_number": forms.TextInput(attrs={
                "placeholder": "e.g. 0821234567"
            }),

            "email": forms.EmailInput(attrs={
                "placeholder": "Customer email (optional)"
            }),
        }


# =========================================================
# VEHICLE FORM
# =========================================================

class VehicleForm(forms.ModelForm):

    class Meta:
        model = Vehicle

        fields = [
            "customer",
            "registration_number",
            "make",
            "model",
            "year",
            "colour",
            "vin_number",
        ]

        widgets = {

            "registration_number": forms.TextInput(attrs={
                "placeholder": "e.g. AB 12 CD GP"
            }),

            "make": forms.TextInput(attrs={
                "placeholder": "e.g. Toyota"
            }),

            "model": forms.TextInput(attrs={
                "placeholder": "e.g. Corolla"
            }),

            "year": forms.NumberInput(attrs={
                "placeholder": "e.g. 2020"
            }),

            "colour": forms.TextInput(attrs={
                "placeholder": "e.g. White"
            }),

            "vin_number": forms.TextInput(attrs={
                "placeholder": "Vehicle VIN number"
            }),
        }

        # =========================================================
# REPAIR JOB FORM
# =========================================================

class RepairJobForm(forms.ModelForm):

    class Meta:
        model = RepairJob

        fields = [
            "vehicle",
            "problem_description",
            "mileage",
            "assigned_to",
            "estimated_completion_date",
        ]

        widgets = {

            "problem_description": forms.Textarea(attrs={
                "placeholder": "Describe the customer's complaint or repair required",
                "rows": 5
            }),

            "mileage": forms.NumberInput(attrs={
                "placeholder": "e.g. 125000"
            }),

            "estimated_completion_date": forms.DateInput(attrs={
                "type": "date"
            }),
        }

        # =========================================================
# REPAIR JOB STATUS FORM
# =========================================================

class RepairJobStatusForm(forms.ModelForm):

    class Meta:
        model = RepairJob

        fields = [
            "status",
        ]

        # =========================================================
# JOB NOTE FORM
# =========================================================

class JobNoteForm(forms.ModelForm):

    class Meta:
        model = JobNote

        fields = [
            "note",
        ]

        widgets = {
            "note": forms.Textarea(attrs={
                "placeholder": "Enter workshop update, diagnosis, parts required, or repair progress...",
                "rows": 4,
            }),
        }

 # =========================================================
# MULTIPLE FILE INPUT
# =========================================================

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            "widget",
            MultipleFileInput()
        )
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):

        single_file_clean = super().clean

        if isinstance(data, (list, tuple)):
            result = [
                single_file_clean(file, initial)
                for file in data
            ]
        else:
            result = single_file_clean(
                data,
                initial
            )

        return result


# =========================================================
# JOB PHOTO FORM
# =========================================================

class JobPhotoForm(forms.ModelForm):

    images = MultipleFileField(
        required=True
    )

    class Meta:
        model = JobPhoto

        fields = [
            "photo_type",
            "description",
        ]

        widgets = {

            "description": forms.TextInput(attrs={
                "placeholder": "Describe these photos (optional)"
            }),

        }

        # =========================================================
# CUSTOMER JOB TRACKING FORM
# =========================================================

class CustomerTrackingForm(forms.Form):

    tracking_number = forms.CharField(
        max_length=30,
        label="Tracking Number",
        widget=forms.TextInput(attrs={
            "placeholder": "e.g. ATC-A0A5248F"
        })
    )

    phone_number = forms.CharField(
        max_length=20,
        label="Phone Number",
        widget=forms.TextInput(attrs={
            "placeholder": "e.g. 0821234567"
        })
    )