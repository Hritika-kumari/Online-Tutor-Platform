from django.db import models
from users.models import Student, Tutor


class Rating(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='ratings_given')
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='ratings')
    booking = models.ForeignKey('bookings.Booking', on_delete=models.CASCADE, related_name='rating', null=True, blank=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'tutor', 'booking']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.user.username} rated {self.tutor.user.username} - {self.rating} stars"
