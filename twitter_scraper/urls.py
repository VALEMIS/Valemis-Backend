from django.urls import path
from . import views

urlpatterns = [
    # Health check
    path('health/', views.health_check, name='health-check'),
    
    # Account Analysis (scrape + analyze in one endpoint)
    path('analyze-account/', views.analyze_account, name='analyze-account'),
]
