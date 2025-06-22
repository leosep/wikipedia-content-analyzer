# Analizador de Contenido de Wikipedia

Este proyecto consiste en una aplicación que permite buscar artículos en Wikipedia, analizarlos (conteo de palabras, palabras frecuentes, análisis de sentimiento) y guardar artículos con notas personalizadas en una base de datos. Está construido con un backend en FastAPI (Python) y un frontend en React (TypeScript).

## Documentación

### 1. Instrucciones de Configuración y Ejecución

Para configurar y ejecutar este proyecto en un entorno Windows (o cualquier otro sistema operativo compatible con Python y Node.js), sigue los siguientes pasos:

#### Requisitos Previos:
* Python 3.13 o superior
* Node.js y npm
* PostgreSQL

#### Configuración del Backend

1.  **Clonar el repositorio:**

2.  **Configurar el entorno virtual y las dependencias con Poetry:**
    ```bash
    pip install poetry
    poetry install
    ```
    
3.  **Configurar variables de entorno:**
    En el archivo `.env` en la raíz del directorio `backend` con las siguientes variables. 
    ```
    DATABASE_URL="postgresql+psycopg2://postgres:123456@localhost:5432/wikipedia_db"
    WIKIPEDIA_API_BASE_URL=[https://en.wikipedia.org/w/](https://en.wikipedia.org/w/)
    ```

4.  **Ejecutar migraciones de la base de datos con Alembic:**
    Asegúrate de que tu base de datos PostgreSQL esté corriendo antes de ejecutar las migraciones.
    ```bash
    poetry run alembic upgrade head
    ```
    Esto creará las tablas necesarias en tu base de datos.

5.  **Iniciar el servidor FastAPI con Uvicorn:**
    ```bash
    poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```

#### Configuración del Frontend

1.  **Navegar al directorio del frontend:**
    ```bash
    cd ../frontend 
    ```

2.  **Instalar dependencias de Node.js:**
    ```bash
    npm install
    ```

3.  **Configurar variables de entorno para el frontend:**
    En el archivo `.env` en la raíz del directorio `frontend` y define la URL base de tu API:
    ```
    VITE_API_BASE_URL=http://localhost:8000/api/v1
    ```

4.  **Iniciar la aplicación React:**
    ```bash
    npm run dev
    ```
    El frontend se ejecutará en `http://localhost:5174`.

### 2. Decisiones de Diseño y Arquitectura

El proyecto sigue una rquitectura cliente-servidor con un backend monolítico API y un frontend de una sola página (SPA).

* **Backend (Python/FastAPI):**
    * **FastAPI:** Elegido por su alto rendimiento y facilidad de uso.
    * **SQLAlchemy:** Utilizado como Object Relational Mapper (ORM) para interactuar con la base de datos.
    * **Alembic:** Gestiona las migraciones de la base de datos.
    * **TextBlob:** Se usa para el análisis de sentimiento de los resúmenes de los artículos de Wikipedia.
    * **Wikipedia-API:** Una biblioteca de Python para interactuar con la API de Wikipedia.
    * **Estructura de Archivos:** El backend está organizado lógicamente con directorios para `api` (endpoints), `core` (configuración), `database` (modelos y sesión), `crud` (operaciones de base de datos) y `services` (lógica de negocio externa, como la API de Wikipedia).

* **Frontend (React/TypeScript):**
    * **React:** Biblioteca de JavaScript para construir interfaces.
    * **TypeScript:** Mejora la robustez del código y facilitando el mantenimiento.
    * **Vite:** Un bundler rápido para el desarrollo frontend.

* **Base de Datos:**
    * **PostgreSQL:** Base de datos relacional.
    * **SQLite:** Opción para las pruebas unitarias.

### 3. Definición de los Endpoints de la API

La API se expone bajo el prefijo `/api/v1`.

#### Endpoints de Wikipedia (`/api/v1/wikipedia`)

Estos endpoints interactúan con la API externa de Wikipedia para buscar y obtener detalles de artículos.

* **`GET /api/v1/wikipedia/search`**
    * **Descripción:** Busca artículos en Wikipedia y devuelve una lista de artículos.
    * **Parámetros de consulta:**
        * `query` (string, requerido): La consulta de búsqueda de Wikipedia (mín. 1, máx. 100 caracteres).
        * `limit` (entero, opcional): Número máximo de resultados de búsqueda a devolver (1-50, por defecto 10).
    * **Ejemplo de respuesta (200 OK):**
        ```json
        [
            {
                "title": "Python",
                "pageid": 12345,
                "url": "[https://es.wikipedia.org/wiki/Python](https://es.wikipedia.org/wiki/Python)"
            }
        ]
        ```

