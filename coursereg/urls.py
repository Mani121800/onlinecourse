
from django.contrib import admin
from django.urls import path,include
from courseapp import views
from courseapp.views import SignupPage
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', SignupPage, name='signup'),
    path('', include('courseapp.urls')),
    path('home2/',views.HomePage,name='home2'),
    path('req/',views.req_view,name='req'),

   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)