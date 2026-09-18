from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.staff_login,
        name="staff_login"
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "customers/register/",
        views.register_customer,
        name="register_customer"
    ),

    path(
        "vehicles/register/",
        views.register_vehicle,
        name="register_vehicle"
    ),

    path(
        "jobs/create/",
        views.create_repair_job,
        name="create_repair_job"
    ),

    path(
        "jobs/<str:tracking_number>/",
        views.repair_job_detail,
        name="repair_job_detail"
    ),

    # =========================================================
    # CUSTOMER TRACKING
    # =========================================================

    path(
        "track/",
        views.customer_tracking,
        name="customer_tracking"
    ),

    # =========================================================
    # LOGOUT
    # =========================================================

    path(
        "logout/",
        views.staff_logout,
        name="staff_logout"
    ),

]