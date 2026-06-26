import openpyxl
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
from django.core.exceptions import ValidationError
from twilio.rest import Client
from .models import VoterRecord
from .forms import VoterRecordForm
from .utils import format_phone_number_to_e164
from django.utils.text import slugify
from .utils import send_sms_gatewayhub
from django.db.models import Count
import json
# Views

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    # Filter values
   # part_no = request.GET.get('part_no').strip()
    #village = request.GET.get('village').strip()
   # section = request.GET.get('section').strip()
    part_no = (request.GET.get('part_no') or '').strip()
    village = (request.GET.get('village') or '').strip()
    section = (request.GET.get('section') or '').strip()
     # Base queryset
    records = VoterRecord.objects.all()

# Apply filters
    if part_no:
        try:
           records = records.filter(part_no=int(part_no))
        except ValueError:
           records = records.none()

    if village:
        records = records.filter(village__icontains=village )

    if section:
        records = records.filter(sec_name__icontains=section)

    total_voters = records.count()

    active_voters = records.filter(
        status__iexact='Active'
    ).count()

    dead_voters = records.filter(
        status__iexact='Dead'
    ).count()

    transferred_voters = records.filter(
        status__iexact='Transferred'
    ).count()

    mobile_available = (
        records.exclude(mob_no__isnull=True)
        .exclude(mob_no='')
        .count()
    )

    mobile_missing = total_voters - mobile_available

    if total_voters > 0:
        mobile_coverage = round(
            (mobile_available / total_voters) * 100,
            2
        )
    else:
        mobile_coverage = 0
   # Gender
    male_count = records.filter(gender='Male').count()
    female_count = records.filter(gender='Female').count()
    other_count = records.filter(gender='Other').count()

# Religion
    religion_stats = (
        records.exclude(religion__isnull=True)
        .exclude(religion='')
        .values('religion')
        .annotate(total=Count('id'))
        .order_by('-total')
         )

# Caste
    caste_stats = (
        records
         .exclude(caste__isnull=True)
         .exclude(caste='')
         .values('caste')
          .annotate(total=Count('id'))
         .order_by('-total')
        )
    religion_labels = [r['religion'] for r in religion_stats]
    religion_counts = [r['total'] for r in religion_stats]

    caste_labels = [c['caste'] for c in caste_stats]
    caste_counts = [c['total'] for c in caste_stats]

# Age Groups
    age_18_25 = records.filter(age__gte=18, age__lte=25).count()
    age_26_35 = records.filter(age__gte=26, age__lte=35).count()
    age_36_45 = records.filter(age__gte=36, age__lte=45).count()
    age_46_60 = records.filter(age__gte=46, age__lte=60).count()
    age_60_plus = records.filter(age__gt=60).count()

    context = {
        'total_voters': total_voters,
        'active_voters': active_voters,
        'dead_voters': dead_voters,
        'transferred_voters': transferred_voters,
        'mobile_available': mobile_available,
        'mobile_missing': mobile_missing,
        'mobile_coverage': mobile_coverage,
        'male_count': male_count,
'female_count': female_count,
'other_count': other_count,

'religion_stats': religion_stats,
'caste_stats': caste_stats,
'religion_labels': json.dumps(religion_labels),
'religion_counts': json.dumps(religion_counts),

'caste_labels': json.dumps(caste_labels),
'caste_counts': json.dumps(caste_counts),
'age_18_25': age_18_25,
'age_26_35': age_26_35,
'age_36_45': age_36_45,
'age_46_60': age_46_60,
'age_60_plus': age_60_plus,
 'selected_part': part_no,
'selected_village': village,
'selected_section': section,
   }

    return render(request, 'dashboard.html', context)



'''@login_required
def add_record(request):
    if request.method == 'POST':
        form = VoterRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Voter record added successfully!')
            return redirect('dashboard')
    else:
        form = VoterRecordForm()
    return render(request, 'add_record.html', {'form': form})'''
