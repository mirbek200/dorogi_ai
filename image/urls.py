from django.urls import path
from .views import RoadImageAPIView

urlpatterns = [
    path('road-image/', RoadImageAPIView.as_view()),
]
