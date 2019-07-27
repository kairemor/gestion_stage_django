from rest_framework import serializers
from .models import Enterprise, Convention
from accounts.serializers import StudentSerializer, ProjSerializer, FramerSerializer


# THe serializer class allow to fromat the retrieve data in a JSON format
class EnterpriseSerializers(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)
    projects = ProjSerializer(many=True, read_only=True)
    framers = FramerSerializer(many=True, read_only=True)

    class Meta:
        model = Enterprise
        fields = '__all__'


class ConventionSerializer(serializers.ModelSerializer):
    enterprise = EnterpriseSerializers(many=False, read_only=True)

    class Meta:
        model = Convention
        fields = '__all__'
