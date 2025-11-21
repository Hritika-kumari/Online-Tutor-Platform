from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import Student, Tutor
from tutors.models import Subject
from .models import Booking


@login_required
def create_booking(request, tutor_id):
    if request.user.role != 'student':
        messages.error(request, 'Only students can book sessions!')
        return redirect('home')
    
    tutor = get_object_or_404(Tutor, id=tutor_id, is_approved=True)
    student = get_object_or_404(Student, user=request.user)
    
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        notes = request.POST.get('notes', '')
        
        subject = get_object_or_404(Subject, id=subject_id)
        
        Booking.objects.create(
            student=student,
            tutor=tutor,
            subject=subject,
            date=date,
            start_time=start_time,
            end_time=end_time,
            notes=notes
        )
        messages.success(request, 'Booking request sent successfully!')
        return redirect('student_dashboard')
    
    tutor_subjects = tutor.subjects.all()
    return render(request, 'bookings/create_booking.html', {
        'tutor': tutor,
        'tutor_subjects': tutor_subjects
    })


@login_required
def update_booking_status(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.user.role == 'tutor' and booking.tutor.user != request.user:
        messages.error(request, 'Access denied!')
        return redirect('home')
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['accepted', 'rejected', 'completed', 'cancelled']:
            booking.status = status
            booking.save()
            messages.success(request, f'Booking {status} successfully!')
            
            if request.user.role == 'tutor':
                return redirect('tutor_dashboard')
            else:
                return redirect('student_dashboard')
    
    return redirect('home')


@login_required
def student_dashboard(request):
    student = request.user.student_profile
    bookings = Booking.objects.filter(student=student).order_by('-date', '-start_time')
    
    # Calculate statistics
    total_bookings = bookings.count()
    accepted_completed_count = bookings.filter(status__in=['accepted', 'completed']).count()
    pending_count = bookings.filter(status='pending').count()
    
    return render(request, 'bookings/student_dashboard.html', {
        'student': student,
        'bookings': bookings,
        'total_bookings': total_bookings,
        'accepted_completed_count': accepted_completed_count,
        'pending_count': pending_count,
    })
