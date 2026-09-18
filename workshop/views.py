from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from .models import (
    StaffProfile,
    RepairJob,
    Customer,
    Vehicle,
    JobPhoto,
    JobStatusHistory,
)

from .forms import (
    CustomerForm,
    VehicleForm,
    RepairJobForm,
    RepairJobStatusForm,
    JobNoteForm,
    JobPhotoForm,
    CustomerTrackingForm,
)
# =========================================================
# STAFF LOGIN
# =========================================================

def staff_login(request):

    # Already logged in
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            try:
                staff_profile = user.workshop_staff_profile
            except StaffProfile.DoesNotExist:
                messages.error(
                    request,
                    "This account is not connected to a workshop."
                )
                return redirect("staff_login")

            if not staff_profile.is_active:
                messages.error(
                    request,
                    "Your staff account is inactive."
                )
                return redirect("staff_login")

            if not staff_profile.workshop.is_active:
                messages.error(
                    request,
                    "This workshop is currently inactive."
                )
                return redirect("staff_login")

            login(request, user)

            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "workshop/login.html"
    )


# =========================================================
# STAFF LOGOUT
# =========================================================

def staff_logout(request):

    logout(request)

    return redirect("staff_login")


# =========================================================
# WORKSHOP DASHBOARD
# =========================================================

@login_required(login_url="staff_login")
def dashboard(request):

    # =========================================================
    # GET STAFF PROFILE
    # =========================================================

    try:
        staff_profile = request.user.workshop_staff_profile

    except StaffProfile.DoesNotExist:

        logout(request)

        messages.error(
            request,
            "Your account is not connected to a workshop."
        )

        return redirect("staff_login")


    # =========================================================
    # CHECK STAFF ACCOUNT
    # =========================================================

    if not staff_profile.is_active:

        logout(request)

        messages.error(
            request,
            "Your staff account is inactive."
        )

        return redirect("staff_login")


    # =========================================================
    # GET WORKSHOP
    # =========================================================

    workshop = staff_profile.workshop


    # =========================================================
    # CHECK WORKSHOP ACCOUNT
    # =========================================================

    if not workshop.is_active:

        logout(request)

        messages.error(
            request,
            "This workshop is currently inactive."
        )

        return redirect("staff_login")


    # =========================================================
    # ALL REPAIR JOBS
    # =========================================================

    repair_jobs = RepairJob.objects.filter(
        workshop=workshop
    ).select_related(
        "vehicle",
        "vehicle__customer",
        "assigned_to",
        "assigned_to__user",
    ).order_by(
        "-created_at"
    )


    # =========================================================
    # ACTIVE REPAIR JOBS + STATUS FILTER
    # =========================================================

    # Everything except vehicles already collected
    active_jobs = repair_jobs.exclude(
        status="collected"
    )

    # Get selected status from the dashboard
    status_filter = request.GET.get(
        "status",
        "all"
    )

    # Statuses that can be filtered
    allowed_statuses = [
        "check_in",
        "assessment",
        "awaiting_approval",
        "awaiting_parts",
        "repair",
        "quality_check",
        "ready",
    ]

    # Apply selected filter
    if status_filter in allowed_statuses:
        active_jobs = active_jobs.filter(
            status=status_filter
        )


    # =========================================================
    # COMPLETED / COLLECTED JOBS
    # =========================================================

    completed_jobs = repair_jobs.filter(
        status="collected"
    )


    # =========================================================
    # CUSTOMERS
    # =========================================================

    customers = Customer.objects.filter(
        workshop=workshop
    )


    # =========================================================
    # VEHICLES
    # =========================================================

    vehicles = Vehicle.objects.filter(
        customer__workshop=workshop
    )


    # =========================================================
    # DASHBOARD COUNTERS
    # =========================================================

    customer_count = customers.count()

    vehicle_count = vehicles.count()

    job_count = repair_jobs.count()

    active_job_count = active_jobs.count()

    completed_job_count = completed_jobs.count()


    # =========================================================
    # PAGE CONTEXT
    # =========================================================

    context = {

        "staff_profile": staff_profile,

        "workshop": workshop,

        # Jobs
        "repair_jobs": repair_jobs,
        "active_jobs": active_jobs,
        "completed_jobs": completed_jobs,
        "status_filter": status_filter,

        # Counters
        "customer_count": customer_count,
        "vehicle_count": vehicle_count,
        "job_count": job_count,
        "active_job_count": active_job_count,
        "completed_job_count": completed_job_count,
    }


    # =========================================================
    # RENDER DASHBOARD
    # =========================================================

    return render(
        request,
        "workshop/dashboard.html",
        context
    )
