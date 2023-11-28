from django.contrib import admin
from .models import CrmModel
# Register your models here.


class CrmModelAdmin(admin.ModelAdmin):
    model = CrmModel
    list_display = ['company', 'contact_person', 'email', 'phone', 'web_site', 'created_by']


admin.site.register(CrmModel, CrmModelAdmin)
