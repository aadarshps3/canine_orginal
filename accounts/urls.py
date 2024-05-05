from django.urls import path
from accounts import views

urlpatterns = [
    path('',views.index,name='index'),
    path('sign-up/',views.customer_signup,name='sign-up'),
    path('sign-in/',views.login_view,name='sign-in'),
    path('admin-home/',views.admin_home,name='admin-home'),
    path('staff-admin/', views.staff_register, name='staff-admin'),
    path('staff-view/', views.staff_view, name='staff-view'),
    path('customer-view/', views.customer_view, name='customer-view'),
    path('dog-view/', views.dog_view, name='dog-view'),
    path('feeds-view-admin/', views.feedback_view_admin, name='feeds-view-admin'),
    path('boarding-view-admin/', views.boardings_view_admin, name='boarding-view-admin'),
    path('approve-boarding/<int:pk>/', views.approve_boardings, name='approve-boarding'),
    path('list-reports-admin', views.list_reports_admin, name='list-reports-admin'),
    path('sign-out/',views.logout_view,name='sign-out'),
    path('create-room/',views.create_room,name='create-room'),
    path('room-view/',views.room_view,name='room-view'),
    path('add-bill/', views.bill, name='add-bill'),
    path('view-bill/', views.view_bill, name='view-bill'),
    path('Adoption_requests', views.Adoption_requests, name='Adoption_requests'),
    path('confirm_booking/<int:id>/', views.confirm_booking, name='confirm_booking'),
    path('reject_booking/<int:id>/', views.reject_booking, name='reject_booking'),
]