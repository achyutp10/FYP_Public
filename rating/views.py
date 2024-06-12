from django.shortcuts import get_object_or_404, render, redirect
from booking.models import Booking
from technician.models import Technician
from django.contrib import messages
from .models import Rating


# Create your views here.
# def giveRating(request, technician_id):
#   technician = get_object_or_404(Technician, pk=technician_id)
#   context = {
#         'technician': technician
#     }
#   return render(request, 'rating/giveRating.html', context)

# def giveRating(request, technician_id):
#     if request.method == 'POST':
#         rating_value = request.POST.get('rating')
#         feedbacks = request.POST.get('feedbacks')
#         technician = get_object_or_404(Technician, pk=technician_id)
#         user = request.user
#         rating = Rating.objects.create(
#             technician=technician,
#             user=user,
#             rating=rating_value,
#             feedbacks=feedbacks
#         )
#         rating.save()
#         messages.success(request, 'Thank you for your rating and feedback!')
#         return redirect('customerBookingList')
#     else:
#         technician = get_object_or_404(Technician, pk=technician_id)
#         context = {'technician': technician}
#         return render(request, 'rating/giveRating.html', context)

def giveRating(request, technician_id, booking_id):
    if request.method == 'POST':
        rating_value = request.POST.get('rating')
        feedbacks = request.POST.get('feedbacks')
        technician = get_object_or_404(Technician, pk=technician_id)
        user = request.user
        booking = get_object_or_404(Booking, pk=booking_id)  # Retrieve the booking
        rating = Rating.objects.create(
            technician=technician,
            user=user,
            booking=booking,  # Associate the rating with the booking
            rating=rating_value,
            feedbacks=feedbacks
        )
        rating.save()
        messages.success(request, 'Thank you for your rating and feedback!')
        return redirect('customerBookingList')
    else:
        technician = get_object_or_404(Technician, pk=technician_id)
        booking = get_object_or_404(Booking, pk=booking_id)
        context = {
            'technician': technician,
            'booking': booking,
            }
        return render(request, 'rating/giveRating.html', context)

