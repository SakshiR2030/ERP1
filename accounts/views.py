from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .forms import StudentRegisterForm, StudentLoginForm, StudentForm, ConcessionApplicationForm
from .models import Student, ConcessionApplication

User = get_user_model()


# -----------------------------
# Registration
# -----------------------------
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import CustomUser, Student
from django.contrib.auth.hashers import make_password

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        full_name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmPassword']

        if password != confirm_password:
            return render(request, 'accounts/register.html', {'error': 'Passwords do not match'})

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
from django.contrib.auth import authenticate, login

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
# Student profile
# -----------------------------
from django.contrib.auth.decorators import login_required
from .models import Student, ConcessionApplication

@login_required
def student_booking(request):
    if request.method == "POST":
        student = Student.objects.get(user=request.user)
        class_type = request.POST['class_type']
        period = request.POST['period']
        line = request.POST['line']
        from_station = request.POST['from_station']
        to_station = request.POST['to_station']

        ConcessionApplication.objects.create(
            student=student,
            class_type=class_type,
            period=period,
            line=line,
            from_station=from_station,
            to_station=to_station
        )
        return render(request, 'accounts/student.html', {'success': 'Booking successful!'})

    return render(request, 'accounts/student.html')



# -----------------------------
# Home page
# -----------------------------
@login_required
def home(request):
    return render(request, "accounts/home.html")


# -----------------------------
# Concession application
# -----------------------------
@login_required
def concession_application(request):
    student, created = Student.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ConcessionApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.student = student   # always link concession to logged-in student
            application.save()
            return redirect("student")

    return render(request, "accounts/concession.html", {"form": ConcessionApplicationForm()})

 