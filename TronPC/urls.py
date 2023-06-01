from django.contrib import admin
from django.urls import re_path,include
from TronPC import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    re_path(r'^admin', admin.site.urls),
    re_path(r'^$', views.main, name='main'),
    re_path(r'^App/', include('App.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
