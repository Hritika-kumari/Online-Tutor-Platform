from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Student, Tutor


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role', 'student')
        phone = request.POST.get('phone', '')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('register')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
            phone=phone
        )
        
        if role == 'student':
            Student.objects.create(user=user)
        elif role == 'tutor':
            Tutor.objects.create(user=user)
        
        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')
    
    return render(request, 'users/register.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'tutor':
                return redirect('tutor_dashboard')
            elif user.role == 'admin' or user.is_superuser:
                return redirect('admin_dashboard')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password!')
    
    return render(request, 'users/login.html')


@login_required
def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('login')


def home(request):
    tutors = Tutor.objects.filter(is_approved=True)[:6]
    return render(request, 'home.html', {'tutors': tutors})


@login_required
def student_profile(request):
    if request.user.role != 'student':
        messages.error(request, 'Access denied!')
        return redirect('home')
    
    student = get_object_or_404(Student, user=request.user)
    from bookings.models import Booking
    bookings = Booking.objects.filter(student=student).order_by('-created_at')[:5]
    total_bookings = Booking.objects.filter(student=student).count()
    completed_bookings = Booking.objects.filter(student=student, status='completed').count()
    
    return render(request, 'users/student_profile.html', {
        'student': student,
        'bookings': bookings,
        'total_bookings': total_bookings,
        'completed_bookings': completed_bookings,
    })


@login_required
def tutor_profile(request):
    if request.user.role != 'tutor':
        messages.error(request, 'Access denied!')
        return redirect('home')
    
    tutor = get_object_or_404(Tutor, user=request.user)
    from bookings.models import Booking
    from ratings.models import Rating
    from tutors.models import TutorSubject
    
    bookings = Booking.objects.filter(tutor=tutor).order_by('-created_at')[:5]
    total_bookings = Booking.objects.filter(tutor=tutor).count()
    subjects = tutor.subjects.all()
    ratings = Rating.objects.filter(tutor=tutor)[:5]
    total_ratings = Rating.objects.filter(tutor=tutor).count()
    
    return render(request, 'users/tutor_profile.html', {
        'tutor': tutor,
        'bookings': bookings,
        'total_bookings': total_bookings,
        'subjects': subjects,
        'ratings': ratings,
        'total_ratings': total_ratings,
    })


@login_required
def edit_student_profile(request):
    if request.user.role != 'student':
        messages.error(request, 'Access denied!')
        return redirect('home')
    
    student = get_object_or_404(Student, user=request.user)
    
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.phone = request.POST.get('phone', '')
        student.bio = request.POST.get('bio', '')
        
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        
        user.save()
        student.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('student_profile')
    
    return render(request, 'users/edit_student_profile.html', {
        'student': student,
    })


@login_required
def edit_tutor_profile(request):
    if request.user.role != 'tutor':
        messages.error(request, 'Access denied!')
        return redirect('home')
    
    tutor = get_object_or_404(Tutor, user=request.user)
    
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.phone = request.POST.get('phone', '')
        tutor.bio = request.POST.get('bio', '')
        try:
            tutor.experience_years = int(request.POST.get('experience_years', 0))
        except (ValueError, TypeError):
            tutor.experience_years = 0
        try:
            tutor.hourly_rate = float(request.POST.get('hourly_rate', 0.00))
        except (ValueError, TypeError):
            tutor.hourly_rate = 0.00
        
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        
        user.save()
        tutor.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('tutor_profile')
    
    return render(request, 'users/edit_tutor_profile.html', {
        'tutor': tutor,
    })


@login_required
def admin_dashboard(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        messages.error(request, 'Access denied! Only admins can access this page.')
        return redirect('home')
    
    # Get statistics
    total_students = Student.objects.count()
    total_tutors = Tutor.objects.count()
    
    from materials.models import Material
    total_materials = Material.objects.count()
    
    from bookings.models import Booking
    total_bookings = Booking.objects.count()
    
    # Get lists
    students = Student.objects.select_related('user').all().order_by('-user__created_at')
    tutors = Tutor.objects.select_related('user').all().order_by('-user__created_at')
    
    return render(request, 'users/admin_dashboard.html', {
        'total_students': total_students,
        'total_tutors': total_tutors,
        'total_materials': total_materials,
        'total_bookings': total_bookings,
        'students': students,
        'tutors': tutors,
    })