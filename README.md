# 📖 Biblioteca API RESTful

## Versiones de Herramientas

```text
Package                       Version
----------------------------- -----------
asgiref                       3.8.1
contourpy                     1.3.2
cycler                        0.12.1
Django                        5.2.4
djangorestframework           3.16.0
djangorestframework_simplejwt 5.5.0
fonttools                     4.58.4
Jinja2                        3.1.6
kiwisolver                    1.4.8
license                       0.1a3
MarkupSafe                    3.0.2
matplotlib                    3.10.3
numpy                         2.3.1
packaging                     25.0
pandas                        2.3.0
pillow                        11.3.0
pip                           24.3.1
psycopg2-binary               2.9.10
PyJWT                         2.9.0
pyparsing                     3.2.3
python-dateutil               2.9.0.post0
pytz                          2025.2
seaborn                       0.13.2
six                           1.17.0
sqlparse                      0.5.3
tzdata                        2025.2
Unidecode                     1.4.0
```

## Instalación del Entorno

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate   # Windows

# Instalar Django y dependencias
pip install django djangorestframework psycopg2 pandas matplotlib seaborn

# Crear proyecto y app
django-admin startproject biblioteca
cd biblioteca
python manage.py startapp libros

# Migraciones
python manage.py makemigrations
python manage.py migrate
```
## Configuración de la Base de Datos (PostgreSQL)
### Crear la base de datos y usuario
Ejecuta estos comandos en tu cliente SQL (como pgAdmin, DBeaver o consola):
```sql
CREATE DATABASE biblioteca;
CREATE USER biblioteca_user WITH PASSWORD 'biblioteca_pass';
GRANT ALL PRIVILEGES ON DATABASE biblioteca TO biblioteca_user;
```

Asegúrate de que el servidor PostgreSQL esté funcionando y el puerto por defecto (5432) esté habilitado.

### Configurar Django para usar PostgreSQL
Abre el archivo biblioteca/settings.py y reemplaza la sección DATABASES por:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'biblioteca',
        'USER': 'postgres',
        'PASSWORD': '123456789',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
### Aplicar migraciones
Una vez creada la base y configurado settings.py, ejecuta:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Descripción del Proyecto

Esta API RESTful permite:

- Registrar libros, autores, géneros y calificaciones de usuarios.
- Consultar y listar libros y autores.
- Generar reportes automáticos desde consola.
- Obtener recomendaciones de libros por género, según promedio de calificaciones.

El sistema usa Django REST Framework y una base de datos PostgreSQL.

## Prueba de la Aplicacion

### Registrar usuario
Endpoint:
```http
POST http://localhost:8000/api/registro/
```
En el body enviamos el JSon:
```json
{
  "username": "sofia",
  "email": "sofia@sofia.com",
  "password": "123456789"
}
```
![Image](https://github.com/user-attachments/assets/f24a8793-5405-47dc-bdc6-6a7c21751f9e)

### Login en la Aplicacion
Endpoint:
```http
POST http://localhost:8000/api/login/
```
En el body enviamos el JSon:
```json
{
  "username": "sofia",
  "password": "123456789"
}
```
![Image](https://github.com/user-attachments/assets/cc679ad1-508c-4820-b942-1401bed02066)

Este token de acceso (access) generado debe usarse en los headers de autenticación para consumir los demás endpoints protegidos.

### TOKEN
Para consumir los siguentes endpoints usamos el token generado.

Insertar el token en:
![Image](https://github.com/user-attachments/assets/4826a0c6-2c4e-4ef3-b0c7-27cca52aba8c)

### Listar todos los Libros
Endpoint:
```http
GET http://localhost:8000/api/libros/
```
Para listar todos los libros no se requiere pasar ningun body, entonces el resultado seria:

![Image](https://github.com/user-attachments/assets/e6eb9dd8-270b-43d9-87c2-2cc680e78360)

Codigo para este metodo:
```python
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
```

### Listar libro por ID:
Endpoint:
```http
GET http://localhost:8000/api/libros/1/
```
No es necesario enviar un body. Solo debes incluir el ID del libro al final del endpoint para obtener los detalles de un libro específico.

![Image](https://github.com/user-attachments/assets/77e0f92e-2388-49f1-bb4f-914e925e66e1)

Codigo para este metodo:
```python
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
```
### Insertar Libro
Endpoint:
```http
POST http://localhost:8000/api/libros/
```
En el body enviamos el JSon:
```json
{
  "titulo": "Libro Insertado",
  "autor": 1,
  "genero": 1,
  "fecha_publicacion": "2025-01-01",
  "isbn": "11111",
  "url": "http://post.com"
}
```
![Image](https://github.com/user-attachments/assets/582e76c2-d6b7-443c-b8ed-c891f43146d0)

Codigo para este metodo:
```python
def post(self, request):
        # Crea un nuevo libro
        serializer = LibroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### Actualizar
