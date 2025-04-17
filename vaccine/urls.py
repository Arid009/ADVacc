from django.urls import path
from vaccine import views

urlpatterns = [
    path('', views.VaccineList.as_view(), name='vaccine-list'),
    path('<int:id>/', views.ViewSpecificVaccine.as_view(), name='vaccine-list'),
]