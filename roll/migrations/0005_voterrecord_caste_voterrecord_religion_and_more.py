# Generated by Django 5.1.4 on 2025-01-20 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roll', '0004_voterrecord_sec_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='voterrecord',
            name='caste',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='voterrecord',
            name='religion',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='voterrecord',
            name='village',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
