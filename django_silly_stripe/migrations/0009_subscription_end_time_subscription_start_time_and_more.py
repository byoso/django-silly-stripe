# Generated by Django 4.2 on 2023-07-26 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_silly_stripe', '0008_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='end_time',
            field=models.CharField(default='0', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='start_time',
            field=models.CharField(default='0', max_length=16),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subscription',
            name='status',
            field=models.CharField(max_length=64),
        ),
    ]
