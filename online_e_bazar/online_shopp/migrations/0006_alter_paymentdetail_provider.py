# Generated by Django 4.2.4 on 2023-08-22 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_shopp', '0005_alter_product_discount_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentdetail',
            name='provider',
            field=models.CharField(choices=[('humo', 'HUMO'), ('uzcard', 'UzCard'), ('visa', 'VISA'), ('mastercard', 'MasterCard')], max_length=255),
        ),
    ]