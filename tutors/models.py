from django.db import models
from users.models import Tutor


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class TutorSubject(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['tutor', 'subject']
    
    def __str__(self):
        return f"{self.tutor.user.username} - {self.subject.name}"


class AvailabilitySlot(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='availability_slots')
    day_of_week = models.IntegerField(choices=[
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return f"{self.tutor.user.username} - {days[self.day_of_week]} {self.start_time} to {self.end_time}"
