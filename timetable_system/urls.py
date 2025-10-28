
from django.contrib import admin
from django.urls import path, include   
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views 
from timetables import views as timetable_views  # import dashboard
from django.shortcuts import redirect
# Root redirect view
def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # logged-in users go to dashboard
    return redirect('login')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root_redirect, name='root'),

    
    # Dashboard
    path('dashboard/', timetable_views.dashboard, name='dashboard'),

    # Logout
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),


    # Include your other apps
    path('timetables/', include('timetables.urls')),
    path('accounts/', include('accounts.urls')),

]
