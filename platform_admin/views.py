from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from workshop.models import (
    Workshop,
    StaffProfile,
    Customer,
    Vehicle,
    RepairJob,
)

from .forms import WorkshopOnboardingForm, StaffAccountForm, StaffEditForm, StaffPasswordResetForm


# =========================================================
# PLATFORM ACCESS
# =========================================================

def is_platform_admin(user):
    return user.is_authenticated and user.is_superuser


# =========================================================
# EDVANCE TECH PLATFORM DASHBOARD
# =========================================================

@user_passes_test(is_platform_admin, login_url="/admin/login/")
def platform_dashboard(request):

    workshops = Workshop.objects.all().order_by("name")

    connected_workshops = workshops.count()
    active_workshops = workshops.filter(is_active=True).count()
    inactive_workshops = workshops.filter(is_active=False).count()

    customer_count = Customer.objects.count()
    vehicle_count = Vehicle.objects.count()

    repair_jobs = RepairJob.objects.all()

    total_jobs = repair_jobs.count()
    active_jobs = repair_jobs.exclude(status="collected").count()
    completed_jobs = repair_jobs.filter(status="collected").count()

    context = {
        "workshops": workshops,
        "connected_workshops": connected_workshops,
        "active_workshops": active_workshops,
        "inactive_workshops": inactive_workshops,
        "customer_count": customer_count,
        "vehicle_count": vehicle_count,
        "total_jobs": total_jobs,
        "active_jobs": active_jobs,
        "completed_jobs": completed_jobs,
    }

    return render(
        request,
        "platform_admin/dashboard.html",
        context,
    )


# =========================================================
# ADD / ONBOARD WORKSHOP
# =========================================================

@user_passes_test(is_platform_admin, login_url="/admin/login/")
def add_workshop(request):

    if request.method == "POST":

        form = WorkshopOnboardingForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["owner_username"]

            if User.objects.filter(username__iexact=username).exists():

                form.add_error(
                    "owner_username",
                    "A user with this username already exists."
                )

            else:

                with transaction.atomic():

                    workshop = Workshop.objects.create(
                        name=form.cleaned_data["workshop_name"],
                        workshop_type=form.cleaned_data["workshop_type"],
                        phone_number=form.cleaned_data["phone_number"],
                        email=form.cleaned_data["email"],
                        location=form.cleaned_data["location"],
                        address=form.cleaned_data["address"],
                        is_active=True,
                    )

                    owner = User.objects.create_user(
                        username=username,
                        email=form.cleaned_data["owner_email"],
                        password=form.cleaned_data["temporary_password"],
                        first_name=form.cleaned_data["owner_first_name"],
                        last_name=form.cleaned_data["owner_last_name"],
                    )

                    StaffProfile.objects.create(
                        user=owner,
                        workshop=workshop,
                        role="owner",
                        is_active=True,
                    )

                return redirect("platform_admin:dashboard")

    else:

        form = WorkshopOnboardingForm()

    return render(
        request,
        "platform_admin/add_workshop.html",
        {
            "form": form,
        },
    )

# =========================================================
# WORKSHOP MANAGEMENT
# =========================================================

@user_passes_test(is_platform_admin, login_url="/admin/login/")
def workshop_detail(request, workshop_id):

    workshop = Workshop.objects.get(
        id=workshop_id
    )

    staff_members = StaffProfile.objects.filter(
        workshop=workshop
    ).select_related(
        "user"
    ).order_by(
        "role",
        "user__username"
    )

    customers = Customer.objects.filter(
        workshop=workshop
    )

    vehicles = Vehicle.objects.filter(
        customer__workshop=workshop
    )

    repair_jobs = RepairJob.objects.filter(
        workshop=workshop
    )

    active_jobs = repair_jobs.exclude(
        status="collected"
    )

    completed_jobs = repair_jobs.filter(
        status="collected"
    )

    context = {
        "workshop": workshop,
        "staff_members": staff_members,

        "customer_count": customers.count(),
        "vehicle_count": vehicles.count(),

        "total_jobs": repair_jobs.count(),
        "active_jobs": active_jobs.count(),
        "completed_jobs": completed_jobs.count(),
    }

    return render(
        request,
        "platform_admin/workshop_detail.html",
        context,
    )

# =========================================================
# ACTIVATE / DEACTIVATE WORKSHOP
# =========================================================

@user_passes_test(is_platform_admin, login_url="/admin/login/")
@require_POST
def toggle_workshop_status(request, workshop_id):

    workshop = get_object_or_404(
        Workshop,
        id=workshop_id,
    )

    workshop.is_active = not workshop.is_active

    workshop.save(
        update_fields=["is_active"]
    )

    return redirect(
        "platform_admin:workshop_detail",
        workshop_id=workshop.id,
    )


# =========================================================
# ADD WORKSHOP STAFF
# =========================================================

