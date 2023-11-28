from django.db import models
from django.contrib.auth.models import User
from team.models import Team
# Create your models here.


class CrmModel(models.Model):
    NEW = 'new'
    CONTACTED = 'contacted'
    INPROGRESS = 'inprogress'
    LOST = 'lost'
    WON = 'won'

    CHOICES_STATUS = (
        (NEW, 'New'),
        (CONTACTED, 'Contacted'),
        (INPROGRESS, 'InProgress'),
        (LOST, 'Lost'),
        (WON, 'Won')
    )

    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

    CHOICES_PRIORITY = (
        (LOW, 'low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High')
    )
    team = models.ForeignKey(Team, related_name='crm', on_delete=models.CASCADE)
    company = models.CharField(max_length=150)
    contact_person = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    web_site = models.CharField(max_length=150)
    confidence = models.CharField(max_length=150)
    estimated_value = models.CharField(max_length=150)
    status = models.CharField(max_length=25, choices=CHOICES_STATUS, default=NEW)
    priority = models.CharField(max_length=25, choices=CHOICES_PRIORITY, default=MEDIUM)
    assigned_to = models.ForeignKey(User, related_name='assignedCrmModel', on_delete=models.SET_NULL, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='crm_models', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)