# =========================================================
# REGISTER CUSTOMER
# =========================================================

@login_required(login_url="staff_login")
def register_customer(request):

    try:
        staff_profile = request.user.workshop_staff_profile
    except StaffProfile.DoesNotExist:
        logout(request)
        messages.error(
            request,
            "Your account is not connected to a workshop."
        )
        return redirect("staff_login")

    if not staff_profile.is_active:
        logout(request)
        messages.error(
            request,
            "Your staff account is inactive."
        )
        return redirect("staff_login")

    workshop = staff_profile.workshop

    if not workshop.is_active:
        logout(request)
        messages.error(
            request,
            "This workshop is currently inactive."
        )
        return redirect("staff_login")

    if request.method == "POST":

        form = CustomerForm(request.POST)

        if form.is_valid():

            customer = form.save(commit=False)

            # Automatically connect customer
            # to logged-in staff member's workshop
            customer.workshop = workshop

            customer.save()

            messages.success(
                request,
                f"{customer.full_name} has been registered successfully."
            )

            return redirect("dashboard")

    else:

        form = CustomerForm()

    context = {
        "form": form,
        "workshop": workshop,
        "staff_profile": staff_profile,
    }

    return render(
        request,
        "workshop/register_customer.html",
        context
    )

# =========================================================
# REGISTER VEHICLE
# =========================================================

@login_required(login_url="staff_login")
def register_vehicle(request):

    try:
        staff_profile = request.user.workshop_staff_profile
    except StaffProfile.DoesNotExist:
        logout(request)
        messages.error(
            request,
            "Your account is not connected to a workshop."
        )
        return redirect("staff_login")

    workshop = staff_profile.workshop

    if not staff_profile.is_active or not workshop.is_active:
        logout(request)
        messages.error(
            request,
            "Your workshop account is inactive."
        )
        return redirect("staff_login")

    if request.method == "POST":

        form = VehicleForm(
            request.POST
        )

        # Only allow customers from this workshop
        form.fields["customer"].queryset = Customer.objects.filter(
            workshop=workshop
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Vehicle registered successfully."
            )

            return redirect("dashboard")

    else:

        form = VehicleForm()

        # Only show customers belonging to this workshop
        form.fields["customer"].queryset = Customer.objects.filter(
            workshop=workshop
        )

    context = {
        "form": form,
        "workshop": workshop,
        "staff_profile": staff_profile,
    }

    return render(
        request,
        "workshop/register_vehicle.html",
        context
    )

# =========================================================
# CREATE REPAIR JOB
# =========================================================