Endpoint:
```http
PUT http://localhost:8000/api/libros/50/
```
En el endpoint pasamos el id del libro a actualizar.

En el body enviamos el JSon:
```json
{
  "titulo": "Libro Insertado - Ahora Actualizado",
  "autor": 1,
  "genero": 1,
  "fecha_publicacion": "2025-02-02",
  "isbn": "22222",
  "url": "http://post2.com"
}
```
![Image](https://github.com/user-attachments/assets/0950a075-2323-4d7f-b0d5-96d4c522493c)

Codigo para este metodo:
```python
    def put(self, request, pk):
        # Actualiza un libro existente por ID
        libro = get_object_or_404(Libro, pk=pk)
        serializer = LibroSerializer(libro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### Eliminar
Endpoint:
```http
DELETE http://localhost:8000/api/libros/50/
```
En el endpoint pasamos el id del libro a eliminar, no es necesario enviar nada en el body.

![Image](https://github.com/user-attachments/assets/d5a44047-b82d-42b2-930f-041df20e7cb9)

Codigo para este metodo:
```python
def delete(self, request, pk):
        # Elimina un libro por ID
        libro = get_object_or_404(Libro, pk=pk)
        libro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

## Generación de Gráficos desde Consola
📂 Script: generar_reportes.py
Este script se encuentra en:
```bash
libros/management/commands/generar_reportes.py
```
Y permite generar automáticamente 10 reportes gráficos con datos obtenidos directamente desde la base de datos del sistema. El script hace uso de:

Pandas: para procesamiento de datos.

Seaborn y Matplotlib: para visualización de datos.

ORM de Django: para obtener los datos desde los modelos Libro, Autor, Genero, Calificacion y User.

Ejecución del Script
```bash
python manage.py generar_reportes
```
Al ejecutarlo, se genera una carpeta reporte_graficos con los siguientes gráficos en formato .png.

## Descripción de los Gráficos
### Libros por Género
📂 1_libros_por_genero.png

Muestra la cantidad total de libros registrados por cada género.

Es útil para ver en qué categorías hay mayor contenido.

![Image](https://github.com/user-attachments/assets/f7731213-5620-42b3-90c1-a3979f91496e)

### Libros por Autor (Top 10)
📂 2_libros_por_autor.png

Lista los 10 autores que más libros tienen registrados en el sistema.

Ideal para analizar la producción literaria de cada autor.

![Image](https://github.com/user-attachments/assets/eb441010-3760-4b35-a589-d895267ba82e)

### Promedio de Calificación por Libro
📂 3_promedio_calificacion_libro.png

Presenta los 10 libros mejor calificados según el promedio otorgado por los usuarios.

Permite identificar los libros mejor valorados.

![Image](https://github.com/user-attachments/assets/fb20cb0e-6e9a-452c-9030-bee874d94371)

### Promedio de Calificación por Género
📂 4_promedio_calificacion_genero.png

Calcula el promedio de calificaciones por cada género literario.

Útil para analizar cuál género tiene mejores valoraciones en general.

![Image](https://github.com/user-attachments/assets/708b43d1-7137-4877-a0b5-696c9665faa6)

### Calificaciones por Usuario
📂 5_calificaciones_por_usuario.png

Muestra cuántas calificaciones hizo cada usuario registrado.

Ayuda a visualizar la participación de los usuarios en el sistema.

![Image](https://github.com/user-attachments/assets/4ca79c29-4744-4f3a-b363-7c58d41a424b)

### Libros con Más Calificaciones
📂 6_libros_mas_calificados.png

Lista los libros que recibieron más calificaciones.

Permite ver cuáles obras son las más populares entre los lectores.

![Image](https://github.com/user-attachments/assets/214e0ef2-98ed-4493-845e-7332d508c92f)

### Autores con Más Libros Calificados
📂 7_autores_mas_calificados.png

Identifica a los autores cuyos libros recibieron más calificaciones.

Da una idea de qué autores generan mayor interacción.

![Image](https://github.com/user-attachments/assets/65166a0d-230f-48cc-8953-b7ff68b73640)

### Libros Publicados por Año
📂 8_publicaciones_por_anio.png

Gráfico de línea que muestra cuántos libros fueron publicados cada año.

Ideal para observar tendencias de publicación a lo largo del tiempo.

![Image](https://github.com/user-attachments/assets/e49ed695-8b8b-46e6-9385-d68f7bf9d0c4)

### Histograma de Calificaciones
📂 9_histograma_calificaciones.png

Muestra la distribución de calificaciones otorgadas (de 1 a 5).

Permite entender si los usuarios califican con más frecuencia de forma positiva o negativa.

![Image](https://github.com/user-attachments/assets/43d1565a-3df4-453d-bb79-942c76c35142)

### Promedio de Calificación por Usuario
📂 10_promedio_usuario.png

Visualiza el promedio de puntuación que cada usuario ha otorgado.

Útil para analizar qué usuarios son más exigentes o más generosos al calificar.

![Image](https://github.com/user-attachments/assets/ed963533-517b-4cc7-935a-081ac4d0cd20)


## Recomendaciones por Género
📂 Script: recomendar_por_genero.py
Este script se encuentra en:

```bash
libros/management/commands/recomendar_por_genero.py
```
### ¿Qué hace?
Este comando de consola permite recomendar libros en base a un género literario seleccionado, mostrando los libros mejor valorados (según promedio de calificaciones).

La búsqueda por género es flexible, lo que significa que:
- No distingue mayúsculas/minúsculas
- No requiere tildes (acentos)

Por ejemplo, los siguientes comandos producen el mismo resultado:

```bash
python manage.py recomendar_por_genero Programación
python manage.py recomendar_por_genero programacion
python manage.py recomendar_por_genero PROGRAMACION
```

### ¿Cómo funciona internamente?
- Se toma el nombre del género introducido como argumento.
- Se normaliza eliminando acentos y convirtiendo a minúsculas.
- Se busca un género en la base de datos que coincida con ese nombre normalizado.
- Si existe, se consultan los libros de ese género y se calcula su promedio de calificación.

Se muestran hasta 10 libros ordenados del mejor al peor promedio.

🧪 Ejemplo de uso
```bash
python manage.py recomendar_por_genero Programación
```

Resultado esperado:
![Image](https://github.com/user-attachments/assets/fb7e583c-87b1-4cc7-b60c-a4d1b8749dda)

Si no se encuentra el género, se muestra un mensaje de error:

```bash
❌ Género 'fantasia epica' no encontrado.
```

Y si el género existe, pero no hay libros con calificaciones:
```bash
⚠️ No se encontraron libros en el género 'Poesía' o no tienen calificaciones.
```


## Licencias

###  Licencias de las librerias usadas
```text
Package                       Version
----------------------------- -----------
asgiref                       3.8.1
contourpy                     1.3.2
cycler                        0.12.1
Django                        5.2.4
djangorestframework           3.16.0
djangorestframework_simplejwt 5.5.0
fonttools                     4.58.4
Jinja2                        3.1.6
kiwisolver                    1.4.8
license                       0.1a3
MarkupSafe                    3.0.2
matplotlib                    3.10.3
numpy                         2.3.1
packaging                     25.0
pandas                        2.3.0
pillow                        11.3.0
pip                           24.3.1
psycopg2-binary               2.9.10
PyJWT                         2.9.0
pyparsing                     3.2.3
python-dateutil               2.9.0.post0
pytz                          2025.2
seaborn                       0.13.2
six                           1.17.0
sqlparse                      0.5.3
tzdata                        2025.2
Unidecode                     1.4.0
```

---

© Proyecto educativo desarrollado para fines de evaluación y aprendizaje con licencia MIT.

