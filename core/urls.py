from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.DeskFlowLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('ticket/<int:ticket_id>/approve/', views.approve_ticket, name='approve_ticket'),
    path('ticket/<int:ticket_id>/reject/', views.reject_ticket, name='reject_ticket'),
]
