from django import forms

from workshop.models import Workshop


class WorkshopOnboardingForm(forms.Form):

    # =========================================================
    # WORKSHOP DETAILS
    # =========================================================

    workshop_name = forms.CharField(
        max_length=150,
        label="Workshop Name"
    )

    workshop_type = forms.ChoiceField(
        choices=Workshop.WORKSHOP_TYPE_CHOICES,
        label="Workshop Type"
    )

    phone_number = forms.CharField(
        max_length=20,
        label="Workshop Phone Number"
    )

    email = forms.EmailField(
        required=False,
        label="Workshop Email"
    )

    location = forms.CharField(
        max_length=150,
        label="Location"
    )

    address = forms.CharField(
        required=False,
        label="Address",
        widget=forms.Textarea(
            attrs={
                "rows": 3,
            }
        )
    )

    # =========================================================
    # OWNER ACCOUNT
    # =========================================================

    owner_first_name = forms.CharField(
        max_length=150,
        label="Owner First Name"
    )

    owner_last_name = forms.CharField(
        max_length=150,
        required=False,
        label="Owner Last Name"
    )

    owner_username = forms.CharField(
        max_length=150,
        label="Owner Username"
    )

    owner_email = forms.EmailField(
        required=False,
        label="Owner Email"
    )

    temporary_password = forms.CharField(
        label="Temporary Password",
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        label="Confirm Temporary Password",
        widget=forms.PasswordInput
    )

    # =========================================================
    # VALIDATION
    # =========================================================

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get("temporary_password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:

            if password != confirm_password:

                self.add_error(
                    "confirm_password",
                    "The passwords do not match."
                )

        return cleaned_data


# =========================================================
# WORKSHOP STAFF ACCOUNT FORM
# =========================================================

class StaffAccountForm(forms.Form):

    first_name = forms.CharField(
        max_length=150,
        label="First Name"
    )

    last_name = forms.CharField(
        max_length=150,
        required=False,
        label="Last Name"
    )

    username = forms.CharField(
        max_length=150,
        label="Username"
    )

    email = forms.EmailField(
        required=False,
        label="Email"
    )

    role = forms.ChoiceField(
        choices=[
            ("owner", "Owner"),
            ("manager", "Manager"),
            ("advisor", "Service Advisor"),
            ("technician", "Technician"),
        ],
        label="Role"
    )

    temporary_password = forms.CharField(
        label="Temporary Password",
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        label="Confirm Temporary Password",
        widget=forms.PasswordInput
    )

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get(
            "temporary_password"
        )

        confirm_password = cleaned_data.get(
            "confirm_password"
        )

        if password and confirm_password:

            if password != confirm_password:

                self.add_error(
                    "confirm_password",
                    "The passwords do not match."
                )

        return cleaned_data

# =========================================================
# EDIT WORKSHOP STAFF ACCOUNT
# =========================================================

class StaffEditForm(forms.Form):

    first_name = forms.CharField(
        max_length=150,
        label="First Name"
    )

    last_name = forms.CharField(
        max_length=150,
        required=False,
        label="Last Name"
    )

    username = forms.CharField(
        max_length=150,
        label="Username"
    )

    email = forms.EmailField(
        required=False,
        label="Email"
    )

    role = forms.ChoiceField(
        choices=[
            ("owner", "Owner"),
            ("manager", "Manager"),
            ("advisor", "Service Advisor"),
            ("technician", "Technician"),
        ],
        label="Role"
    )

# =========================================================
# RESET WORKSHOP STAFF PASSWORD
# =========================================================

class StaffPasswordResetForm(forms.Form):

    new_password = forms.CharField(
        label="New Temporary Password",
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        label="Confirm Temporary Password",
        widget=forms.PasswordInput
    )

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:

            if password != confirm_password:

                self.add_error(
                    "confirm_password",
                    "The passwords do not match."
                )

        return cleaned_data