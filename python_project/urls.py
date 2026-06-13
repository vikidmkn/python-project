from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def server_error(request):
    return JsonResponse({'error': 'Internal server error.'}, status=500)


handler500 = server_error

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
]

