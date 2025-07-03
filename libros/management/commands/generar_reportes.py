from django.db import models
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from libros.models import Libro, Autor, Genero, Calificacion
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

class Command(BaseCommand):
    help = 'Genera 10 reportes gráficos basados en los modelos de la biblioteca'

    def handle(self, *args, **kwargs):
        output_dir = "reporte_graficos"
        os.makedirs(output_dir, exist_ok=True)

        def save_plot(fig, filename):
            path = os.path.join(output_dir, filename)
            fig.savefig(path, bbox_inches='tight')
            plt.close(fig)

        # Preparar estilo Seaborn
        sns.set(style="whitegrid")

        # ===============================
        # 1. Libros por género
        df1 = pd.DataFrame(
            list(Genero.objects.annotate(cantidad=models.Count('libros')).values('nombre', 'cantidad'))
        )

        if not df1.empty:
            fig, ax = plt.subplots(figsize=(12, 6))
            barplot = sns.barplot(data=df1, x='nombre', y='cantidad', ax=ax, color='skyblue')

            ax.set_title('Libros por Género', fontsize=16)
            ax.set_xlabel('Género', fontsize=12)
            ax.set_ylabel('Cantidad de Libros', fontsize=12)

            plt.xticks(rotation=35, ha='right', fontsize=10)

            for p in barplot.patches:
                height = p.get_height()
                ax.annotate(f'{int(height)}',
                            (p.get_x() + p.get_width() / 2., height + 0.2),
                            ha='center', va='bottom', fontsize=9)

            fig.tight_layout()
            save_plot(fig, "1_libros_por_genero.png")


        # 2. Libros por autor (Top 10)
        df2 = pd.DataFrame(list(Autor.objects.annotate(cantidad=models.Count('libros')).values('nombre', 'cantidad')))
        df2 = df2.sort_values(by='cantidad', ascending=False).head(10)
        if not df2.empty:
            fig = plt.figure(figsize=(10, 6))
            sns.barplot(data=df2, y='nombre', x='cantidad').set_title('Top 10 Autores con Más Libros')
            save_plot(fig, "2_libros_por_autor.png")

        # 3. Promedio de calificación por libro
        df3 = pd.DataFrame(
            list(Libro.objects.annotate(prom=models.Avg('calificaciones__calificacion')).values('titulo', 'prom'))
        )
        df3 = df3.dropna().sort_values(by='prom', ascending=False).head(10)

        if not df3.empty:
            fig, ax = plt.subplots(figsize=(16, 8))

            barplot = sns.barplot(data=df3, x='titulo', y='prom', ax=ax, color='skyblue')
            ax.set_title('Promedio de Calificación por Libro', fontsize=16)
            ax.set_xlabel('Título', fontsize=12)
            ax.set_ylabel('Promedio', fontsize=12)

            # Rotar etiquetas del eje X correctamente sin advertencia
            plt.xticks(rotation=45, ha='right', fontsize=10)

            # Agregar etiquetas encima de las barras
            for p in barplot.patches:
                height = p.get_height()
                ax.annotate(f'{height:.1f}', (p.get_x() + p.get_width() / 2., height + 0.05),
                            ha='center', va='bottom', fontsize=9)

            fig.tight_layout()
            save_plot(fig, "3_promedio_calificacion_libro.png")




        # 4. Promedio de calificación por género
        df4 = pd.DataFrame(
            list(Genero.objects.annotate(prom=models.Avg('libros__calificaciones__calificacion'))
                .values('nombre', 'prom'))
        )
        df4 = df4.dropna()

        if not df4.empty:
            fig, ax = plt.subplots(figsize=(12, 6))  # Ampliar ancho para espacio de texto
            barplot = sns.barplot(data=df4, x='nombre', y='prom', ax=ax, color='cornflowerblue')

            ax.set_title('Promedio de Calificación por Género', fontsize=16)
            ax.set_xlabel('Género', fontsize=12)
            ax.set_ylabel('Promedio', fontsize=12)

            # Rotar etiquetas del eje x para evitar superposición
            plt.xticks(rotation=35, ha='right', fontsize=10)

            # Etiquetas encima de cada barra
            for p in barplot.patches:
                height = p.get_height()
                ax.annotate(f'{height:.1f}',
                            (p.get_x() + p.get_width() / 2., height + 0.05),
                            ha='center', va='bottom', fontsize=9)

            fig.tight_layout()
            save_plot(fig, "4_promedio_calificacion_genero.png")


        # 5. Calificaciones por usuario
        df5 = pd.DataFrame(
            list(User.objects.annotate(cantidad=models.Count('calificaciones'))
                .values('username', 'cantidad'))
        )
        df5 = df5[df5['cantidad'] > 0]

        if not df5.empty:
            fig, ax = plt.subplots(figsize=(12, 6))
            barplot = sns.barplot(data=df5, x='username', y='cantidad', ax=ax, color='lightskyblue')

            ax.set_title('Cantidad de Calificaciones por Usuario', fontsize=16)
            ax.set_xlabel('Usuario', fontsize=12)
            ax.set_ylabel('Cantidad', fontsize=12)

            plt.xticks(rotation=35, ha='right', fontsize=10)

            for p in barplot.patches:
                height = p.get_height()
                ax.annotate(f'{height}', 
                            (p.get_x() + p.get_width() / 2., height + 0.1),
                            ha='center', va='bottom', fontsize=9)

            fig.tight_layout()
            save_plot(fig, "5_calificaciones_por_usuario.png")


        # 6. Libros con más calificaciones
        df6 = pd.DataFrame(list(Libro.objects.annotate(cantidad=models.Count('calificaciones')).values('titulo', 'cantidad')))
        df6 = df6[df6['cantidad'] > 0].sort_values(by='cantidad', ascending=False).head(10)
        if not df6.empty:
            fig = plt.figure(figsize=(10, 6))
            sns.barplot(data=df6, y='titulo', x='cantidad').set_title('Libros con Más Calificaciones')
            save_plot(fig, "6_libros_mas_calificados.png")

        # 7. Autores con más libros calificados
        df7 = pd.DataFrame(
            list(
                Autor.objects
                .annotate(total=models.Count('libros__calificaciones'))
                .values('nombre', 'total')
            )
        )
        df7 = df7[df7['total'] > 0].sort_values(by='total', ascending=False).head(10)

        if not df7.empty:
            fig, ax = plt.subplots(figsize=(12, 6))
            barplot = sns.barplot(data=df7, x='nombre', y='total', ax=ax, color='skyblue')

            ax.set_title('Autores con Más Libros Calificados', fontsize=16)
            ax.set_xlabel('Autor', fontsize=12)
            ax.set_ylabel('Total de Calificaciones', fontsize=12)

            plt.xticks(rotation=35, ha='right', fontsize=10)

            for p in barplot.patches:
                height = p.get_height()
                ax.annotate(f'{height}',
                            (p.get_x() + p.get_width() / 2., height + 0.1),
                            ha='center', va='bottom', fontsize=9)

            fig.tight_layout()
            save_plot(fig, "7_autores_mas_calificados.png")


        # 8. Libros publicados por año
        df8 = pd.DataFrame(list(Libro.objects.values('fecha_publicacion')))
        if not df8.empty:
            df8['anio'] = pd.to_datetime(df8['fecha_publicacion']).dt.year
            df8 = df8.groupby('anio').size().reset_index(name='cantidad')
            fig = plt.figure(figsize=(10, 6))
            sns.lineplot(data=df8, x='anio', y='cantidad', marker='o').set_title('Libros Publicados por Año')
            save_plot(fig, "8_publicaciones_por_anio.png")

        # 9. Histograma de calificaciones
        df9 = pd.DataFrame(list(Calificacion.objects.values('calificacion')))
        if not df9.empty:
            fig = plt.figure(figsize=(10, 6))
            sns.histplot(df9['calificacion'], bins=5, kde=False).set_title('Distribución de Calificaciones')
            save_plot(fig, "9_histograma_calificaciones.png")

        # 10. Promedio de calificación por usuario
        df10 = pd.DataFrame(
            list(
                User.objects
                .annotate(prom=models.Avg('calificaciones__calificacion'))
                .values('username', 'prom')
            )
        )
        df10 = df10.dropna()

        if not df10.empty:
            fig, ax = plt.subplots(figsize=(12, 6))
            barplot = sns.barplot(data=df10, x='username', y='prom', ax=ax, color='skyblue')

            ax.set_title('Promedio de Calificación por Usuario', fontsize=16)
            ax.set_xlabel('Usuario', fontsize=12)
            ax.set_ylabel('Promedio', fontsize=12)

            plt.xticks(rotation=35, ha='right', fontsize=10)

            for p in barplot.patches:
                height = p.get_height()
                ax.annotate(f'{height:.1f}',
                            (p.get_x() + p.get_width() / 2., height + 0.05),
                            ha='center', va='bottom', fontsize=9)

            fig.tight_layout()
            save_plot(fig, "10_promedio_usuario.png")


        self.stdout.write(self.style.SUCCESS(f"✅ Reportes generados en la carpeta '{output_dir}'"))