@user_passes_test(is_platform_admin, login_url="/admin/login/")
def add_workshop_staff(request, workshop_id):

    workshop = get_object_or_404(
        Workshop,
        id=workshop_id,
    )

    if request.method == "POST":

        form = StaffAccountForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]

            if User.objects.filter(
                username__iexact=username
            ).exists():

                form.add_error(
                    "username",
                    "A user with this username already exists."
                )

            else:

                with transaction.atomic():

                    user = User.objects.create_user(
                        username=username,
                        email=form.cleaned_data["email"],
                        password=form.cleaned_data["temporary_password"],
                        first_name=form.cleaned_data["first_name"],
                        last_name=form.cleaned_data["last_name"],
                    )

                    StaffProfile.objects.create(
                        user=user,
                        workshop=workshop,
                        role=form.cleaned_data["role"],
                        is_active=True,
                    )

                return redirect(
                    "platform_admin:workshop_detail",
                    workshop_id=workshop.id,
                )

    else:

        form = StaffAccountForm()

    return render(
        request,
        "platform_admin/add_workshop_staff.html",
        {
            "form": form,
            "workshop": workshop,
        },
    )

# =========================================================
# WORKSHOP STAFF MANAGEMENT
# =========================================================

@user_passes_test(is_platform_admin, login_url="/admin/login/")
def workshop_staff_detail(request, workshop_id, staff_id):

    workshop = get_object_or_404(
        Workshop,
        id=workshop_id,
    )

    staff_member = get_object_or_404(
        StaffProfile.objects.select_related("user"),
        id=staff_id,
        workshop=workshop,
    )

    return render(
        request,
        "platform_admin/workshop_staff_detail.html",
        {
            "workshop": workshop,
            "staff_member": staff_member,
        },
    )

# =========================================================
# ACTIVATE / DEACTIVATE STAFF ACCOUNT
# =========================================================

@user_passes_test(is_platform_admin, login_url="/admin/login/")
@require_POST
def toggle_staff_status(request, workshop_id, staff_id):

    workshop = get_object_or_404(
        Workshop,
        id=workshop_id,
    )

    staff_member = get_object_or_404(
        StaffProfile,
        id=staff_id,
        workshop=workshop,
    )

    staff_member.is_active = not staff_member.is_active

    staff_member.save(
        update_fields=["is_active"]
    )

    return redirect(
        "platform_admin:workshop_staff_detail",
        workshop_id=workshop.id,
        staff_id=staff_member.id,
    )

# =========================================================
# EDIT WORKSHOP STAFF ACCOUNT
# =========================================================

@user_passes_test(is_platform_admin, login_url="/admin/login/")
def edit_workshop_staff(request, workshop_id, staff_id):

    workshop = get_object_or_404(
        Workshop,
        id=workshop_id,
    )

    staff_member = get_object_or_404(
        StaffProfile.objects.select_related("user"),
        id=staff_id,
        workshop=workshop,
    )

    user = staff_member.user

    if request.method == "POST":

        form = StaffEditForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]

            username_exists = User.objects.filter(
                username__iexact=username
            ).exclude(
                id=user.id
            ).exists()

            if username_exists:

                form.add_error(
                    "username",
                    "A user with this username already exists."
                )

            else:

                with transaction.atomic():

                    user.first_name = form.cleaned_data["first_name"]
                    user.last_name = form.cleaned_data["last_name"]
                    user.username = username
                    user.email = form.cleaned_data["email"]

                    user.save()

                    staff_member.role = form.cleaned_data["role"]

                    staff_member.save(
                        update_fields=["role"]
                    )

                return redirect(
                    "platform_admin:workshop_staff_detail",
                    workshop_id=workshop.id,
                    staff_id=staff_member.id,
                )

    else:

        form = StaffEditForm(
            initial={
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "email": user.email,
                "role": staff_member.role,
            }
        )

    return render(
        request,
        "platform_admin/edit_workshop_staff.html",
        {
            "form": form,
            "workshop": workshop,
            "staff_member": staff_member,
        },
    )

# =========================================================
# RESET WORKSHOP STAFF PASSWORD
# =========================================================

@user_passes_test(is_platform_admin, login_url="/admin/login/")
def reset_workshop_staff_password(request, workshop_id, staff_id):

    workshop = get_object_or_404(
        Workshop,
        id=workshop_id,
    )

    staff_member = get_object_or_404(
        StaffProfile.objects.select_related("user"),
        id=staff_id,
        workshop=workshop,
    )

    if request.method == "POST":

        form = StaffPasswordResetForm(request.POST)

        if form.is_valid():

            user = staff_member.user

            user.set_password(
                form.cleaned_data["new_password"]
            )

            user.save()

            return redirect(
                "platform_admin:workshop_staff_detail",
                workshop_id=workshop.id,
                staff_id=staff_member.id,
            )

    else:

        form = StaffPasswordResetForm()

    return render(
        request,
        "platform_admin/reset_workshop_staff_password.html",
        {
            "form": form,
            "workshop": workshop,
            "staff_member": staff_member,
        },
    )

# =========================================================
# PLATFORM LOGOUT
# =========================================================

@require_POST
def platform_logout(request):
    logout(request)
    return redirect("home")

