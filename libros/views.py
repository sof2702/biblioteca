from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Libro, Autor, Genero, Calificacion
from .serializers import LibroSerializer, AutorSerializer, GeneroSerializer, CalificacionSerializer
from django.shortcuts import get_object_or_404


class LibroAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated] #Solo los usuarios autenticados pueden acceder

    def get(self, request, pk=None):
        # Si viene un ID (pk), devuelve el libro específico
        if pk:
            libro = get_object_or_404(Libro, pk=pk)
            serializer = LibroSerializer(libro)
            return Response(serializer.data)
        else:
            # Si no hay ID, devuelve todos los libros
            libros = Libro.objects.all()
            serializer = LibroSerializer(libros, many=True)
            return Response(serializer.data)

    def post(self, request):
        # Crea un nuevo libro
        serializer = LibroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        # Actualiza un libro existente por ID
        libro = get_object_or_404(Libro, pk=pk)
        serializer = LibroSerializer(libro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Elimina un libro por ID
        libro = get_object_or_404(Libro, pk=pk)
        libro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class AutorAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, pk=None):
        if pk:
            autor = get_object_or_404(Autor, pk=pk)
            serializer = AutorSerializer(autor)
            return Response(serializer.data)
        else:
            autores = Autor.objects.all()
            serializer = AutorSerializer(autores, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = AutorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        autor = get_object_or_404(Autor, pk=pk)
        serializer = AutorSerializer(autor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        autor = get_object_or_404(Autor, pk=pk)
        autor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class GeneroAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, pk=None):
        if pk:
            genero = get_object_or_404(Genero, pk=pk)
            serializer = GeneroSerializer(genero)
            return Response(serializer.data)
        else:
            generos = Genero.objects.all()
            serializer = GeneroSerializer(generos, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = GeneroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        genero = get_object_or_404(Genero, pk=pk)
        serializer = GeneroSerializer(genero, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        genero = get_object_or_404(Genero, pk=pk)
        genero.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class CalificacionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            calificacion = get_object_or_404(Calificacion, pk=pk, usuario=request.user)
            serializer = CalificacionSerializer(calificacion)
            return Response(serializer.data)
        else:
            calificaciones = Calificacion.objects.filter(usuario=request.user)
            serializer = CalificacionSerializer(calificaciones, many=True)
            return Response(serializer.data)

    def post(self, request):
        # Crea una calificación nueva asociada al usuario autenticado
        serializer = CalificacionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        calificacion = get_object_or_404(Calificacion, pk=pk, usuario=request.user)
        serializer = CalificacionSerializer(calificacion, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        calificacion = get_object_or_404(Calificacion, pk=pk, usuario=request.user)
        calificacion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)