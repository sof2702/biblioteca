from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import registro_view

urlpatterns = [
    path('registro/', registro_view, name='registrarse'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
