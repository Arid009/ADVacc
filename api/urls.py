from django.urls import path, include
from vaccine.views import VaccineViewSet, ReviewViewSet, BookingViewSet,DoctorViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('vaccines', VaccineViewSet, basename='vaccines')
router.register('bookings', BookingViewSet, basename='bookings')
router.register('doctors', DoctorViewSet, basename='doctors')

vaccine_router = routers.NestedDefaultRouter(router, 'vaccines', lookup='vaccine')
vaccine_router.register('reviews', ReviewViewSet, basename='vaccine-review')



urlpatterns = [
    path('', include(router.urls)),
    path('', include(vaccine_router.urls))
    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.jwt')),
]