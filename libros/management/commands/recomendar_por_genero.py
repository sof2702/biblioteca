from django.core.management.base import BaseCommand
from libros.models import Libro, Genero
from django.db.models import Avg
from unidecode import unidecode  # para eliminar tildes

class Command(BaseCommand):
    help = 'Sugiere libros por género seleccionado, ordenados por mejor valoración'

    def add_arguments(self, parser):
        parser.add_argument('genero', nargs='+', type=str, help='Nombre del género')

    def handle(self, *args, **kwargs):
        genero_input = ' '.join(kwargs['genero'])
        genero_input_normalizado = unidecode(genero_input).lower()

        # Buscar género de forma robusta
        genero = None
        for g in Genero.objects.all():
            if unidecode(g.nombre).lower() == genero_input_normalizado:
                genero = g
                break

        if not genero:
            self.stdout.write(self.style.ERROR(f"❌ Género '{genero_input}' no encontrado."))
            return

        libros = (
            Libro.objects
            .filter(genero=genero)
            .annotate(promedio=Avg('calificaciones__calificacion'))
            .order_by('-promedio')[:10]
        )

        if libros.exists():
            self.stdout.write(self.style.SUCCESS(f"\n📚 Top libros en el género '{genero.nombre}':\n"))
            for libro in libros:
                promedio = f"{libro.promedio:.1f}" if libro.promedio is not None else "Sin calificaciones"
                self.stdout.write(f"- {libro.titulo} (Autor: {libro.autor.nombre}) → Promedio: {promedio}")
        else:
            self.stdout.write(self.style.WARNING(f"⚠️ No se encontraron libros en el género '{genero.nombre}' o no tienen calificaciones."))
