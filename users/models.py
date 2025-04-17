from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import CustomUserManager
from cloudinary.models import CloudinaryField

# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    nid_num = models.IntegerField(default=0)
    image = CloudinaryField('image',blank=True,null=True)

    med_detail = models.TextField(blank=True,null=True)
    # vaccination_history = models.ManyToManyField('vaccine.Vaccine', through='vaccine.Booking', related_name='vacc_detail')

    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    hospital = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.email