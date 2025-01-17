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
    return render(request, 'dashboard.html')



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
    age = request.GET.get('age')
    part_no = request.GET.get('part_no')
    voter_id = request.GET.get('voter_id')
    rel_name = request.GET.get('rel_name')
    address = request.GET.get('address')
    mob_no = request.GET.get('mob_no')
    gender = request.GET.get('gender')
    sec_name= request.GET.get('sec_name')
    records = VoterRecord.objects.all()
    
   
    if name: 
        records = records.filter(name__icontains = name)
    if age :
        records = records.filter(age=age)
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

    

    if not any([name, age, part_no, voter_id,rel_name,address, mob_no,gender,sec_name]):
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
        headers = ['Name','Relative Name','Age','Mobile Number', 'Voter ID', 'Part_no','Address','Gender']
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
def return_to_dashboard(request):
    return redirect('dashboard')