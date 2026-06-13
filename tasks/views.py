from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Task
from .forms import RegisterForm, LoginForm, TaskForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to Forge, {user.username}!')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'tasks/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}.')
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'tasks/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been signed out.')
    return redirect('login')

@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)
    query = request.GET.get('q', '')
    if query:
        tasks = tasks.filter(Q(title__icontains=query) | Q(description__icontains=query))
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    sort_by = request.GET.get('sort', '-created_at')
    sort_map = {
        'deadline': 'deadline', '-deadline': '-deadline',
        'priority': 'priority', '-priority': '-priority',
        'created_at': 'created_at', '-created_at': '-created_at',
    }
    tasks = tasks.order_by(sort_map.get(sort_by, '-created_at'))
    all_tasks = Task.objects.filter(user=request.user)
    total = all_tasks.count()
    completed = all_tasks.filter(status='completed').count()
    pending = all_tasks.filter(status='pending').count()
    overdue = sum(1 for t in all_tasks.filter(status='pending') if t.is_overdue())
    completion_pct = round((completed / total * 100)) if total > 0 else 0
    context = {
        'tasks': tasks, 'total': total, 'completed': completed,
        'pending': pending, 'overdue': overdue, 'completion_pct': completion_pct,
        'query': query, 'status_filter': status_filter,
        'priority_filter': priority_filter, 'sort_by': sort_by,
    }
    return render(request, 'tasks/dashboard.html', context)


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, f'Task "{task.title}" created.')
            return redirect('dashboard')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Create'})


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f'Task "{task.title}" updated.')
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Edit', 'task': task})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        title = task.title
        task.delete()
        messages.success(request, f'Task "{title}" deleted.')
        return redirect('dashboard')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


@login_required
def task_toggle(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.status = 'completed' if task.status == 'pending' else 'pending'
        task.save()
        return JsonResponse({'status': task.status, 'label': task.get_status_display()})
    return JsonResponse({'error': 'Invalid method'}, status=405)