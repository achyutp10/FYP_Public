from django.db import models
from accounts.models import User
from technician.models import Technician
from booking.models import Booking

class Rating(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
  technician = models.ForeignKey(Technician, on_delete=models.CASCADE, related_name='ratings')
  booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='ratings')
  rating = models.IntegerField(default=0)
  feedbacks = models.TextField(null=True, blank=True)

  def __str__(self):
    return f'Rating for {self.technician.user.first_name} by {self.user.first_name}'

