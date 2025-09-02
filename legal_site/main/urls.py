from django.urls import path
from . import views


urlpatterns = [
    path('', views.maintenance, name='maintenance'),
    path('working', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('policy/',views.privacy_policy, name='policy'),
    path('jobs/', views.job_list, name='job_list'),
    path('maintenance/', views.maintenance, name='maintenance'),
    path('jobs/<int:job_id>/apply/', views.apply_for_job, name='apply_for_job'),
]
