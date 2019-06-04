from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^comment/', include(('comment.urls', 'comment'), namespace='comment')),
    url(r'^blog/',include(('blog.urls','blog'),namespace='blog')),
    url(r'^', include(('blooger.urls', 'blooger'), namespace='blooger')),
    url(r'mdeditor/', include('mdeditor.urls')),
]
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)