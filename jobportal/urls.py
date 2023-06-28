from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from users.views import custom_permission_denied_view

handler403 = custom_permission_denied_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("users.urls")),
    path('accounts/', include("allauth.urls")),
    path('', include("jobseeker.urls")),
    path('', include("jobs.urls")),
    path('', include("employer.urls")),
    path('', include("resumes.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
