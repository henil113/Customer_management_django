# Generated by Django 3.1 on 2020-08-11 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('filedata9', '0003_auto_20200810_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='filedata9.customer'),
        ),
        migrations.AddField(
            model_name='orders',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='filedata9.products'),
        ),
    ]
