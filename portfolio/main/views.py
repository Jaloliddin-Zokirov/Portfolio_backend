from rest_framework.generics import ListAPIView
from .models import Sertificate, Skill, Portfolio
from rest_framework import serializers
from .models import Sertificate, Skill, Portfolio


class SerticateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sertificate
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = '__all__'


class SerticateListAPIView(ListAPIView):
    queryset = Sertificate.objects.all()
    serializer_class = SerticateSerializer


class SkillListAPIView(ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class PortfolioListAPIView(ListAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
