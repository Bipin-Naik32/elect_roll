from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import VoterRecord

#@admin.register(VoterRecord)
#class VoterRecordAdmin(admin.ModelAdmin):
#    list_display = ('voter_id','ac_no','name','address','ac_name','date_of_birth', 
#    'part_no', 
#    'gender', 
 #   'ps_name', 
 #   'sec_no', 
 #   'sr_no', 
 #   'age', 
 #   'rel_name', 
 #   'rel_type', 
 #   'mob_no')


@admin.register(VoterRecord)
class VoterRecordAdmin(ImportExportModelAdmin):
    pass