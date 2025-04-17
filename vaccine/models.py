from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User

# Create your models here.

class Vaccine(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_dose_available_dates = models.DateTimeField()
    second_dose_schedule = models.IntegerField()


    class Meta:
        ordering = ['-id',]

    def __str__(self):
        return self.name

class Review(models.Model):
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ratings = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.user.first_name} on {self.vaccine.name}"

class Booking(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE, related_name='bookings')
    first_dose_date = models.DateTimeField()
    second_dose_date = models.DateTimeField(null=True, blank=True)
    booking_date = models.DateTimeField(auto_now_add=True)
    location = models.CharField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} booked {self.vaccine.name} on {self.first_dose_date.strftime('%Y-%m-%d %H:%M')}"