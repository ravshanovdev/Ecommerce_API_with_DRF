from django.db import models
from django.contrib.auth.models import User
from team.models import Team
# Create your models here.


class Client(models.Model):
    team = models.ForeignKey(Team, related_name='clients', on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    contact_person = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    web_site = models.CharField(max_length=150)
    created_by = models.ForeignKey(User, related_name='clients', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Note(models.Model):
    team = models.ForeignKey(Team, related_name='notes', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='notes', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='notes', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Client Name: {self.client}, Note Name: {self.name}"





