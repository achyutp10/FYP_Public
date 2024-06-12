# from django.test import TestCase
# from django.utils import timezone
# from accounts.models import User, UserProfile

# class BookingModelTestCase(TestCase):
#     def setUp(self):
#         self.user = User.objects.create(email='user@example.com', username='testuser', first_name='Test',
#             last_name='User', phone_number='1234567890', password='testpassword'
#         )
#         self.user_profile = UserProfile.objects.create( user=self.user, address='123 Test St', country='Country',state='State',
#             city='City', pin_code='123456', latitude='40.7128', longitude='-74.0060'
#         )
#         self.technician = Technician.objects.create(user=self.user, user_profile=self.user_profile, technician_description='Test description',
#             service_type='PLUMBER', service_description='Test service description', service_charge=100, is_approved=True, is_available_status=True,
#             is_booked_status=False
#         )

#     def test_booking_creation(self):
#         print("Creating booking...")
#         booking = Booking.objects.create(user=self.user, technician=self.technician, booking_date=timezone.now(), status='PENDING', is_paid=False)
#         print("Booking created successfully.")
#         self.assertEqual(Booking.objects.count(), 1)
#         saved_booking = Booking.objects.get(id=booking.id)
#         print("Retrieved saved booking:")
#         print(saved_booking)
#         self.assertEqual(saved_booking.email, 'user@example.com')
#         print("Email assertion successful.")
#         self.assertEqual(saved_booking.name, 'Test User')
#         print("Name assertion successful.")
#         self.assertEqual(saved_booking.address, '123 Test St')
#         print("Address assertion successful.")
#         self.assertEqual(saved_booking.status, 'PENDING')
#         print("Status assertion successful.")
#         self.assertFalse(saved_booking.is_paid)
#         print("is_paid assertion successful.")

# from django.test import TestCase
# from django.utils import timezone
# from .models import Payment
# from accounts.models import User, UserProfile
# from technician.models import Technician
# from .models import Booking

# class PaymentModelTestCase(TestCase):
#     def setUp(self):
#         self.user = User.objects.create(email='user@example.com', username='testuser', first_name='Test', last_name='User', phone_number='1234567890', password='testpassword')
#         self.user_profile = UserProfile.objects.create(user=self.user, address='123 Test St', country='Country', state='State', city='City', pin_code='123456', latitude='40.7128',
#             longitude='-74.0060'
#         )
#         self.technician = Technician.objects.create(user=self.user, user_profile=self.user_profile, technician_description='Test description', service_type='PLUMBER', 
#             service_description='Test service description', service_charge=100, is_approved=True, is_available_status=True, is_booked_status=False
#         )
#         self.booking = Booking.objects.create(user=self.user, technician=self.technician, booking_date=timezone.now(), status='PENDING', is_paid=False)

#     def test_payment_creation(self):
#         print("Creating payment...")
#         payment = Payment.objects.create( booking=self.booking, time_stamp=timezone.now()
#         )
#         print("Payment created successfully.")
#         self.assertEqual(Payment.objects.count(), 1)
#         saved_payment = Payment.objects.get(id=payment.id)
#         print("Retrieved saved payment:")
#         print(saved_payment)
#         self.assertEqual(saved_payment.booking.email, 'user@example.com')
#         print("Booking email assertion successful.")
#         self.assertEqual(saved_payment.charge, 100)
#         print("Charge assertion successful.")
