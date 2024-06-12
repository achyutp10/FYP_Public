from django.contrib import admin

from technician.models import Technician

# Register your models here.
class TechnicianAdmin(admin.ModelAdmin):
  list_display = ('user','service_type', 'is_approved', 'created_at')
  list_display_links = ('user','service_type')
  list_editable = ('is_approved',)
admin.site.register(Technician, TechnicianAdmin)