@login_required
def add_record(request):
    if request.method == 'POST':
        # Manually handle form submission
        name = request.POST.get('name', '').strip()
        rel_name = request.POST.get('rel_name', '').strip()
        age = request.POST.get('age', '').strip()
        voter_id = request.POST.get('voter_id', '').strip()
        address = request.POST.get('address', '').strip()
        mob_no = request.POST.get('mob_no', '').strip()
        gender = request.POST.get('gender', '').strip()
        date_of_birth = request.POST.get('date_of_birth', '').strip()
        part_no = request.POST.get('part_no', '').strip()
        sec_no = request.POST.get('sec_no', '').strip()
        sr_no = request.POST.get('sr_no', '').strip()
        rel_type = request.POST.get('rel_type', '').strip()
        ps_name = request.POST.get('ps_name', '').strip()
        sec_name = request.POST.get('sec_name', '').strip()
        village = request.POST.get('village', '').strip()
        religion = request.POST.get('religion', '').strip()
        caste = request.POST.get('caste', '').strip()
        status = request.POST.get('status', 'Active').strip()
        party_choice = request.POST.get('party_choice', '').strip()

        # Validate the fields (basic server-side validation)
        if not all([name, rel_name, age, voter_id, address, mob_no, gender]):
            messages.error(request, 'All fields are required.')
        elif not age.isdigit() or not (18 <= int(age) <= 120):
            messages.error(request, 'Age must be a valid number between 18 and 120.')
        elif not mob_no.isdigit() or len(mob_no) != 10:
            messages.error(request, 'Mobile number must be a valid 10-digit number.')
        else:
            # Manually parse date_of_birth if it's in DD/MM/YYYY format
            try:
                # Try to parse the date as DD/MM/YYYY
                parsed_date = datetime.strptime(date_of_birth, '%d/%m/%Y')
            except ValueError:
                try:
                    # If that fails, try the default format YYYY-MM-DD
                    parsed_date = datetime.strptime(date_of_birth, '%Y-%m-%d')
                except ValueError:
                    messages.error(request, 'Invalid date format. Please use DD/MM/YYYY or YYYY-MM-DD.')
                    return render(request, 'add_record.html')  # Show the form again with the error

            # Save the record if date is parsed correctly
            VoterRecord.objects.create(
                voter_id=voter_id,
                ac_no=22,
                name=name,
                address=address,
                ac_name='Siroda',
                date_of_birth=parsed_date,  # Save parsed date
                part_no=part_no,
                gender=gender,
                ps_name=ps_name,
                sec_no=sec_no,
                sec_name=sec_name,
                sr_no=sr_no,
                age=int(age),
                rel_name=rel_name,
                rel_type=rel_type,
                mob_no=mob_no,
                village=village,
                religion=religion,
                caste=caste,
                status=status,
                party_choice=party_choice,
            )
            messages.success(request, 'Voter record added successfully!')
            return redirect('dashboard')
    
    return render(request, 'add_record.html')

    

def suggest_voter_id(request):
    query = request.GET.get('q', '').strip()
    suggestions = []
    if query:
        suggestions = (
            VoterRecord.objects.filter(voter_id__icontains=query)
            .values_list('voter_id', flat=True)[:10]
        )
    return JsonResponse({'suggestions': list(suggestions)})
    
@login_required

def send_sms(request):
    # Twilio configuration (replace with your credentials)
    #TWILIO_ACCOUNT_SID = 'AC2f1d41c75075e8f288c7262385ec394f'
    #TWILIO_AUTH_TOKEN = '5d36c687b5cb82796e1cb52dac8726e7'
    #TWILIO_PHONE_NUMBER = '+17854533228'  # Replace with your Twilio phone number

    # Retrieve filtered record IDs from the query parameters
    record_ids = request.GET.getlist('ids')

    # Fetch the filtered records
    records = VoterRecord.objects.filter(id__in=record_ids)
    if request.method == "POST":

       custom_message = request.POST.get("custom_message", "")

       success_count = 0
       failure_count = 0

       for record in records:

           if record.mob_no:

               mobile = str(record.mob_no).strip()

               result = send_sms_gatewayhub(
                   mobile,
                   f"Hello {record.name}, {custom_message}"
                )

               print(result)

               success_count += 1

       return render(
           request,
           "send_sms.html",
          {
            "records": records,
            "success_count": success_count,
            "failure_count": failure_count
          }
       )
    

    '''if request.method == "POST":
        # Get the custom message from the form
        custom_message = request.POST.get('custom_message', '')

        # Send SMS to each record
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        for record in records:
            if record.mob_no:  # Ensure the record has a mobile number
                try:
                    formatted_number = format_phone_number_to_e164(record.mob_no)
                    message = client.messages.create(
                        body=f"Hello {record.name}, {custom_message}",
                        from_=TWILIO_PHONE_NUMBER,
                        to=formatted_number
                    )
                    print(f"SMS sent to {record.name}: {message.sid}")
                except Exception as e:
                    print(f"Failed to send SMS to {record.name}: {e}")

        return redirect('dashboard')'''

    return render(request, 'send_sms.html', {'records': records})


