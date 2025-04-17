from django.contrib import admin
from vaccine.models import Vaccine, Booking , Review
from users.models import DoctorProfile
# Register your models here.
admin.site.register(Vaccine)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(DoctorProfile)