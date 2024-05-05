from django.urls import path
from staff_app import views

urlpatterns = [
    path('staff_home/',views.staff_home,name='staff_home'),
    path('profile-view/',views.profile_view,name='profile-view'),
    path('dogs-view-staff/',views.dog_view_staff,name='dogs-view-staff'),
    path('profile-update/',views.update_profile,name='profile-update'),
    path('boarding-assigned/',views.boarding_assigned,name='boarding-assigned'),
    path('boarding-assigned-update/<int:pk>/',views.boarding_assigned_update,name='boarding-assigned-update'),
    path('feeds-view-staff/', views.feedback_view_staff, name='feeds-view-staff'),
    path('report-add/', views.report_add, name='report-add'),
    path('list-reports/', views.list_reports, name='list-reports'),
]