from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Student
from courses.models import Course

# LOGIN
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('student_list')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

# LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')

# STUDENT LIST
@login_required(login_url='login')
def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})

@login_required(login_url='login')
def add_student(request):
    courses = Course.objects.all()
    if request.method == 'POST':
        Student.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            course_id=request.POST['course'],
            dob=request.POST['dob'],
            address=request.POST['address']
        )
        return redirect('student_list')
    return render(request, 'add_student.html', {'courses': courses})

@login_required(login_url='login')
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    courses = Course.objects.all()
    if request.method == 'POST':
        student.name = request.POST['name']
        student.email = request.POST['email']
        student.phone = request.POST['phone']
        student.course_id = request.POST['course']
        student.dob = request.POST['dob']
        student.address = request.POST['address']
        student.save()
        return redirect('student_list')
    return render(request, 'edit_student.html', {'student': student, 'courses': courses})
