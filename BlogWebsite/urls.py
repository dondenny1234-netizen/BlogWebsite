from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
import os
from django.core.files.storage import default_storage
from portfolio import views


def debug_cloudinary(request):
    return JsonResponse({
        'cloud_name': os.environ.get('CLOUDINARY_CLOUD_NAME'),
        'api_key': os.environ.get('CLOUDINARY_API_KEY'),
        'has_secret': bool(os.environ.get('CLOUDINARY_API_SECRET')),
        'default_storage': str(default_storage.__class__),
    })
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portfolio.urls')),
    path('debug/', debug_cloudinary),
    path("fix-media/", views.fix_media),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