@login_required
def search_records(request):
    #query = request.GET.get('query')
    name = request.GET.get('name')
    #age = request.GET.get('age')
    min_age = request.GET.get('min_age')
    max_age = request.GET.get('max_age')
    print("MIN AGE =", min_age)
    print("MAX AGE =", max_age)
    part_no = request.GET.get('part_no')
    voter_id = request.GET.get('voter_id')
    rel_name = request.GET.get('rel_name')
    address = request.GET.get('address')
    mob_no = request.GET.get('mob_no')
    gender = request.GET.get('gender')
    sec_name= request.GET.get('sec_name')
    village= request.GET.get('village')
    religion= request.GET.get('religion')
    caste = request.GET.get('caste')
    status = request.GET.get('status')
    party_choice = request.GET.get('party_choice')
    records = VoterRecord.objects.all()


   
    if name: 
        records = records.filter(name__icontains = name)
    #if age :
     #   records = records.filter(age=age)
    if min_age:
        records = records.filter(age__gte=min_age)
    if max_age:
        records = records.filter(age__lte=max_age)
    if part_no:
        records = records.filter(part_no=part_no)
    if voter_id:
        records = records.filter(voter_id=voter_id)
    if rel_name:
        records = records.filter(relative__icontains=rel_name)
    if address:
        records = records.filter(address__icontains=address)
    if mob_no:
        records = records.filter(mob_no=mob_no)
    if gender:
        records = records.filter(gender=gender)
    if sec_name:
        records = records.filter(sec_name__icontains=sec_name)
    if village:
        records = records.filter(village__icontains=village)
    if religion:
        records = records.filter(religion__icontains=religion)
    if caste:
        records = records.filter(caste__icontains=caste)
    if status:
        records = records.filter(status__icontains=status)
    if party_choice:
        records = records.filter(party_choice__icontains=party_choice)

    print("Filtered records query:", records.query)
    print("Filtered records count:", records.count())

    if not any([name,min_age,max_age,part_no,voter_id,rel_name,address,mob_no,gender,sec_name,village,religion,caste,status,party_choice]):
        records = VoterRecord.objects.none()

    # Set up pagination
    records = records.order_by('id')
    paginator = Paginator(records, 25)  # Show 25 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Check if the user requested an Excel download
    if 'download' in request.GET:
        # Create an Excel workbook and worksheet
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = "Search Results"

        # Add headers
        headers = ['Name','Relative Name','Age','Mobile Number', 'Voter ID', 'Part_no','Address','Gender','Status',
'Party Choice',]
        worksheet.append(headers)

        # Add data rows
        for record in records:
            worksheet.append([
                record.name,
                record.rel_name,
                record.age,
                record.mob_no,
                record.voter_id,
                record.part_no,
                record.address,
                record.gender,
                record.status,
                record.party_choice,
            ])

        # Prepare the response as an Excel file
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response['Content-Disposition'] = 'attachment; filename=search_results.xlsx'
        workbook.save(response)
        return response

    return render(request, 'search_records.html', {'page_obj': page_obj})

@login_required
def edit_record(request, record_id):
    # Get the record or return a 404 if not found
    record = get_object_or_404(VoterRecord, id=record_id)
    print(record.address)

    if request.method == 'POST':
        # Manually get the data from the POST request
        record.name = request.POST.get('name', record.name)
        record.rel_name = request.POST.get('rel_name', record.rel_name)
        record.age = request.POST.get('age', record.age)
        record.mob_no = request.POST.get('mob_no', record.mob_no)
        record.voter_id = request.POST.get('voter_id', record.voter_id)
        record.part_no = request.POST.get('part_no', record.part_no)
        record.address = request.POST.get('address', record.address)
        record.gender = request.POST.get('gender', record.gender)
        record.sr_no = request.POST.get('sr_no', record.sr_no)
        record.religion = request.POST.get('religion', record.religion)
        record.rel_type = request.POST.get('rel_type', record.rel_type)
        record.caste = request.POST.get('caste', record.caste)
        # Parse and handle the date_of_birth field
        date_of_birth_str = request.POST.get('date_of_birth', record.date_of_birth)
        if date_of_birth_str:
            try:
                # Assuming the format is YYYY-MM-DD; adjust the format if needed
                record.date_of_birth = datetime.strptime(date_of_birth_str, '%B %d, %Y').date()
            except ValueError:
                messages.error(request, 'Invalid date format. Please use YYYY-MM-DD.')
                return redirect('edit_record', record_id=record.id)  # Redirect back to edit page in case of error
        record.village = request.POST.get('village', record.village)
        record.sec_no = request.POST.get('sec_no', record.sec_no)
        record.sec_name = request.POST.get('sec_name', record.sec_name)
        record.ps_name = request.POST.get('ps_name', record.ps_name).strip()
        record.status = request.POST.get('status', record.status)
        record.party_choice = request.POST.get('party_choice', record.party_choice)

        # Validate and save the record
        try:
            record.age = int(record.age)
            record.save()
            messages.success(request, 'Record updated successfully!')
            print(record.address)
            return redirect('search_records')  # Redirect to the search page
        except ValueError:
            messages.error(request, 'Invalid input. Please ensure age is a number.')

    return render(request, 'edit_record.html', {'record': record})
@login_required
def export_vcf(request):
    record_ids = request.GET.getlist('ids')

    records = VoterRecord.objects.filter(id__in=record_ids)

    if records.exists():
        section_name = records.first().sec_name or "contacts"
    else:
        section_name = "contacts"

    filename = f"{slugify(section_name)}.vcf"

    response = HttpResponse(content_type='text/vcard')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    for record in records:
        mobile = str(record.mob_no).strip()

        if not mobile:
            continue

        if len(mobile) == 10:
            mobile = "91" + mobile

        response.write(
            f"BEGIN:VCARD\n"
            f"VERSION:3.0\n"
            f"N:{record.name}\n"
            f"FN:[{record.sec_name}] {record.name}\n"
            f"TEL;TYPE=CELL:+{mobile}\n"
            f"END:VCARD\n"
        )

    return response

@login_required
def return_to_dashboard(request):
    return redirect('dashboard')
