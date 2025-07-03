from django.urls import path
from .views import LibroAPIView, AutorAPIView, GeneroAPIView, CalificacionAPIView

urlpatterns = [
    # 📚 Libros
    path('libros/', LibroAPIView.as_view(), name='libros-list-create'),
    path('libros/<int:pk>/', LibroAPIView.as_view(), name='libros-detail'),

    # 👨‍💼 Autores
    path('autores/', AutorAPIView.as_view(), name='autores-list-create'),
    path('autores/<int:pk>/', AutorAPIView.as_view(), name='autores-detail'),

    # 🏷️ Géneros
    path('generos/', GeneroAPIView.as_view(), name='generos-list-create'),
    path('generos/<int:pk>/', GeneroAPIView.as_view(), name='generos-detail'),

    # ⭐ Calificaciones 
    path('calificaciones/', CalificacionAPIView.as_view(), name='calificaciones-list-create'),
    path('calificaciones/<int:pk>/', CalificacionAPIView.as_view(), name='calificaciones-detail'),
]
