from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import Student, Tutor
from bookings.models import Booking
from .models import Rating


@login_required
def add_rating(request, tutor_id, booking_id=None):
    if request.user.role != 'student':
        messages.error(request, 'Only students can rate tutors!')
        return redirect('home')
    
    tutor = get_object_or_404(Tutor, id=tutor_id)
    student = get_object_or_404(Student, user=request.user)
    booking = None
    
    if booking_id:
        booking = get_object_or_404(Booking, id=booking_id, student=student, tutor=tutor)
    
    if request.method == 'POST':
        rating_value = request.POST.get('rating')
        review = request.POST.get('review', '')
        
        rating, created = Rating.objects.get_or_create(
            student=student,
            tutor=tutor,
            booking=booking,
            defaults={'rating': rating_value, 'review': review}
        )
        
        if not created:
            rating.rating = rating_value
            rating.review = review
            rating.save()
        
        messages.success(request, 'Rating submitted successfully!')
        return redirect('tutor_detail', tutor_id=tutor_id)
    
    return render(request, 'ratings/add_rating.html', {
        'tutor': tutor,
        'booking': booking
    })
