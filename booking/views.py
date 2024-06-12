from datetime import date
from django.utils import timezone
from django.shortcuts import render,redirect
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Exists, OuterRef
from accounts.models import User
from rating.models import Rating
from .forms import BookingForm 
from technician.models import Technician
from booking.models import Booking, Payment
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_technician, check_role_customer
from django.urls import reverse
from .utils import send_notification_to_technician, send_notification_to_user
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
# Create your views here.
def bookTechnician(request):
    technicians = Technician.objects.all()  # Queryset for all technicians
    paginator = Paginator(technicians, 3) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # already_booked = any(technician.is_booked_status for technician in technicians)
    context = {
        'page_obj': page_obj, 
        # 'already_booked': already_booked, 
    }
    return render(request, 'booking/bookTechnician.html', context)



# def bookNow(request, technician_id):
#     user_profile = request.user.userprofile
#     technician = get_object_or_404(Technician, id=technician_id)
#     today_date = date.today().strftime('%Y-%m-%d')
#     current_time = timezone.now().strftime('%H:%M')
#     context = {
#         'technician': technician,
#         'user_profile': user_profile,
#         'today_date': today_date,
#         'current_time': current_time,
#     }
#     return render(request, 'booking/bookNow.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def bookNow(request, technician_id):
    user_profile = request.user.userprofile
    technician = get_object_or_404(Technician, id=technician_id)
    today_date = date.today().strftime('%Y-%m-%d')
    current_time = timezone.now().strftime('%H:%M')

      # Assign values to context dictionary
    context = {
        'user': request.user,
    }

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.technician = technician
            booking.save()

            mail_subject = 'You have been requested for booking'
            mail_template = 'accounts/emails/booking_request_email.html'

            send_notification_to_technician(technician.user.email, mail_subject, mail_template, technician.user)

            messages.success(request, 'Congratulations booking request has been sent with email notification')
            return redirect(reverse('bookNow', kwargs={'technician_id': technician_id}))

    else:
        # Filling the form with initial data
        initial_data = {
            'email': request.user.email,
            'name': f"{request.user.first_name} {request.user.last_name}",
            'address': request.user.userprofile.address,
            'phone_number': request.user.phone_number,
            'booking_date': today_date,  # Assuming today's date as default
            'booking_time': current_time  # Assuming current time as default
        }
        form = BookingForm(initial=initial_data)

    # Assign values to context dictionary
    context = {
        'form': form,
        'technician': technician,
        'user_profile': user_profile,
        'today_date': today_date,
        'current_time': current_time,
    }
    return render(request, 'booking/bookNow.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_technician)
def changeStatus(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    context = {
        'booking': booking,
    }
    
    return render(request, 'booking/change_status.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_technician)
def giveStatus(request, booking_id):
    if request.method == 'POST':
        new_status = request.POST.get('status')
        booking = get_object_or_404(Booking, pk=booking_id)
        old_status = booking.status
        booking.status = new_status
        booking.save()

        # Send notification based on the new status
        if new_status == 'ACCEPT':
            mail_subject = 'Booking Accepted'
            mail_template = 'accounts/emails/accepted_notification_email.html'
            booking.technician.is_booked_status = True
            booking.technician.save()
        elif new_status == 'REJECT':
            mail_subject = 'Booking Rejected'
            mail_template = 'accounts/emails/rejected_notification_email.html'
        elif new_status == 'COMPLETED':
            mail_subject = 'Booking Completed'
            mail_template = 'accounts/emails/completed_notification_email.html'
            booking.technician.is_booked_status = False
            booking.technician.save()
        elif new_status == 'PENDING':
            mail_subject = 'Booking Pending'
            mail_template = 'accounts/emails/pending_notification_email.html'

        # Send email notification to technician
        send_notification_to_user(booking.email, mail_subject, mail_template, booking.user)

        # Send success message to the user
        messages.success(request, f'Booking status changed to {new_status}')

        return redirect('technicianBookingList')
    context = {
        'booking': booking,
    }
    
    return render(request, 'booking/change_status.html', context)

@login_required(login_url='login')
def customerBookingList(request):
    # Get the current logged-in customer
    customer = request.user
  
    bookings = Booking.objects.filter(user=customer)
    ratings = Rating.objects.filter(user=customer)
    paginator = Paginator(bookings, 3) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
        
    context = {
        'bookings': bookings,
        'ratings': ratings,
        'page_obj': page_obj,
    }
    return render(request, 'customer/customerBookingList.html', context)


# @login_required(login_url='login')
# @user_passes_test(check_role_customer)
def checkout(request, booking_id):
    bookings = get_object_or_404(Booking, pk=booking_id)
    context = {
        'bookings': bookings
    }
    return render(request, 'booking/checkout.html', context)


stripe.api_key=''

# @login_required(login_url='login')
# @user_passes_test(check_role_customer)
def checkout_session(request,booking_id):
	booking=Booking.objects.get(pk=booking_id)
	session=stripe.checkout.Session.create(
		payment_method_types=['card'],
		line_items=[{
	      'price_data': {
	        'currency': 'npr',
	        'product_data': {
	          'name': booking.name,
	        },
	        'unit_amount': booking.technician.service_charge*100,
	      },
	      'quantity': 1,
	    }],
	    mode='payment',

	    success_url = f'http://127.0.0.1:8000/accounts/booking/pay_success?session_id={{CHECKOUT_SESSION_ID}}',

	    cancel_url='http://127.0.0.1:8000/accounts/booking/pay_cancel',
	    # success_url='http://127.0.0.1:8000/accounts/booking/customerBookingList',
	    # cancel_url='http://127.0.0.1:8000/accounts/booking/customerBookingList',
	    client_reference_id=booking_id
	)
	return redirect(session.url, code=303)



# @login_required(login_url='login')
# @user_passes_test(check_role_customer)
# def pay_success(request):
#     session = stripe.checkout.Session.retrieve(request.GET['session_id'])
#     booking_id = session.client_reference_id
#     booking = Booking.objects.get(pk=booking_id)
#     user = request.user
    
#     Payment.objects.create(
#         booking=booking,
#         charge=booking.technician.service_charge,

#     )
#     booking.is_paid = True
#     booking.save(update_fields=["is_paid"])
#     messages.success(request, 'Payment successfull')
#     return render(request, 'booking/success.html')
    # return redirect(request, 'customer/customerBookingList.html')


def pay_success(request):
    session_id = request.GET.get('session_id')
    if session_id:
        session = stripe.checkout.Session.retrieve(session_id)
        booking_id = session.client_reference_id
        booking = Booking.objects.get(pk=booking_id)
        Payment.objects.create(
            booking=booking,
            charge=booking.technician.service_charge,
        )
        booking.is_paid = True
        booking.save(update_fields=["is_paid"])
        messages.success(request, 'Payment successful')
        
        user = booking.user
        if user.is_authenticated:

            return redirect('customerBookingList')
        else:
            login(request, user)
            return redirect('customerBookingList')
    else:
        return redirect('cancel')

def pay_cancel(request):
	return render(request, 'booking/cancel.html')


def search(request):
    if not 'address' in request.GET:
        return redirect('bookTechnician')
    else:

        address = request.GET['address']
        latitude = request.GET['lat']
        longitude = request.GET['lng']
        radius = request.GET['radius']
        s_type = request.GET['s_type']

        page_obj = Technician.objects.filter(service_type__icontains=s_type, is_approved=True, user__is_active=True)
        if latitude and longitude and radius:
            pnt = GEOSGeometry('POINT(%s %s)' %  (longitude, latitude), 4326)
            
            page_obj = Technician.objects.filter(service_type__icontains=s_type, is_approved=True, user__is_active=True, user_profile__location__distance_lte=(pnt, D(km=radius))).annotate(distance=Distance("user_profile__location",pnt)).order_by("distance")

            for dist in page_obj:
                dist.kms = round(dist.distance.km)
        context = {
            'page_obj': page_obj,
            'address': address,
        }

        return render(request, 'booking/bookTechnician.html',context)
    

    


