from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import todo
from django.contrib.auth.decorators import login_required
from .forms import TodoForm
import re

# Create your views here.

@login_required
def edit_task(request, id):
    task = get_object_or_404(todo, id=id)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('home-page')
    else:
        form = TodoForm(instance=task)
    return render(request, 'todoapp/edit_task.html', {'form': form})


@login_required
def home(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        new_todo = todo(user=request.user, todo_name=task)
        new_todo.save()

    all_todos = todo.objects.filter(user = request.user)
    context = {
        'todos': all_todos
    }
    return render(request, 'todoapp/todo.html', context) 

def register(request):
    if request.user.is_authenticated:
        return redirect('home-page')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        special_characters = r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?`~]"

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        elif not re.search(r'[A-Z]', password):
            messages.error(request, 'Password must contain at least one uppercase letter.')
        elif not re.search(r'[a-z]', password):
            messages.error(request, 'Password must contain at least one lowercase letter.')
        elif not re.search(r'\d', password):
            messages.error(request, 'Password must contain at least one number.')
        elif not re.search(special_characters, password):
            messages.error(request, 'Password must contain at least one special character.')
        else:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Error! Username already exists.')
                return render(request, 'todoapp/register.html', {'email': email})
            else:
                new_user = User.objects.create_user(username=username, email=email, password=password)
                new_user.save()
                messages.success(request, 'User created successfully. You can now log in.')
                return redirect('login')

        return redirect('register')

    return render(request, 'todoapp/register.html', {})

def LogoutView(request):
    logout(request)
    return redirect('login')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')

        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect('home-page')
        else:
            messages.error(request, 'Error! Wrong user details or user does not exist.')
            return redirect('login')

    return render(request, 'todoapp/login.html', {})

@login_required
def DeleteTask(request, name):
    get_todo = todo.objects.get(user=request.user, todo_name=name)
    get_todo.delete()
    return redirect('home-page')

@login_required
def Update(request, name):
    get_todo = todo.objects.get(user=request.user, todo_name=name)
    get_todo.status = not get_todo.status
    get_todo.save()
    return redirect('home-page')
