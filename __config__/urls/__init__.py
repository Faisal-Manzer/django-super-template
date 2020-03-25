"""
Root url pattern for the project,
in production all url patterns will be converted to sub-domains
"""


from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    path('', include('__config__.urls.api')),
    path('admin/', include('__config__.urls.admin')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.PRODUCTION:
    urlpatterns = []
