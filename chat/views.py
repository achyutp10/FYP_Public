# from django.shortcuts import render
# from booking.models import Booking
# from technician.models import Technician
# from accounts.models import User

# from django.shortcuts import render
# from booking.models import Booking

# def messages_page(request):
#     user = request.user
#     bookings = Booking.objects.filter(user=user)
#     technician = request.user
#     bookings = Booking.objects.filter(user=technician)

#     # Get unique technicians from bookings
#     unique_technician_ids = bookings.values_list('technician__id', flat=True).distinct()
#     unique_technicians = Technician.objects.filter(id__in=unique_technician_ids)
#     unique_customer_ids = bookings.values_list('user__id', flat=True).distinct()
#     unique_customers = User.objects.filter(id__in=unique_customer_ids)

#     context = {
#         'technicians': unique_technicians,
#         'customers': unique_customers,
#     }

#     return render(request, 'chat/messages.html', context)



from django.shortcuts import render
from booking.models import Booking
from technician.models import Technician
from accounts.models import User
from django.contrib.auth.decorators import login_required
from chat.models import Thread
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q

@login_required
def messages_page(request):
    user = request.user
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    # Check if the user is authenticated
    if user.is_authenticated:
        # Check if the user is a technician
        try:
            technician = Technician.objects.get(user=user)
            bookings = Booking.objects.filter(technician=technician)
            # Get unique customers from technician bookings
            unique_customer_ids = bookings.values_list('user__id', flat=True).distinct()
            unique_customers = User.objects.filter(id__in=unique_customer_ids)
            context = {
                'customers': unique_customers,
                'Threads': threads,
            }
        except Technician.DoesNotExist:
            # If user is not a technician, filter bookings for the customer
            bookings = Booking.objects.filter(user=user)
            # Get unique technicians from customer bookings
            unique_technician_ids = bookings.values_list('technician__id', flat=True).distinct()
            unique_technicians = Technician.objects.filter(id__in=unique_technician_ids)
            context = {
                'technicians': unique_technicians,
                'Threads': threads,
            }
    else:
        # If the user is not authenticated, set context variables to None
        context = {
            'technicians': None,
            'customers': None,
        }

    return render(request, 'chat/messages.html', context)



@receiver(post_save, sender=Booking)
def create_thread_for_booking(sender, instance, created, **kwargs):
    if created:
        # Check if a Thread already exists for the given pair of users
        existing_thread = Thread.objects.filter(
            Q(first_person=instance.user, second_person=instance.technician.user) |
            Q(first_person=instance.technician.user, second_person=instance.user)
        ).first()
        if not existing_thread:
            # If no Thread exists, create a new one
            Thread.objects.create(first_person=instance.user, second_person=instance.technician.user)

