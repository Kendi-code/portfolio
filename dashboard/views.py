from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from portfolio.models import Project, ContactMessage
from blog.models import Post


# ─── LOGIN ───────────────────────────────────────────────
def dashboard_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard_home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('dashboard_home')
        else:
            messages.error(request, 'Invalid credentials.')

    return render(request, 'dashboard/login.html')


def dashboard_logout(request):
    logout(request)
    return redirect('dashboard_login')


# ─── HOME / OVERVIEW ─────────────────────────────────────
@login_required(login_url='dashboard_login')
def dashboard_home(request):
    stats = {
        'projects': Project.objects.count(),
        'posts': Post.objects.count(),
        'messages': ContactMessage.objects.count(),
        'unread': ContactMessage.objects.filter(read=False).count(),
    }
    recent_messages = ContactMessage.objects.order_by('-sent_at')[:5]
    return render(request, 'dashboard/home.html', {
        'stats': stats,
        'recent_messages': recent_messages,
    })


# ─── PROJECTS ────────────────────────────────────────────
@login_required(login_url='dashboard_login')
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'dashboard/project_list.html', {'projects': projects})


@login_required(login_url='dashboard_login')
def project_add(request):
    if request.method == 'POST':
        title       = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        github_url  = request.POST.get('github_url', '').strip()
        live_url    = request.POST.get('live_url', '').strip()
        tags        = request.POST.get('tags', '').strip()
        featured    = request.POST.get('featured') == 'on'
        order       = request.POST.get('order', 0)
        image       = request.FILES.get('image')

        if not all([title, description, github_url, tags]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'dashboard/project_form.html', {'action': 'Add'})

        project = Project.objects.create(
            title=title,
            description=description,
            github_url=github_url,
            live_url=live_url,
            tags=tags,
            featured=featured,
            order=order,
        )
        if image:
            project.image = image
            project.save()

        messages.success(request, f'Project "{title}" added successfully.')
        return redirect('dashboard_projects')

    return render(request, 'dashboard/project_form.html', {'action': 'Add'})


@login_required(login_url='dashboard_login')
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        project.title       = request.POST.get('title', '').strip()
        project.description = request.POST.get('description', '').strip()
        project.github_url  = request.POST.get('github_url', '').strip()
        project.live_url    = request.POST.get('live_url', '').strip()
        project.tags        = request.POST.get('tags', '').strip()
        project.featured    = request.POST.get('featured') == 'on'
        project.order       = request.POST.get('order', 0)

        if request.FILES.get('image'):
            project.image = request.FILES['image']

        project.save()
        messages.success(request, f'Project "{project.title}" updated.')
        return redirect('dashboard_projects')

    return render(request, 'dashboard/project_form.html', {
        'action': 'Edit',
        'project': project,
    })


@login_required(login_url='dashboard_login')
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        name = project.title
        project.delete()
        messages.success(request, f'Project "{name}" deleted.')
        return redirect('dashboard_projects')
    return render(request, 'dashboard/confirm_delete.html', {
        'item': project,
        'type': 'Project',
        'cancel_url': 'dashboard_projects',
    })


# ─── BLOG POSTS ──────────────────────────────────────────
@login_required(login_url='dashboard_login')
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'dashboard/post_list.html', {'posts': posts})


@login_required(login_url='dashboard_login')
def post_add(request):
    if request.method == 'POST':
        title     = request.POST.get('title', '').strip()
        excerpt   = request.POST.get('excerpt', '').strip()
        body      = request.POST.get('body', '').strip()
        published = request.POST.get('published') == 'on'
        image     = request.FILES.get('image')

        if not all([title, excerpt, body]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'dashboard/post_form.html', {'action': 'Add'})

        post = Post.objects.create(
            title=title,
            excerpt=excerpt,
            body=body,
            published=published,
        )
        if image:
            post.image = image
            post.save()

        messages.success(request, f'Post "{title}" added successfully.')
        return redirect('dashboard_posts')

    return render(request, 'dashboard/post_form.html', {'action': 'Add'})


@login_required(login_url='dashboard_login')
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        post.title     = request.POST.get('title', '').strip()
        post.excerpt   = request.POST.get('excerpt', '').strip()
        post.body      = request.POST.get('body', '').strip()
        post.published = request.POST.get('published') == 'on'

        if request.FILES.get('image'):
            post.image = request.FILES['image']

        post.save()
        messages.success(request, f'Post "{post.title}" updated.')
        return redirect('dashboard_posts')

    return render(request, 'dashboard/post_form.html', {
        'action': 'Edit',
        'post': post,
    })


@login_required(login_url='dashboard_login')
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        name = post.title
        post.delete()
        messages.success(request, f'Post "{name}" deleted.')
        return redirect('dashboard_posts')
    return render(request, 'dashboard/confirm_delete.html', {
        'item': post,
        'type': 'Blog Post',
        'cancel_url': 'dashboard_posts',
    })


# ─── MESSAGES ────────────────────────────────────────────
@login_required(login_url='dashboard_login')
def message_list(request):
    all_messages = ContactMessage.objects.all()
    return render(request, 'dashboard/message_list.html', {'messages': all_messages})


@login_required(login_url='dashboard_login')
def message_detail(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.read = True
    msg.save()
    return render(request, 'dashboard/message_detail.html', {'msg': msg})


@login_required(login_url='dashboard_login')
def message_delete(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        msg.delete()
        messages.success(request, 'Message deleted.')
        return redirect('dashboard_messages')
    return render(request, 'dashboard/confirm_delete.html', {
        'item': msg,
        'type': 'Message',
        'cancel_url': 'dashboard_messages',
    })