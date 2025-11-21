from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import Tutor
from tutors.models import Subject
from .models import Material


@login_required
def material_list(request):
    materials = Material.objects.all()
    subject_id = request.GET.get('subject')
    if subject_id:
        materials = materials.filter(subject_id=subject_id)
    
    subjects = Subject.objects.all()
    return render(request, 'materials/material_list.html', {
        'materials': materials,
        'subjects': subjects
    })


@login_required
def upload_material(request):
    if request.user.role != 'tutor':
        messages.error(request, 'Only tutors can upload materials!')
        return redirect('home')
    
    tutor = Tutor.objects.get(user=request.user)
    
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        file = request.FILES.get('file')
        material_type = request.POST.get('material_type', 'pdf')
        
        subject = Subject.objects.get(id=subject_id)
        
        Material.objects.create(
            tutor=tutor,
            subject=subject,
            title=title,
            description=description,
            file=file,
            material_type=material_type
        )
        messages.success(request, 'Material uploaded successfully!')
        return redirect('material_list')
    
    tutor_subjects = tutor.subjects.all()
    return render(request, 'materials/upload_material.html', {
        'tutor_subjects': tutor_subjects
    })
