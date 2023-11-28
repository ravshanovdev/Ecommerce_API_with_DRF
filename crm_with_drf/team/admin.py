from django.contrib import admin
from .models import Team, Plans
# Register your models here.

admin.site.register(Plans)


class TeamModelAdmin(admin.ModelAdmin):
    model = Team
    list_display = ['name', 'created_by', 'created_at']


admin.site.register(Team, TeamModelAdmin)

