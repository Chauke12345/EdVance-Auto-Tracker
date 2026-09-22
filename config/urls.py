from django.contrib import admin
from django.urls import path, include


urlpatterns = [

    # =====================================================
    # DJANGO TECHNICAL ADMIN
    # =====================================================

    path(
        "admin/",
        admin.site.urls
    ),

    # =====================================================
    # EDVANCE TECH PLATFORM ADMINISTRATION
    # =====================================================

    path(
        "platform/",
        include("platform_admin.urls")
    ),

    # =====================================================
    # WORKSHOP TENANT SYSTEM
    # =====================================================

    path(
        "",
        include("workshop.urls")
    ),

]
