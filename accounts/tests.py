# from django.test import TestCase

# # Create your tests here.
# from django.test import TestCase
# from django.urls import reverse
# from django.contrib.auth import get_user_model
# from django.core import mail

# User = get_user_model()

# class RegisterUserTestCase(TestCase):
#     def test_register_user(self):
#         # Test registering a user with valid form data
#         response = self.client.post(reverse('registerUser'), {
#             'first_name': 'John',
#             'last_name': 'Doe',
#             'username': 'johndoe',
#             'email': 'johndoe@example.com',
#             'phone_number': '1234567890',
#             'password': 'password123',
#             'confirm_password': 'password123',  # Assuming you have a confirm password field in the form
#         })

#         # Check if the user is redirected to the registration page after successful registration
#         self.assertRedirects(response, reverse('registerUser'))

#         # Check if the user is created in the database
#         self.assertTrue(User.objects.filter(username='johndoe').exists())

#         # Check if an account activation email is sent
#         self.assertEqual(len(mail.outbox), 1)
#         self.assertEqual(mail.outbox[0].subject, 'Please activate your account')
#         self.assertEqual(mail.outbox[0].to, ['johndoe@example.com'])

#     def test_register_user_invalid_form(self):
#         # Test registering a user with invalid form data
#         response = self.client.post(reverse('registerUser'), {
#             'first_name': 'John',
#             'last_name': 'Doe',
#             'username': 'johndoe',
#             'email': 'invalidemail',  # Invalid email format
#             'phone_number': '1234567890',
#             'password': 'password123',
#             'confirm_password': 'password123',
#         })

#         # Check if the form is not valid and user is not created
#         self.assertEqual(response.status_code, 200)
#         self.assertFalse(User.objects.filter(username='johndoe').exists())


# from django.test import TestCase
# from .models import User, UserProfile

# class UserModelTestCase(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             email='test@example.com', username='testuser', first_name='Test',last_name='User', phone_number='1234567890', profile_picture=None,
#             password='testpassword'
#         )

#     def test_user_creation(self):
#         print("Testing user creation...")
#         self.assertEqual(User.objects.count(), 1)
#         saved_user = User.objects.get(email='test@example.com')
#         self.assertEqual(saved_user.first_name, 'Test')
#         self.assertEqual(saved_user.last_name, 'User')
#         self.assertEqual(saved_user.username, 'testuser')
#         self.assertEqual(saved_user.phone_number, '1234567890')
#         print("User creation test passed.")

# class UserProfileModelTestCase(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             email='test@example.com', username='testuser', first_name='Test', last_name='User', phone_number='1234567890', profile_picture=None,
#             password='testpassword'
#         )
#         self.user_profile = UserProfile.objects.create(
#             user=self.user, address='123 Test St', country='Country', state='State', city='City',
#             pin_code='123456', latitude='40.7128', longitude='-74.0060'
#         )

#     def test_user_profile_creation(self):
#         print("Testing user profile creation...")
#         self.assertEqual(UserProfile.objects.count(), 1)
#         saved_user_profile = UserProfile.objects.get(user=self.user)
#         self.assertEqual(saved_user_profile.address, '123 Test St')
#         self.assertEqual(saved_user_profile.country, 'Country')
#         self.assertEqual(saved_user_profile.state, 'State')
#         self.assertEqual(saved_user_profile.city, 'City')
#         self.assertEqual(saved_user_profile.pin_code, '123456')
#         self.assertEqual(saved_user_profile.latitude, '40.7128')
#         self.assertEqual(saved_user_profile.longitude, '-74.0060')
#         print("User profile creation test passed.")





