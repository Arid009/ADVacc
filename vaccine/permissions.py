from rest_framework import permissions
from vaccine.models import Booking
from vaccine.models import Vaccine

class IsReviewAuthorOrReadonly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'POST':
            user = request.user
            vaccine_id = view.kwargs.get('vaccine_pk')
            if user and user.is_authenticated and vaccine_id:
                try:
                    vaccine = Vaccine.objects.get(pk=vaccine_id)
                    return Booking.objects.filter(user=user, vaccine=vaccine).exists()
                except Vaccine.DoesNotExist:
                    return False
            return False

        return request.user and request.user.is_authenticated



    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_staff:
            return True

        return obj.user == request.user

class IsDoctorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or request.user.groups.filter(name='Doctor').exists()
        )

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.user == request.user
