"""
URL configuration for valemis_backend project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        'message': 'Valemis Backend API',
        'version': '1.0.0',
        'endpoints': {
            'admin': '/admin/',
            'twitter_scraper': '/api/twitter/',
            'sentiment_analysis': '/api/sentiment/',
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/twitter/', include('twitter_scraper.urls')),
]
