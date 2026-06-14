from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.shortcuts import render

def server_error(request):
    return JsonResponse({'error': 'Internal server error.'}, status=500)

def custom_404(request, exception):
    return render(request, 'tasks/404.html', status=404)

handler500 = server_error
handler404 = custom_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
]