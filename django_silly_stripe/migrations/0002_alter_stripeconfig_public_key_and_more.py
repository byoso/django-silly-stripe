# Generated by Django 4.2 on 2023-07-12 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_silly_stripe', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stripeconfig',
            name='public_key',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='stripeconfig',
            name='secret_key',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='stripeconfig',
            name='webhook_secret',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
