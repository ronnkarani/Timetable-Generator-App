
from django.contrib import admin
from django.urls import path, include   
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views 
from timetables import views as timetable_views 
from timetables.views import root_redirect  # ✅ import redirect view
from django.shortcuts import redirect


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root_redirect, name='root'),

    # Include your other apps
    path('timetables/', include('timetables.urls')),
    path('accounts/', include('accounts.urls')),

]
