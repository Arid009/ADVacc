from rest_framework import serializers
from vaccine.models import Vaccine, Review, Booking
from users.models import DoctorProfile
from django.contrib.auth import get_user_model



class VaccineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vaccine
        fields = ['id', 'name', 'description', 'first_dose_available_dates','second_dose_schedule', 'price', 'stock']

class SimpleUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(method_name='get_current_user_name')

    class Meta:
        model = get_user_model()
        fields = ['id', 'name']

    def get_current_user_name(self, obj):
        return obj.get_full_name()

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name='get_user')

    class Meta:
        model = Review
        fields = ['id', 'user', 'vaccine','ratings', 'comment']
        read_only_fields = ['user', 'vaccine']

    def get_user(self, obj):
        return SimpleUserSerializer(obj.user).data

    def create(self, validated_data):
        vaccine_id = self.context['vaccine_id']
        return Review.objects.create(vaccine_id=vaccine_id, **validated_data)

class DoctorSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name='get_user')

    class Meta:
        model = DoctorProfile
        fields = ['user', 'specialization','hospital']
        read_only_fields = ['user']

    def get_user(self, obj):
        return SimpleUserSerializer(obj.user).data

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name='get_user')

    class Meta:
        model = Booking
        fields = ['id','user','vaccine', 'first_dose_date', 'second_dose_date', 'booking_date','location']
        read_only_fields = ['id','user', 'second_dose_date', 'booking_date']

    def get_user(self, obj):
        return SimpleUserSerializer(obj.user).data
