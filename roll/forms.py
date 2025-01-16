from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import VoterRecord  # Ensure you import your actual model

class VoterRecordForm(forms.ModelForm):
    class Meta:
        model = VoterRecord  # Replace with your actual model name
        fields = ['voter_id','ac_no','name','address','ac_name','date_of_birth', 
    'part_no', 
    'gender', 
    'ps_name', 
    'sec_no', 
    'sr_no', 
    'age', 
    'rel_name', 
    'rel_type', 
    'mob_no']  # Include the relevant fields from your model

 # Additional validators
    mob_no = forms.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="Enter a valid 10-digit mobile number.",
                code='invalid_mobile'
            )
        ],
        label="Mobile Number",
    )

    voter_id = forms.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^[A-Z]{3}[0-9]{7}$',
                message="Enter a valid voter ID (e.g., ABC1234567).",
                code='invalid_voter_id'
            )
        ],
        label="Voter ID",
    )

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 18:
            raise ValidationError("Age must be at least 18.")
        return age

    '''def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth >= forms.DateField().today():
            raise ValidationError("Date of birth cannot be in the future.")
        return date_of_birth

    def clean_rel_type(self):
        rel_type = self.cleaned_data.get('rel_type')
        valid_choices = ['Father', 'Mother', 'Spouse', 'Guardian']
        if rel_type not in valid_choices:
            raise ValidationError(f"Relation type must be one of {', '.join(valid_choices)}.")
        return rel_type'''

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        address = cleaned_data.get('address')

        if not name or len(name) < 3:
            self.add_error('name', "Name must be at least 3 characters long.")

        if not address or len(address) < 10:
            self.add_error('address', "Address must be at least 10 characters long.")
        return cleaned_data