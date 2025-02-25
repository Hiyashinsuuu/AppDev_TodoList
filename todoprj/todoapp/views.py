from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import todo
from .forms import TodoForm
from .serializers import TodoSerializer, UserRegistrationSerializer, UserLoginSerializer
from django.contrib.auth.decorators import login_required

class UserRegistrationView(viewsets.ViewSet):
    def create(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User  created successfully.'}, status=201)
        return Response(serializer.errors, status=400)

class UserLoginView(viewsets.ViewSet):
    def create(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return Response({'message': 'Login successful.'}, status=200)
            return Response({'error': 'Invalid credentials.'}, status=400)
        return Response(serializer.errors, status=400)

class TodoViewSet(viewsets.ModelViewSet):
    queryset = todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return todo.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'], url_path='toggle-status')
    def toggle_status(self, request, pk=None):
        todo_item = self.get_object()
        todo_item.status = not todo_item.status
        todo_item.save()
        return Response({'status': 'status updated'})

    @action(detail=True, methods=['delete'], url_path='delete')
    def delete_task(self, request, pk=None):
        todo_item = self.get_object()
        todo_item.delete()
        return Response({'status': 'task deleted'})

@login_required
def home(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        new_todo = todo(user=request.user, todo_name=task)
        new_todo.save()

    all_todos = todo.objects.filter(user=request.user)
    context = {
        'todos': all_todos
    }
    return render(request, 'todoapp/todo.html', context)

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

def LogoutView(request):
    logout(request)
    return redirect('login')