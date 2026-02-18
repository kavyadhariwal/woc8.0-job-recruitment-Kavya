from django.urls import path
from . import views

urlpatterns = [
    path('manage/<int:job_id>/', views.manage_applications, name='manage_applications'),
    path('update/<int:app_id>/<str:status>/', views.update_application_status, name='update_application_status'),
    path('withdraw/<int:app_id>/', views.withdraw_application, name='withdraw_application'),
]
