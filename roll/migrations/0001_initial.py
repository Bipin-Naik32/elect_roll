# Generated by Django 5.1.4 on 2025-01-10 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VoterRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voter_id', models.CharField(max_length=20, unique=True)),
                ('ac_no', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('ac_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('part_no', models.IntegerField()),
                ('gender', models.TextField()),
                ('ps_name', models.TextField()),
                ('sec_no', models.IntegerField()),
                ('sr_no', models.IntegerField()),
                ('age', models.IntegerField()),
                ('rel_name', models.TextField()),
                ('rel_type', models.TextField()),
                ('mob_n0', models.IntegerField()),
            ],
        ),
    ]