@login_required(login_url="staff_login")
def create_repair_job(request):

    # =========================================================
    # GET LOGGED-IN STAFF PROFILE
    # =========================================================

    try:
        staff_profile = request.user.workshop_staff_profile

    except StaffProfile.DoesNotExist:

        logout(request)

        messages.error(
            request,
            "Your account is not connected to a workshop."
        )

        return redirect("staff_login")


    # =========================================================
    # GET WORKSHOP
    # =========================================================

    workshop = staff_profile.workshop


    # =========================================================
    # CHECK STAFF AND WORKSHOP ARE ACTIVE
    # =========================================================

    if not staff_profile.is_active or not workshop.is_active:

        logout(request)

        messages.error(
            request,
            "Your workshop account is inactive."
        )

        return redirect("staff_login")


    # =========================================================
    # CREATE FORM
    # =========================================================

    if request.method == "POST":

        form = RepairJobForm(
            request.POST
        )

    else:

        form = RepairJobForm()


    # =========================================================
    # FILTER VEHICLES BY WORKSHOP
    # =========================================================

    form.fields["vehicle"].queryset = Vehicle.objects.filter(
        customer__workshop=workshop
    ).select_related(
        "customer"
    )


    # =========================================================
    # FILTER STAFF BY WORKSHOP
    # =========================================================

    form.fields["assigned_to"].queryset = StaffProfile.objects.filter(
        workshop=workshop,
        is_active=True
    ).select_related(
        "user"
    )


    # =========================================================
    # SAVE REPAIR JOB
    # =========================================================

    if request.method == "POST" and form.is_valid():

        repair_job = form.save(
            commit=False
        )

        # Automatically connect the job
        # to the logged-in workshop
        repair_job.workshop = workshop

        # Every new repair job begins
        # at the Checked In stage
        repair_job.status = "check_in"

        repair_job.save()


        # =====================================================
        # CREATE INITIAL STATUS HISTORY
        # =====================================================

        JobStatusHistory.objects.create(
            repair_job=repair_job,
            status=repair_job.status,
            changed_by=staff_profile,
        )


        # =====================================================
        # SUCCESS MESSAGE
        # =====================================================

        messages.success(
            request,
            f"Repair job {repair_job.tracking_number} created successfully."
        )

        return redirect(
            "dashboard"
        )


    # =========================================================
    # PAGE CONTEXT
    # =========================================================

    context = {
        "form": form,
        "workshop": workshop,
        "staff_profile": staff_profile,
    }


    # =========================================================
    # RENDER PAGE
    # =========================================================

    return render(
        request,
        "workshop/create_repair_job.html",
        context
    )

# =========================================================
# REPAIR JOB DETAIL
# =========================================================

