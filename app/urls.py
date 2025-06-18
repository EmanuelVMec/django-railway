from django.urls import path
from .views import predict_cafe

urlpatterns = [
    path('prediccion/', predict_cafe),
]