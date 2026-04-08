from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Project, ContactMessage
from blog.models import Post


def home(request):
    featured_projects = Project.objects.filter(featured=True)[:3]
    latest_posts = Post.objects.filter(published=True)[:2]
    return render(request, 'portfolio/home.html', {
        'projects': featured_projects,
        'posts': latest_posts,
    })


def about(request):
    skills = [
        {'name': 'HTML', 'level': 85},
        {'name': 'CSS', 'level': 80},
        {'name': 'JavaScript', 'level': 70},
        {'name': 'Python', 'level': 80},
        {'name': 'Django', 'level': 70},
        {'name': 'GitHub', 'level': 75},
    ]
    return render(request, 'portfolio/about.html', {'skills': skills})


def projects(request):
    all_projects = Project.objects.all()
    return render(request, 'portfolio/projects.html', {'projects': all_projects})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        # Basic validation
        if not all([name, email, subject, message]):
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'portfolio/contact.html')

        # Save to database
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )

        # Send email notification to yourself
        try:
            send_mail(
                subject=f"Portfolio Contact: {subject}",
                message=f"From: {name} <{email}>\n\n{message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
        except Exception:
            # Email failed but message is still saved in DB, so don't crash
            pass

        messages.success(request, "Message sent! I'll get back to you soon.")
        return redirect('contact')

    return render(request, 'portfolio/contact.html')