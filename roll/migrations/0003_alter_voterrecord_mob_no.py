# Generated by Django 5.1.4 on 2025-01-12 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roll', '0002_rename_mob_n0_voterrecord_mob_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voterrecord',
            name='mob_no',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
