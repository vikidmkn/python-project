from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import login, logout
from django.db.models import Q
from .models import Task
from .serializers import TaskSerializer, RegisterSerializer, UserSerializer


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': f'Welcome to Forge, {user.username}!',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        from django.contrib.auth import authenticate
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({
                'message': f'Welcome back, {user.username}.',
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskListAPIView(APIView):
    def get(self, request):
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
            'priority': 'priority', 'created_at': 'created_at', '-created_at': '-created_at',
        }
        tasks = tasks.order_by(sort_map.get(sort_by, '-created_at'))
        all_tasks = Task.objects.filter(user=request.user)
        total = all_tasks.count()
        completed_count = all_tasks.filter(status='completed').count()
        pending_count = all_tasks.filter(status='pending').count()
        overdue = sum(1 for t in all_tasks.filter(status='pending') if t.is_overdue())
        completion_pct = round((completed_count / total * 100)) if total > 0 else 0
        serializer = TaskSerializer(tasks, many=True)
        return Response({
            'tasks': serializer.data,
            'stats': {
                'total': total,
                'completed': completed_count,
                'pending': pending_count,
                'overdue': overdue,
                'completion_pct': completion_pct,
            }
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailAPIView(APIView):
    def get_object(self, pk, user):
        try:
            return Task.objects.get(pk=pk, user=user)
        except Task.DoesNotExist:
            return None

    def get(self, request, pk):
        task = self.get_object(pk, request.user)
        if not task:
            return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        task = self.get_object(pk, request.user)
        if not task:
            return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        task = self.get_object(pk, request.user)
        if not task:
            return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = self.get_object(pk, request.user)
        if not task:
            return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskStatsAPIView(APIView):
    def get(self, request):
        all_tasks = Task.objects.filter(user=request.user)
        total = all_tasks.count()
        completed = all_tasks.filter(status='completed').count()
        pending = all_tasks.filter(status='pending').count()
        overdue = sum(1 for t in all_tasks.filter(status='pending') if t.is_overdue())
        completion_pct = round((completed / total * 100)) if total > 0 else 0
        return Response({
            'total': total,
            'completed': completed,
            'pending': pending,
            'overdue': overdue,
            'completion_pct': completion_pct,
        }, status=status.HTTP_200_OK)