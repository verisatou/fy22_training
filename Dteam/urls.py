from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('feedback/', include('feedback.urls')),
    path('memo/', include('memo.urls')),
    path('login/', include('django.contrib.auth.urls')),
]