* **`GET /api/v1/wikipedia/article/{title}`**
    * **Descripción:** Obtiene el contenido detallado de un artículo específico de Wikipedia por título, incluyendo resumen, conteo de palabras, palabras frecuentes y análisis de sentimiento.
    * **Parámetros de ruta:**
        * `title` (string, requerido): El título del artículo de Wikipedia.
    * **Ejemplo de respuesta (200 OK):**
        ```json
        {
            "title": "FastAPI",
            "summary": "FastAPI es un...",
            "full_url": "[https://es.wikipedia.org/wiki/FastAPI](https://es.wikipedia.org/wiki/FastAPI)",
            "content": "...",
            "references": ["referencia1", "referencia2"],
            "url": "[https://es.wikipedia.org/wiki/FastAPI](https://es.wikipedia.org/wiki/FastAPI)",
            "word_count": 500,
            "frequent_words": [["fastapi", 10], ["python", 8]],
            "sentiment_polarity": 0.5,
            "sentiment_subjectivity": 0.3,
            "sentiment_label": "positivo"
        }
        ```
    * **Errores:**
        * `404 Not Found`: Si el artículo no se encuentra.
        * `400 Bad Request`: Si el título corresponde a una página de desambiguación.

#### Endpoints de Artículos Guardados (`/api/v1/articles`)

Estos endpoints gestionan las operaciones CRUD para los artículos guardados en la base de datos.

* **`POST /api/v1/articles/`**
    * **Descripción:** Guarda un artículo de Wikipedia en la base de datos.
    * **Cuerpo de la solicitud (JSON):**
        ```json
        {
            "wikipedia_title": "Título del Artículo",
            "wikipedia_url": "[http://ejemplo.com/url_articulo](http://ejemplo.com/url_articulo)",
            "processed_summary": "Resumen procesado del artículo.",
            "word_count": 1500,
            "frequent_words": [["palabra1", 10], ["palabra2", 7]],
            "personal_notes": "Mis notas sobre este artículo.",
            "sentiment_polarity": 0.2,
            "sentiment_subjectivity": 0.4,
            "sentiment_label": "neutral",
            "user_id": 1
        }
        ```
    * **Ejemplo de respuesta (201 Created):** Retorna el objeto `ArticleInDB` del artículo creado.

* **`GET /api/v1/articles/{article_id}`**
    * **Descripción:** Recupera un artículo guardado por su ID.
    * **Parámetros de ruta:**
        * `article_id` (entero, requerido): El ID único del artículo.
    * **Ejemplo de respuesta (200 OK):** Retorna el objeto `ArticleInDB` del artículo.
    * **Errores:**
        * `404 Not Found`: Si el artículo no se encuentra.

* **`GET /api/v1/articles/`**
    * **Descripción:** Recupera una lista de artículos guardados con paginación.
    * **Parámetros de consulta:**
        * `skip` (entero, opcional): Número de artículos a omitir (por defecto 0).
        * `limit` (entero, opcional): Número máximo de artículos a devolver (1-100, por defecto 10).
    * **Ejemplo de respuesta (200 OK):** Retorna una lista de objetos `ArticleInDB`.

* **`PATCH /api/v1/articles/{article_id}`**
    * **Descripción:** Actualiza las notas personales de un artículo guardado.
    * **Parámetros de ruta:**
        * `article_id` (entero, requerido): El ID único del artículo.
    * **Cuerpo de la solicitud (JSON):**
        ```json
        {
            "personal_notes": "Nuevas notas actualizadas."
        }
        ```
    * **Ejemplo de respuesta (200 OK):** Retorna el objeto `ArticleInDB` actualizado.
    * **Errores:**
        * `404 Not Found`: Si el artículo no se encuentra.

* **`DELETE /api/v1/articles/{article_id}`**
    * **Descripción:** Elimina un artículo guardado de la base de datos.
    * **Parámetros de ruta:**
        * `article_id` (entero, requerido): El ID único del artículo.
    * **Ejemplo de respuesta (204 No Content):** No retorna contenido si la eliminación fue exitosa.
    * **Errores:**
        * `404 Not Found`: Si el artículo no se encuentra.
