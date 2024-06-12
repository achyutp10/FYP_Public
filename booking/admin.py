from django.contrib import admin

from booking.models import Booking,Payment

# Register your models here.
class BookingAdmin(admin.ModelAdmin):
  list_display = ('user','technician','email', 'name', 'phone_number','status')
  list_display_links = ('user','technician','email')
  list_editable = ('status',)
admin.site.register(Booking, BookingAdmin)

admin.site.register(Payment)