from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from vaccine.models import Vaccine, Review, Booking
from users.models import DoctorProfile
from vaccine.serializers import VaccineSerializer, BookingSerializer, ReviewSerializer, DoctorSerializer
from vaccine.filters import VaccineFilter
from vaccine.permissions import IsReviewAuthorOrReadonly, IsDoctorOrAdmin
from vaccine.paginations import DefaultPagination 
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from api.permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your views here.


class VaccineViewSet(ModelViewSet):
    queryset = Vaccine.objects.all()
    serializer_class = VaccineSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = VaccineFilter
    pagination_class = DefaultPagination
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'updated_at']
    permission_classes = [IsAdminOrReadOnly]
    

class VaccineList(ListCreateAPIView):
    queryset = Vaccine.objects.all()
    serializer_class = VaccineSerializer

class ViewSpecificVaccine(APIView):
    def get(self, request, id):
        Vaccine = get_object_or_404(Vaccine, pk=id)
        serializer = VaccineSerializer(Vaccine)
        return Response(serializer.data)

    def put(self, request, id):
        Vaccine = get_object_or_404(Vaccine, pk=id)
        serializer = VaccineSerializer(Vaccine, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, id):
        Vaccine = get_object_or_404(Vaccine, pk=id)
        copy_of_Vaccine = Vaccine
        Vaccine.delete()
        serializer = VaccineSerializer(copy_of_Vaccine)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadonly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Review.objects.none()
        return Review.objects.select_related('user').filter(vaccine_id=self.kwargs.get('vaccine_pk'))

    def get_serializer_context(self):
        if getattr(self, 'swagger_fake_view', False):
            return super().get_serializer_context()
        return {'vaccine_id': self.kwargs.get('vaccine_pk')}

class DoctorViewSet(ModelViewSet):
    serializer_class = DoctorSerializer
    permission_classes = [IsDoctorOrAdmin]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return DoctorProfile.objects.none()
        if self.request.user.groups.filter(name='Doctor').exists():
            return DoctorProfile.objects.select_related('user').filter(user=self.request.user)
        elif self.request.user.is_staff:
            return DoctorProfile.objects.select_related('user').all()
        return DoctorProfile.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

class BookingViewSet(ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Booking.objects.none()
        if self.request.user.is_staff:
            return Booking.objects.select_related('vaccine').all()
        return Booking.objects.select_related('vaccine').filter(user=self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        if instance.first_dose_date and instance.vaccine:
            print('asdf ine k', instance.vaccine.second_dose_schedule)
            instance.second_dose_date = instance.first_dose_date + timezone.timedelta(days=instance.vaccine.second_dose_schedule)
            instance.save()