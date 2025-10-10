from django.urls import path
from .views import SerticateListAPIView, SkillListAPIView, PortfolioListAPIView

urlpatterns = [
    path('serticates/', SerticateListAPIView.as_view(), name='serticate-list'),
    path('skills/', SkillListAPIView.as_view(), name='skill-list'),
    path('portfolios/', PortfolioListAPIView.as_view(), name='portfolio-list'),
]
