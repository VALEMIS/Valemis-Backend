
from rest_framework import serializers
from .models import *
from django.apps import apps


# class PidanaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Pidana
#         fields = '__all__'
# class ClaimSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Claim
#         fields = '__all__'

def generate_serializer(model_name):
    models = apps.get_model('valemis', model_name)
    class AutoSerializer(serializers.ModelSerializer):
        class Meta:
            model = models
            fields = "__all__"
    return AutoSerializer