from django.urls import path, include
from rest_framework import routers
from .views import *
from . import views
from django.apps import apps


router = routers.DefaultRouter()

app_models = apps.get_app_config("valemis").get_models()

for model in app_models:
    name = model.__name__.lower()
    router.register(name, generate_viewset(model.__name__))

urlpatterns = [
    path("", include(router.urls)),      # <-- router ikut masuk
    path("analyze/", views.api_analyze, name="analyze"),
    path("tes/", views.tes, name="tes"),
]
