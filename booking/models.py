from django.db import models
from django.utils import timezone
from accounts.models import User, UserProfile
from technician.models import Technician

class Booking(models.Model):
    CHOICES = (
        ("ACCEPT", "Accept"),
        ("REJECT", "Reject"),
        ("COMPLETED", "Completed"),
        ("PENDING", "Pending"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE, related_name='bookings')
    email = models.EmailField(max_length=100)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=250, blank=True, null=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    booking_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=100, choices=CHOICES, default="PENDING")
    is_paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Populate email, name, and address fields dynamically
        self.email = self.user.email
        self.name = f"{self.user.first_name} {self.user.last_name}"
        if self.user.userprofile:
            self.address = self.user.userprofile.address
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} - {self.technician.user.email}"


class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    charge = models.IntegerField()
    time_stamp=models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.charge = self.booking.technician.service_charge
        super().save(*args, **kwargs)

    def __str__(self):
        return self.booking.email
    
