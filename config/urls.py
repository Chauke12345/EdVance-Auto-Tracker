from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve


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
    # PRODUCTION MEDIA FILES
    # =====================================================
    # Railway stores uploaded files in the persistent
    # /media volume configured through MEDIA_ROOT.
    # =====================================================

    path(
        "media/<path:path>",
        serve,
        {"document_root": settings.MEDIA_ROOT},
    ),

    # =====================================================
    # WORKSHOP TENANT SYSTEM
    # =====================================================

    path(
        "",
        include("workshop.urls")
    ),

]


# =========================================================
# LOCAL DEVELOPMENT MEDIA
# =====================================================

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )