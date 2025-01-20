from django.db import models

# Create your models here.
class VoterRecord(models.Model):
    voter_id = models.CharField(max_length=20, unique=True)
    ac_no = models.IntegerField()
    name = models.CharField(max_length=100)
    address = models.TextField()
    ac_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    part_no = models.IntegerField()
    gender = models.TextField()
    ps_name = models.TextField()
    sec_no = models.IntegerField()
    sec_name = models.CharField(max_length=255,null=True)
    sr_no = models.IntegerField()
    age = models.IntegerField()
    rel_name = models.TextField()
    rel_type = models.TextField()
    mob_no = models.CharField(max_length=15, null=True, blank=True)
    village = models.CharField(max_length=15, null=True, blank=True)
    religion = models.CharField(max_length=15, null=True, blank=True)
    caste = models.CharField(max_length=15, null=True, blank=True)


    def __str__(self):
        return self.name