from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication
    path('', views.dashboard, name='home'),  # Root URL redirects to appropriate dashboard
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Password Reset URLs for new employees
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='main/password_reset_confirm.html',
             success_url='/login/?password_set=true'
         ),
         name='password_reset_confirm'),
    
    # Dashboard routing
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Technicien URLs
    path('technicien/', views.technicien_dashboard, name='technicien_dashboard'),
    
    # Médecin URLs
    path('medecin/', views.medecin_dashboard, name='medecin_dashboard'),
    path('report/<int:report_id>/', views.report_detail, name='report_detail'),
    path('patient/<int:patient_id>/history/', views.report_history, name='report_history'),
    
    # Admin URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-employee/', views.add_employee, name='add_employee'),
    path('archive-user/<int:user_id>/', views.archive_user, name='archive_user'),
    path('reactivate-user/<int:user_id>/', views.reactivate_user, name='reactivate_user'),
    path('reset-password/<int:user_id>/', views.reset_password, name='reset_password'),
]
