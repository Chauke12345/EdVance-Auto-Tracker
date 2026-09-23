from django.urls import path
from . import views


app_name = "platform_admin"


urlpatterns = [

    # =========================================================
    # STAFF PASSWORD RESET
    # =========================================================

    path(
        "workshops/<int:workshop_id>/staff/<int:staff_id>/reset-password/",
        views.reset_workshop_staff_password,
        name="reset_workshop_staff_password",
    ),


    # =========================================================
    # STAFF EDIT
    # =========================================================

    path(
        "workshops/<int:workshop_id>/staff/<int:staff_id>/edit/",
        views.edit_workshop_staff,
        name="edit_workshop_staff",
    ),


    # =========================================================
    # STAFF STATUS
    # =========================================================

    path(
        "workshops/<int:workshop_id>/staff/<int:staff_id>/toggle-status/",
        views.toggle_staff_status,
        name="toggle_staff_status",
    ),


    # =========================================================
    # STAFF MANAGEMENT
    # =========================================================

    path(
        "workshops/<int:workshop_id>/staff/<int:staff_id>/",
        views.workshop_staff_detail,
        name="workshop_staff_detail",
    ),

    path(
        "workshops/<int:workshop_id>/staff/add/",
        views.add_workshop_staff,
        name="add_workshop_staff",
    ),


    # =========================================================
    # WORKSHOP STATUS
    # =========================================================

    path(
        "workshops/<int:workshop_id>/toggle-status/",
        views.toggle_workshop_status,
        name="toggle_workshop_status",
    ),


    # =========================================================
    # PLATFORM DASHBOARD
    # =========================================================

    path(
        "",
        views.platform_dashboard,
        name="dashboard",
    ),


    # =========================================================
    # PLATFORM LOGOUT
    # =========================================================

    path(
        "logout/",
        views.platform_logout,
        name="logout",
    ),


    # =========================================================
    # WORKSHOP ONBOARDING
    # =========================================================

    path(
        "workshops/add/",
        views.add_workshop,
        name="add_workshop",
    ),


    # =========================================================
    # WORKSHOP MANAGEMENT
    # =========================================================

    path(
        "workshops/<int:workshop_id>/",
        views.workshop_detail,
        name="workshop_detail",
    ),

]
