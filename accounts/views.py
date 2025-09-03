from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from .forms import StudentRegisterForm, StudentLoginForm, StudentForm, ConcessionApplicationForm
from .models import CustomUser, Student, ConcessionApplication

User = get_user_model()

# -----------------------------
# Registration
# -----------------------------
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        full_name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmPassword']

        if password != confirm_password:
            return render(request, 'accounts/register.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/register.html', {'error': 'Username already exists'})

        user = CustomUser.objects.create(
            username=username,
            email=email,
            full_name=full_name,
            password=make_password(password)
        )

        # create linked Student object with blank/defaults
        Student.objects.create(user=user, full_name=full_name, branch='', year=0)

        return redirect('login')

    return render(request, 'accounts/register.html')


# -----------------------------
# Login
# -----------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('student')  # redirect to booking page
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})

    return render(request, 'accounts/login.html')


# -----------------------------
# Student page (Profile + Concession Application)
# -----------------------------


@login_required
def student_booking(request):
    error = None
    success = None
    student, created = Student.objects.get_or_create(user=request.user)
    now = timezone.now()
    last_application = ConcessionApplication.objects.filter(student=student).order_by('-applied_at').first()
   
    next_allowed_date = None

    # ---------- Check last application ---------- #
    if last_application:
        period = last_application.period.lower()
        if period == "monthly":
            next_allowed_date = last_application.applied_at + timedelta(days=30)
            if now < next_allowed_date:
                error = f"You already submitted a monthly concession. You can apply again after {next_allowed_date.strftime('%d %b %Y')}."
        elif period == "quarterly":
            next_allowed_date = last_application.applied_at + timedelta(days=90)
            if now < next_allowed_date:
                error = f"You already submitted a quarterly concession. You can apply again after {next_allowed_date.strftime('%d %b %Y')}."

    # ---------- Handle form submission ---------- #
    if request.method == "POST":
        if "save_student" in request.POST:
            # Handle Student Profile update
            student_form = StudentForm(request.POST, instance=student)
            if student_form.is_valid():
                student_form.save()
                messages.success(request, "Student profile saved successfully.")
                return redirect("student")

        elif "apply_concession" in request.POST:
            # Handle Concession Application
            if error:
                messages.error(request, error)
            else:
                concession_form = ConcessionApplicationForm(request.POST)
                if concession_form.is_valid():
                    application = concession_form.save(commit=False)
                    application.student = student
                    application.applied_at = timezone.now()
                    application.save()
                    # Send email notification to the student
                    if student.user.email:
                        # Only send if the email is a college email
                        if student.user.email.endswith('@vit.edu.in'):  # change domain as needed
                            subject = 'Concession Eligibility Confirmation'
                            message = f"""
Dear {student.full_name},

You are eligible to submit the concession application.

Here are your submitted details:
- Username: {student.user.username}
- Full Name: {student.full_name}
- Email: {student.user.email}
- Class: {application.class_type}
- Period: {application.period}
- From Station: {application.from_station}
- To Station: {application.to_station}
- Railway Line: {application.line}

Thank you.
"""
                            send_mail(
                                subject,
                                message,
                                settings.EMAIL_HOST_USER,  # Use the configured email
                                [student.user.email],
                                fail_silently=False,
                            )
                            messages.success(request, "Booking successful! A verification email has been sent to your college email.")
                        else:
                            messages.warning(request, "Booking successful, but email not sent. Please use a valid college email.")
                    return redirect("student")

    # ---------- GET Request or invalid POST ---------- #
    student_form = StudentForm(instance=student)
    concession_form = ConcessionApplicationForm()

    return render(request, 'accounts/student.html', {
        'form': student_form,
        'concession_form': concession_form,
       
        'next_allowed_date': next_allowed_date
    })




# -----------------------------
# Home page
# -----------------------------
@login_required
def home(request):
    return render(request, "accounts/home.html")
