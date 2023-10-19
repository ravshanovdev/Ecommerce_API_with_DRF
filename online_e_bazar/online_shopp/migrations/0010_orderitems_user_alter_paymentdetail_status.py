# Generated by Django 4.2.4 on 2023-08-22 11:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('online_shopp', '0009_alter_paymentdetail_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitems',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='paymentdetail',
            name='status',
            field=models.CharField(choices=[('1', 'No Paid'), ('2', 'Paid')], max_length=255),
        ),
    ]