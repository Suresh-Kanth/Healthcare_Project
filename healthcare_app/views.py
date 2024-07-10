from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
# from .models import Doctor, Patient,Blog
from .models import Users,Blog,Appointment
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from datetime import date
from django.utils import timezone
def signup(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address_line1 = request.POST.get('address-line1')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        image=request.FILES.get('profile-photo')
        is_doctor = 'doctor' == request.POST.get('user_type')

        # Check if the email already exists
        if Users.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please use a different email.')
            return render(request, 'signup.html')

        # Create the User object
        user = User.objects.create_user(username=email, email=email, password=password)
        user = Users(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                address_line1=address_line1,
                city=city,
                state=state,
                pincode=pincode,
                image=image,
                is_doctor=is_doctor
            )
        user.save()
        messages.success(request, 'User account created successfully.')

        # if user_type == 'doctor':
        #     # Create Doctor object
        #     doctor = Doctor(
        #         first_name=first_name,
        #         last_name=last_name,
        #         username=username,
        #         email=email,
        #         address_line1=address_line1,
        #         city=city,
        #         state=state,
        #         pincode=pincode,
        #         image=image
        #     )
        #     doctor.save()
        #     messages.success(request, 'Doctor account created successfully.')
            
        # elif user_type == 'patient':
        #     patient = Patient(
        #         first_name=first_name,
        #         last_name=last_name,
        #         username=username,
        #         email=email,
        #         address_line1=address_line1,
        #         city=city,
        #         state=state,
        #         pincode=pincode,
        #         image=image
        #     )
        #     patient.save()
        #     messages.success(request, 'Patient account created successfully.')
        
        return redirect('login')
    
    return render(request, 'signup.html')


def user_login(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type') 
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            try:
                user = Users.objects.get(email=email) 
                return redirect('dashboard')
            except Users.DoesNotExist:
                messages.error(request, 'User profile not found.')
                return render(request, 'login.html')

            # if user_type == 'doctor':
            #     try:
            #         doctor = Doctor.objects.get(email=email) 
            #         return redirect('doctor')
            #     except Doctor.DoesNotExist:
            #         messages.error(request, 'Doctor profile not found.')
            #         return render(request, 'login.html')

            # elif user_type == 'patient':
            #     try:
            #         patient = Patient.objects.get(email=email)
            #         return redirect('patient')
            #     except Patient.DoesNotExist:
            #         messages.error(request, 'Patient profile not found.')
            #         return render(request, 'login.html')

        else:
            # Authentication failed
            messages.error(request, 'Invalid email or password.')
            return render(request, 'login.html')

    else:
        # Render the login form for GET requests
        return render(request, 'login.html')

# @login_required(login_url='login')
# def doctor(request):
#     doctor = get_object_or_404(Doctor, email=request.user.email)
#     return render(request, 'doctor_dashboard.html', {'user': doctor})

# @login_required(login_url='login')
# def patient(request):
#     patient = get_object_or_404(Patient, email=request.user.email)
#     return render(request, 'patient_dashboard.html', {'user': patient})

@login_required(login_url='login')
def dashboard(request):
    user = get_object_or_404(Users, email=request.user.email)
    return render(request, 'dashboard.html', {'user': user})


def Logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def Add_Blog(request):
    user = get_object_or_404(Users, email=request.user.email)
    if user.is_doctor:
        if request.method == 'POST':
            title = request.POST.get('title')
            image = request.FILES.get('image')
            category = request.POST.get('category')
            summary = request.POST.get('summary')
            content = request.POST.get('content')
            is_draft = bool(request.POST.get('draft'))

            # Assuming you have a ForeignKey relationship with Doctor for author
            # author = request.user.doctor  # Adjust this based on your user and Doctor setup
            author = user

            # Create a Blog object
            blog = Blog(
                title=title,
                image=image,
                category=category,
                summary=summary,
                content=content,
                author=author,
                draft=is_draft
            )
            blog.save()
            
            messages.success(request, 'Blog created successfully.')
            return redirect('dashboard')
        
        # If not POST, render the form again (GET request)
        return render(request, 'add_blog.html',{'is_doctor':user.is_doctor} )
    else:
        messages.error(request, 'Only Doctors can Access')
        return redirect('dashboard')

@login_required(login_url='login')
def blog(request, blog_no):
    blog = get_object_or_404(Blog, no = blog_no )
    user = get_object_or_404(Users, email=request.user.email)
    context = {
        'blog': blog,
        'is_doctor': user.is_doctor
    }
    return render(request, 'blog.html', context)

# @login_required(login_url='login')
# def blogs(request):
#     blogs = Blog.objects.filter(draft=False)
#     user = get_object_or_404(Users, email=request.user.email)
#     context = {
#         'blogs': blogs,
#         'is_doctor': user.is_doctor
#     }
#     return render(request, 'blogs.html',context)


# @login_required(login_url='login')
# def blogs(request):
#     if request.method == 'GET' and 'category_id' in request.GET:
#         category_id = request.GET['category_id']
#         category = get_object_or_404(Category, id=category_id)
#         blogs = Blog.objects.filter(category=category, draft=False)
#     else:
#         blogs = Blog.objects.filter(draft=False)
    
#     user = get_object_or_404(Users, email=request.user.email)
#     categories = Category.objects.filter(blog__draft=False).distinct()

#     context = {
#         'blogs': blogs,
#         'is_doctor': user.is_doctor,
#         'categories': categories,
#     }
#     return render(request, 'categories.html', context)

# @login_required(login_url='login')
# def blogs(request):
#     categories = Blog.objects.filter(draft=False).values_list('category', flat=True).distinct()

#     if 'category' in request.GET:
#         category = request.GET['category']
#         blogs = Blog.objects.filter(category=category, draft=False)
#     else:
#         blogs = Blog.objects.filter(draft=False)

#     user = get_object_or_404(Users, email=request.user.email)

#     context = {
#         'blogs': blogs,
#         'is_doctor': user.is_doctor,
#         'categories': categories,
#     }
#     return render(request, 'blogs.html', context)
@login_required(login_url='login')
def blogs(request):
    categories = Blog.objects.filter(draft=False).values_list('category', flat=True).distinct()

    category = request.GET.get('category')

    if category:
        blogs = Blog.objects.filter(category=category, draft=False)
    else:
        blogs = Blog.objects.filter(draft=False)

    user = get_object_or_404(Users, email=request.user.email)

    context = {
        'blogs': blogs,
        'is_doctor': user.is_doctor,
        'categories': categories,
    }
    return render(request, 'blogs.html', context)

@login_required(login_url='login')
def myblogs(request):
    user = get_object_or_404(Users, email=request.user.email)
    if user.is_doctor:
        blogs = Blog.objects.filter(author=user,draft=False)
        context = {
            'blogs': blogs,
            'is_doctor': user.is_doctor
        }
        return render(request, 'blogs.html', context)
    else:
        messages.error(request, 'Only Doctors can Access')
        return redirect('dashboard')

@login_required(login_url='login')
def mydrafts(request):
    user = get_object_or_404(Users, email=request.user.email)
    if user.is_doctor:
        blogs = Blog.objects.filter(author=user, draft=True)
        context = {
            'blogs': blogs,
            'is_doctor': user.is_doctor
        }
        return render(request, 'blogs.html', context)
    else:
        messages.error(request, 'Only Doctors can Access')
        return redirect('dashboard')


@login_required(login_url='login')
def draft(request, blog_no):
    user = get_object_or_404(Users, email=request.user.email)
    if user.is_doctor:
        blog = get_object_or_404(Blog, no=blog_no)
        if request.method == 'POST':
            # Update existing blog draft
            blog.title = request.POST.get('title')
            new_image = request.FILES.get('image')
            if new_image:
                blog.image = new_image
            blog.category = request.POST.get('category')
            blog.summary = request.POST.get('summary')
            blog.content = request.POST.get('content')
            blog.draft = bool(request.POST.get('draft'))

            blog.save()
            messages.success(request, 'Blog draft updated successfully.')
            return redirect('dashboard')
        
        # If not POST, render the draft edit form with existing data
        context = {
            'blog': blog,
            'is_doctor': user.is_doctor
        }
        return render(request, 'draft.html', context)
    else:
        messages.error(request, 'Only Doctors can access.')
        return redirect('dashboard')

@login_required(login_url='login')
def bookappointment(request):
    user = get_object_or_404(Users, email=request.user.email)
    if not user.is_doctor:
        doctors = Users.objects.filter(is_doctor=True)
        return render(request, 'bookappointment.html', {'doctors': doctors})
    else:
        messages.error(request, 'Only Patients can Access')
        return redirect('dashboard')

from datetime import datetime, timedelta

from django.utils import timezone

@login_required(login_url='login')
def doctor_appointment(request, doctor_no):
    patient = get_object_or_404(Users, email=request.user.email)
    if not patient.is_doctor:
        doctor = get_object_or_404(Users, no=doctor_no)
        if request.method == 'POST':
            speciality = request.POST.get('speciality')
            date = request.POST.get('date')
            time = request.POST.get('time')
            
            # Check if the requested datetime is in the future
            requested_datetime = timezone.make_aware(datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M'))

            if requested_datetime < timezone.now():
                messages.error(request, 'You cannot schedule appointments in the past. Please choose a future date and time.')
                return render(request, 'doctor_appointment.html', {'doctor': doctor})
            
            requested_end_datetime = requested_datetime + timedelta(minutes=45)
            
            # Check if the requested time slot overlaps with existing appointments
            appointments = Appointment.objects.filter(doctor=doctor)
            for appointment in appointments:
                start_datetime = datetime.combine(appointment.date, appointment.time)
                end_datetime = start_datetime + timedelta(minutes=45)
                
                # Check for overlap
                if requested_datetime < end_datetime and requested_end_datetime > start_datetime:
                    messages.error(request, 'The requested appointment time overlaps with an existing appointment. Please choose another time.')
                    return render(request, 'doctor_appointment.html', {'doctor': doctor})
            
            # If no overlap and future date, create the appointment
            appointment = Appointment(
                doctor=doctor,
                patient=patient,
                date=date,
                time=time,
                speciality=speciality
            )
            appointment.save()
            
            messages.success(request, 'Appointment scheduled successfully!')
            return redirect('appointment_confirmation', appointment_no=appointment.no)
        
        return render(request, 'doctor_appointment.html', {'doctor': doctor})
    else:
        messages.error(request, 'Only Patients can access this functionality.')
        return redirect('dashboard')



@login_required(login_url='login')
def appointment_confirmation(request, appointment_no):
    appointment = get_object_or_404(Appointment, no=appointment_no)
    user = get_object_or_404(Users, email=request.user.email)
    
    # Combine date from appointment.date and time from appointment.time to create a datetime object
    appointment_datetime = datetime.combine(appointment.date, appointment.time)
    
    # Calculate end time by adding 45 minutes to appointment start time
    end_time = appointment_datetime + timedelta(minutes=45)

    context = {
        'appointment': appointment,
        'end_time': end_time,  # Include end_time in context
        'is_doctor': user.is_doctor,
    }
    return render(request, 'appointment_confirmation.html', context)

@login_required(login_url='login')
def myappointments(request):
    user = get_object_or_404(Users, email=request.user.email)
    
    status = request.GET.get('status', 'all')  # Default to 'all' if status parameter is not provided
    if user.is_doctor :
        if status == 'future':
            appointments = Appointment.objects.filter(doctor=user, date__gte=date.today()).order_by('date', 'time')
        elif status == 'past':
            appointments = Appointment.objects.filter(doctor=user, date__lt=date.today()).order_by('-date', '-time')
        else:
            appointments = Appointment.objects.filter(doctor=user).order_by('-date', '-time')
    else:
        if status == 'future':
            appointments = Appointment.objects.filter(patient=user, date__gte=date.today()).order_by('date', 'time')
        elif status == 'past':
            appointments = Appointment.objects.filter(patient=user, date__lt=date.today()).order_by('-date', '-time')
        else:
            appointments = Appointment.objects.filter(patient=user).order_by('-date', '-time')
    context = {
        'appointments': appointments,
        'status': status,
        'is_doctor': user.is_doctor,
    }
    return render(request, 'myappointments.html', context)
