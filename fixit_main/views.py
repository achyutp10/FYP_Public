from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from accounts.models import User
from booking.models import Booking, Payment
from rating.models import Rating
from technician.models import Technician
from django.db.models import Sum
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models.functions import TruncMonth

def home(request):
  all_ratings = Rating.objects.all()[:2]
    
  context = {
        'all_ratings': all_ratings,
    }
  return render(request, 'home.html', context)

def services(request):
  all_ratings = Rating.objects.all()[:2]
    
  context = {
        'all_ratings': all_ratings,
    }
  return render(request, 'services.html', context)

from django.db.models import Count
def admin(request):
  total_technicians = Technician.objects.all().count()
  total_customers = User.objects.filter(role=User.CUSTOMER).count()
  total_bookings = Booking.objects.all().count()
  total_earnings = Payment.objects.aggregate(total=Sum('charge'))['total']
  earnings_data = Payment.objects.annotate(month=TruncMonth('time_stamp')).values('month').annotate(total_earnings=Sum('charge'))
  bookings_by_month = Booking.objects.annotate(month=TruncMonth('booking_date')).values('month').annotate(count=Count('id'))

    # Prepare data for chart
  booking_data = [{'month': b['month'].strftime('%B %Y'), 'count': b['count']} for b in bookings_by_month]

  
  context = {
    'total_technicians': total_technicians,
    'total_customers': total_customers,
    'total_bookings': total_bookings,
    'total_earnings': total_earnings,
    'earnings_data': earnings_data,
    'booking_data': booking_data,
    
  }
  return render(request, 'admin/admin.html', context)

def adminTechnician(request):
  all_technicians = Technician.objects.all()
  paginator = Paginator(all_technicians, 5) 

  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  context = {
    'all_technicians': all_technicians,
    'page_obj': page_obj,
  }
  return render(request,  'admin/adminTechnician.html', context)

def adminCustomer(request):
  all_customer = User.objects.filter(role=User.CUSTOMER)
  paginator = Paginator(all_customer, 5) 

  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  context = {
    'all_customer': all_customer,
    'page_obj': page_obj,
  }
  return render(request,  'admin/adminCustomer.html', context)

def adminBooking(request):
  all_booking = Booking.objects.all()
  paginator = Paginator(all_booking, 5) 

  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  context = {
    'all_customer': all_booking,
    'page_obj': page_obj,
  }
  return render(request,  'admin/adminBookings.html', context)

# def assignStatus(request, technician_id):
#   technician = get_object_or_404(Technician, pk=technician_id)
#   context = {
#     'technician': technician,
#   }
#   return render(request, 'admin/assignStatus.html', context)

def assignStatus(request, technician_id):
    technician = get_object_or_404(Technician, pk=technician_id)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status == 'ACCEPT':
            technician.is_approved = True
            technician.save()
            messages.success(request, 'Technician has been approved successfully.')
        elif status == 'REJECT':
            technician.is_approved = False
            technician.save()
            messages.success(request, 'Technician has been rejected.')
        else:
            messages.error(request, 'Invalid status provided.')

        return redirect('adminTechnician')
    
    context = {'technician': technician}
    return render(request, 'admin/assignStatus.html', context)


def deleteUser(request, customer_id):
    # Get the user object or return 404 if not found
    customer = get_object_or_404(User, id=customer_id)

    if request.method == 'POST':
        # Delete the user object
        customer.delete()
        messages.success(request, 'User has been deleted successfully.')
        return redirect('adminCustomer')  # Redirect to the user list page
    else:
        context = {
            "customer": customer,
        }
        return render(request, 'admin/adminCustomer.html', context)

def deleteTechnician(request, technician_id):
    
    technician = get_object_or_404(Technician, id=technician_id)
    user = technician.user

    if request.method == 'POST':
        
        technician.delete()
        user.delete()
        messages.success(request, 'Technician has been deleted successfully.')
        return redirect('adminTechnician')  
    else:
        context = {
            "technician": technician,
        }
        return render(request, 'admin/admintechnician.html', context)

    
def deletebooking(request, booking_id):
    
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        
        booking.delete()
        messages.success(request, 'Booking has been deleted successfully.')
        return redirect('adminBooking')  
    else:
        context = {
            "booking": booking,
        }
        return render(request, 'admin/adminBookings.html', context)




