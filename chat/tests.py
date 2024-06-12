# from django.test import TestCase
# from django.utils import timezone
# from accounts.models import User
# from .models import Thread, ChatMessage

# class ThreadModelTestCase(TestCase):
#     def setUp(self):
#         # Create users
#         self.user1 = User.objects.create_user(
#             email='user@example.com', username='testuser',
#             first_name='Test', last_name='User', phone_number='1234567890',
#             password='testpassword', profile_picture=None,
#         )
#         self.user2 = User.objects.create_user(
#             email='user2@example.com', username='testuser2',
#             first_name='Test2', last_name='User2', phone_number='1234567890',
#             password='testpassword', profile_picture=None,
#         )
#         self.thread = Thread.objects.create(first_person=self.user1, second_person=self.user2)

#     def test_thread_manager(self):
#         user1_threads = Thread.objects.by_user(user=self.user1)
#         user2_threads = Thread.objects.by_user(user=self.user2)

#         self.assertEqual(user1_threads.count(), 1)
#         self.assertEqual(user2_threads.count(), 1)

#     def test_chat_message_creation(self):
#         message_text = "Hello, how are you?"
#         chat_message = ChatMessage.objects.create(thread=self.thread, user=self.user1, message=message_text)
#         self.assertEqual(ChatMessage.objects.count(), 1)
#         saved_chat_message = ChatMessage.objects.first()
#         self.assertEqual(saved_chat_message.thread, self.thread)
#         self.assertEqual(saved_chat_message.user, self.user1)
#         self.assertEqual(saved_chat_message.message, message_text)
#         print(f"Message Sent by {self.user1.username}: '{message_text}'")
#         print(f"Message Received by {self.user2.username}: '{message_text}'")

#         received_message_text = "I'm good, thank you!"
#         received_chat_message = ChatMessage.objects.create(thread=self.thread, user=self.user2, message=received_message_text)

#         self.assertEqual(ChatMessage.objects.count(), 2)
#         saved_received_chat_message = ChatMessage.objects.last()
#         self.assertEqual(saved_received_chat_message.thread, self.thread)
#         self.assertEqual(saved_received_chat_message.user, self.user2)
#         self.assertEqual(saved_received_chat_message.message, received_message_text)
#         print(f"Message Sent by {self.user2.username}: '{received_message_text}'")
#         print(f"Message Received by {self.user1.username}: '{received_message_text}'")
