from django.urls import path
from . import views, admin_views, auth_views

urlpatterns = [
    # API URLs (must come first to avoid conflicts)
    path('api/kursus/', views.get_kursus_list, name='kursus-list'),
    path('api/kursus/create/', views.create_kursus, name='kursus-create'),
    path('api/kursus/<int:kursus_id>/', views.get_kursus_detail, name='kursus-detail'),
    path('api/kursus/<int:kursus_id>/update/', views.update_kursus, name='kursus-update'),
    path('api/kursus/<int:kursus_id>/delete/', views.delete_kursus, name='kursus-delete'),
    
    # Profile API URLs
    path('api/profile/', views.UserProfileDetailView.as_view(), name='profile-detail'),
    path('api/profile/update/', views.update_profile, name='profile-update'),
    path('api/user-info/', views.get_user_info, name='user-info'),
    path('api/user/update/', views.update_user_info, name='user-update'),
    path('api/profile/profile-page-data/', views.profile_page_data, name='profile-page-data'),
    
    # Authentication URLs
    path('login/', auth_views.login_view, name='login'),
    path('register/', auth_views.register_view, name='register'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('admin-info/', auth_views.admin_info_view, name='admin-info'),
    
    # Profile Pages
    path('profile/profile-page/', views.profile_page, name='profile-page'),
    
    # Admin export URLs
    path('export/', admin_views.admin_export_page, name='admin-export'),
    path('export/excel/', admin_views.export_excel, name='export-excel'),
    path('export/user-summary/', admin_views.export_user_summary_excel, name='export-user-summary'),
    path('export/zip/', admin_views.export_zip, name='export-zip'),
    
    # Home URL (must come last)
    path('', auth_views.home_view, name='home'),
]
