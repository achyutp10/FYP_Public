# from django.test import TestCase
# from accounts.models import User, UserProfile
# from technician.models import Technician
# from booking.models import Booking
# from .models import Rating
# from django.utils import timezone

# class RatingModelTestCase(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user( email='user@example.com', username='testuser', first_name='Test', last_name='User', phone_number='1234567890',
#             password='testpassword', profile_picture=None,
#         )
#         self.user_profile = UserProfile.objects.create(user=self.user, address='123 Test St', country='Country', state='State', city='City', pin_code='123456',
#             latitude='40.7128', longitude='-74.0060'
#         )
#         self.technician = Technician.objects.create(user=self.user, technician_description='Test description', service_type='PLUMBER', service_description='Test service description',
#             service_charge=100, is_approved=True, is_available_status=True, is_booked_status=False, user_profile=self.user_profile)
#         self.booking = Booking.objects.create(user=self.user, technician=self.technician, booking_date=timezone.now(), status='PENDING', is_paid=False
#         )

#     def test_rating_creation(self):
#         print("Creating a rating...")
#         rating = Rating.objects.create(user=self.user, technician=self.technician, booking=self.booking, rating=4, feedbacks="Good service provided."
#         )
#         print("Rating created.")
        
#         print("Asserting count of ratings...")
#         self.assertEqual(Rating.objects.count(), 1)
#         print("Count assertion passed.")
        
#         print("Retrieving saved rating...")
#         saved_rating = Rating.objects.get(id=rating.id)
#         print("Saved rating retrieved.")
        
#         print("Asserting rating and feedbacks...")
#         self.assertEqual(saved_rating.rating, 4)
#         self.assertEqual(saved_rating.feedbacks, "Good service provided.")
#         print("Rating and feedback assertions passed.")
