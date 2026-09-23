from django.urls import path
from . import views


urlpatterns = [

    # =========================================================
    # PUBLIC HOME PAGE
    # =========================================================

    path(
        "",
        views.home,
        name="home"
    ),

    # =========================================================
    # WORKSHOP LOGIN
    # =========================================================

    path(
        "login/",
        views.staff_login,
        name="staff_login"
    ),

    # =========================================================
    # WORKSHOP DASHBOARD
    # =========================================================

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    # =========================================================
    # CUSTOMER MANAGEMENT
    # =========================================================

    path(
        "customers/register/",
        views.register_customer,
        name="register_customer"
    ),

    # =========================================================
    # VEHICLE MANAGEMENT
    # =========================================================

    path(
        "vehicles/register/",
        views.register_vehicle,
        name="register_vehicle"
    ),

    # =========================================================
    # REPAIR JOBS
    # =========================================================

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


    path(
        "reports/monthly/",
        views.monthly_report,
        name="monthly_report"
    ),
]

