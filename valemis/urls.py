from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path("analyze/", views.api_analyze,name="analyze"),
    path("tes/",views.tes,name="tes")
]