@login_required(login_url="staff_login")
def repair_job_detail(request, tracking_number):

    try:
        staff_profile = request.user.workshop_staff_profile

    except StaffProfile.DoesNotExist:

        logout(request)

        messages.error(
            request,
            "Your account is not connected to a workshop."
        )

        return redirect("staff_login")

    workshop = staff_profile.workshop

    if not staff_profile.is_active or not workshop.is_active:

        logout(request)

        messages.error(
            request,
            "Your workshop account is inactive."
        )

        return redirect("staff_login")

    # =========================================================
    # GET REPAIR JOB
    # =========================================================

    try:

        repair_job = RepairJob.objects.select_related(
            "vehicle",
            "vehicle__customer",
            "assigned_to",
            "assigned_to__user"
        ).get(
            tracking_number=tracking_number,
            workshop=workshop
        )

    except RepairJob.DoesNotExist:

        messages.error(
            request,
            "Repair job not found."
        )

        return redirect("dashboard")

    # =========================================================
    # FORMS
    # =========================================================

    status_form = RepairJobStatusForm(
        instance=repair_job
    )

    note_form = JobNoteForm()

    photo_form = JobPhotoForm()

    # =========================================================
    # HANDLE FORM SUBMISSIONS
    # =========================================================

    if request.method == "POST":

        form_type = request.POST.get("form_type")

                # -----------------------------------------------------
        # UPDATE JOB STATUS
        # -----------------------------------------------------

        if form_type == "status":

            status_form = RepairJobStatusForm(
                request.POST,
                instance=repair_job
            )

            if status_form.is_valid():

                updated_job = status_form.save()

                # Save this status change to history
                JobStatusHistory.objects.create(
                    repair_job=updated_job,
                    status=updated_job.status,
                    changed_by=staff_profile,
                )

                messages.success(
                    request,
                    f"Job {repair_job.tracking_number} status updated successfully."
                )

                return redirect(
                    "repair_job_detail",
                    tracking_number=repair_job.tracking_number
                )
                

        # -----------------------------------------------------
        # ADD JOB NOTE
        # -----------------------------------------------------

        elif form_type == "note":

            note_form = JobNoteForm(
                request.POST
            )

            if note_form.is_valid():

                job_note = note_form.save(
                    commit=False
                )

                job_note.repair_job = repair_job
                job_note.staff = staff_profile

                job_note.save()

                messages.success(
                    request,
                    "Workshop note added successfully."
                )

                return redirect(
                    "repair_job_detail",
                    tracking_number=repair_job.tracking_number
                )


        # -----------------------------------------------------
        # UPLOAD MULTIPLE JOB PHOTOS
        # -----------------------------------------------------

        elif form_type == "photo":

            photo_form = JobPhotoForm(
                request.POST,
                request.FILES
            )

            if photo_form.is_valid():

                images = photo_form.cleaned_data["images"]

                photo_type = photo_form.cleaned_data[
                    "photo_type"
                ]

                description = photo_form.cleaned_data[
                    "description"
                ]

                for image in images:

                    JobPhoto.objects.create(
                        repair_job=repair_job,
                        image=image,
                        photo_type=photo_type,
                        description=description,
                    )

                messages.success(
                    request,
                    f"{len(images)} repair job photo(s) uploaded successfully."
                )

                return redirect(
                    "repair_job_detail",
                    tracking_number=repair_job.tracking_number
                )

        # =========================================================
    # JOB NOTE HISTORY
    # =========================================================

    job_notes = repair_job.notes.select_related(
        "staff",
        "staff__user"
    ).order_by(
        "-created_at"
    )

    # =========================================================
    # JOB PHOTOS
    # =========================================================

    job_photos = repair_job.photos.all().order_by(
        "-uploaded_at"
    )

    # =========================================================
    # JOB STATUS HISTORY
    # =========================================================

    status_history = repair_job.status_history.select_related(
        "changed_by",
        "changed_by__user"
    ).order_by(
        "-changed_at"
    )

    # =========================================================
    # PAGE CONTEXT
    # =========================================================

    context = {
        "repair_job": repair_job,
        "status_form": status_form,
        "note_form": note_form,
        "photo_form": photo_form,
        "job_notes": job_notes,
        "job_photos": job_photos,
        "status_history": status_history,
        "workshop": workshop,
        "staff_profile": staff_profile,
    }

    return render(
        request,
        "workshop/repair_job_detail.html",
        context
    )
# =========================================================
# CUSTOMER JOB TRACKING
# =========================================================

def customer_tracking(request):

    repair_job = None
    status_history = None
    error_message = None

    if request.method == "POST":

        form = CustomerTrackingForm(
            request.POST
        )

        if form.is_valid():

            tracking_number = form.cleaned_data[
                "tracking_number"
            ].strip()

            phone_number = form.cleaned_data[
                "phone_number"
            ].strip()

            try:

                repair_job = RepairJob.objects.select_related(
                    "vehicle",
                    "vehicle__customer",
                    "workshop"
                ).get(
                    tracking_number__iexact=tracking_number,
                    vehicle__customer__phone_number=phone_number
                )

                # =================================================
                # CUSTOMER-VISIBLE STATUS HISTORY
                # =================================================

                status_history = repair_job.status_history.all().order_by(
                    "changed_at"
                )

            except RepairJob.DoesNotExist:

                error_message = (
                    "No repair job was found with that "
                    "tracking number and phone number."
                )

    else:

        form = CustomerTrackingForm()

    context = {
        "form": form,
        "repair_job": repair_job,
        "status_history": status_history,
        "error_message": error_message,
    }

    return render(
        request,
        "workshop/customer_tracking.html",
        context
    )