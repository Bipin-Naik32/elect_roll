from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import VoterRecord
from .models import CategoryMaster, CasteMaster,ReligionMaster,OccupationMaster

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

@admin.register(CategoryMaster)
class CategoryMasterAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(CasteMaster)
class CasteMasterAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category",)
    search_fields = ("name",)
    ordering = ("category", "name")
    
admin.site.register(ReligionMaster)
admin.site.register(OccupationMaster)