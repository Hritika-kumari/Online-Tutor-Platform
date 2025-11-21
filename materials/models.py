from django.db import models
from users.models import Tutor


class Material(models.Model):
    MATERIAL_TYPE_CHOICES = [
        ('pdf', 'PDF'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('other', 'Other'),
    ]
    
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='materials')
    subject = models.ForeignKey('tutors.Subject', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='materials/')
    material_type = models.CharField(max_length=10, choices=MATERIAL_TYPE_CHOICES, default='pdf')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.tutor.user.username}"
