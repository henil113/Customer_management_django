# Generated by Django 3.1 on 2020-08-17 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filedata9', '0003_customer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]