from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import Tutor, Student
from .models import Subject, TutorSubject, AvailabilitySlot
from bookings.models import Booking


def tutor_list(request):
    tutors = Tutor.objects.filter(is_approved=True)
    subject_id = request.GET.get('subject')
    if subject_id:
        tutors = tutors.filter(subjects__subject_id=subject_id).distinct()
    
    subjects = Subject.objects.all()
    return render(request, 'tutors/tutor_list.html', {
        'tutors': tutors,
        'subjects': subjects
    })


def tutor_detail(request, tutor_id):
    tutor = get_object_or_404(Tutor, id=tutor_id, is_approved=True)
    # Changed from 'subjects' to 'tutor_subjects' to match template
    tutor_subjects = tutor.subjects.select_related('subject').all()
    availability_slots = tutor.availability_slots.filter(is_available=True)
    
    # Get ratings
    from ratings.models import Rating
    ratings = Rating.objects.filter(tutor=tutor)[:5]
    
    return render(request, 'tutors/tutor_detail.html', {
        'tutor': tutor,
        'tutor_subjects': tutor_subjects,  # Changed variable name
        'availability_slots': availability_slots,
        'ratings': ratings
    })


@login_required
def tutor_dashboard(request):
    if request.user.role != 'tutor':
        messages.error(request, 'Access denied!')
        return redirect('home')
    
    tutor = get_object_or_404(Tutor, user=request.user)
    bookings = Booking.objects.filter(tutor=tutor).order_by('-created_at')[:10]
    subjects = tutor.subjects.all()
    availability_slots = tutor.availability_slots.all()
    
    return render(request, 'tutors/dashboard.html', {
        'tutor': tutor,
        'bookings': bookings,
        'subjects': subjects,
        'availability_slots': availability_slots
    })


@login_required
def add_subject(request):
    if request.user.role != 'tutor':
        messages.error(request, 'Access denied!')
        return redirect('home')
    
    tutor = get_object_or_404(Tutor, user=request.user)
    
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        subject = get_object_or_404(Subject, id=subject_id)
        tutor_subject, created = TutorSubject.objects.get_or_create(tutor=tutor, subject=subject)
        if created:
            messages.success(request, 'Subject added successfully!')
        else:
            messages.info(request, 'Subject is already in your profile!')
        return redirect('tutor_dashboard')
    
    subjects = Subject.objects.all().order_by('name')
    tutor_subject_ids = set(tutor.subjects.values_list('subject_id', flat=True))
    
    return render(request, 'tutors/add_subject.html', {
        'subjects': subjects,
        'tutor_subject_ids': tutor_subject_ids
    })


@login_required
def add_availability(request):
    if request.user.role != 'tutor':
        messages.error(request, 'Access denied!')
        return redirect('home')
    
    tutor = get_object_or_404(Tutor, user=request.user)
    
    if request.method == 'POST':
        day_of_week = request.POST.get('day_of_week')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        
        AvailabilitySlot.objects.create(
            tutor=tutor,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time
        )
        messages.success(request, 'Availability slot added successfully!')
        return redirect('tutor_dashboard')
    
    return render(request, 'tutors/add_availability.html')