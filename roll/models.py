from django.db import models
from django.contrib.auth.models import User
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
    status = models.CharField( max_length=50,default='Active')
    party_choice = models.CharField(max_length=50,blank=True,null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=30,blank=True,null=True)


    def __str__(self):
        return self.name

class VoterGradation(models.Model):
    voter = models.OneToOneField(
        VoterRecord,
        on_delete=models.CASCADE,
        related_name='gradation'
    )

    traditional = models.CharField(max_length=30, blank=True)
    swing_reason = models.TextField(blank=True, null=True)
    religion = models.CharField(max_length=30, blank=True)
    category = models.CharField(max_length=30, blank=True)
    caste = models.CharField(max_length=50, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    mobile_number = models.CharField(max_length=15, blank=True)
    completed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.voter.name} ({self.voter.part_no})"

class CategoryMaster(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class ReligionMaster(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class OccupationMaster(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class CasteMaster(models.Model):
    category = models.ForeignKey(
        CategoryMaster,
        on_delete=models.CASCADE,
        related_name="castes"
    )

    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]
        unique_together = ("category", "name")

    def __str__(self):
        return self.name