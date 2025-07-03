from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from libros.models import Libro, Genero, Calificacion
from django.db.models import Count, Avg, Q

class Command(BaseCommand):
    help = 'Recomienda libros al usuario según sus géneros más calificados'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Nombre de usuario para generar recomendaciones')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"❌ Usuario '{username}' no encontrado."))
            return

        # 1. Encontrar los géneros más calificados por el usuario
        generos_preferidos = (
            Genero.objects
            .filter(libros__calificaciones__usuario=user)
            .annotate(total=Count('libros__calificaciones'))
            .order_by('-total')
        )

        if not generos_preferidos.exists():
            self.stdout.write(self.style.WARNING(f"⚠️ El usuario '{username}' no tiene calificaciones registradas."))
            return

        genero_top = generos_preferidos.first()
        self.stdout.write(self.style.SUCCESS(f"📚 Género preferido de {username}: {genero_top.nombre}"))

        # 2. Obtener libros del género más calificado, que aún no calificó
        libros_recomendados = (
            Libro.objects
            .filter(genero=genero_top)
            .exclude(calificaciones__usuario=user)
            .annotate(promedio=Avg('calificaciones__calificacion'))
            .order_by('-promedio')[:10]
        )

        if libros_recomendados:
            self.stdout.write("\n🔝 Recomendaciones:")
            for libro in libros_recomendados:
                self.stdout.write(f"- {libro.titulo} (Autor: {libro.autor.nombre}) → Promedio: {libro.promedio:.1f}" if libro.promedio else f"- {libro.titulo} (sin calificaciones aún)")
        else:
            self.stdout.write(self.style.WARNING("⚠️ No se encontraron libros recomendables en este género."))
