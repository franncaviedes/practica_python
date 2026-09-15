# Servidor HTTP para gestión de tareas

## Objetivo

Desarrollar un servidor HTTP utilizando Python y `wsgiref.simple_server`, sin utilizar frameworks como Flask.

El servidor permite administrar una lista de tareas almacenada en memoria y funciona localmente en:

`http://localhost:9292`

## Operaciones disponibles

El servidor permite trabajar con las tareas mediante los siguientes métodos HTTP:

* **GET `/tasks`**: muestra todas las tareas y responde con `200 OK`.

* **GET `/tasks/{id}`**: busca una tarea específica. Si existe, devuelve `200 OK`; si no existe, devuelve `404 Not Found`.

* **POST `/tasks`**: crea una nueva tarea utilizando los datos enviados en formato JSON y responde con `201 Created`.

* **PATCH `/tasks/{id}`**: modifica solamente los campos enviados de una tarea existente. Los demás datos se mantienen sin cambios. Devuelve `200 OK` o `404 Not Found`.

* **DELETE `/tasks/{id}`**: elimina una tarea. Si existe, responde con `200 OK`; si no existe, devuelve `404 Not Found`.

## Comportamiento de cada método

### GET — Consultar

GET se utiliza para obtener información y no modifica las tareas.

Por ejemplo:

`GET /tasks/1`

Muestra la información de la tarea que tiene el ID `1`.

Si se realiza nuevamente la misma consulta y la tarea no fue modificada, el resultado será el mismo.

### POST — Crear

POST se utiliza para crear una tarea nueva.

Por ejemplo:

`POST /tasks`

enviando:

```json
{
  "title": "Comprar pan"
}
```

Cada vez que se realiza un POST se crea una nueva tarea y se le asigna un ID diferente.

Por eso, **POST no es idempotente**: si se envía la misma solicitud dos veces, se crean dos tareas diferentes.

### PATCH — Modificar parcialmente

PATCH permite modificar solamente los datos que se envían.

Por ejemplo:

`PATCH /tasks/1`

enviando:

```json
{
  "title": "Comprar leche"
}
```

En este caso solamente se modifica el título de la tarea. Los demás datos permanecen iguales.

### DELETE — Eliminar

DELETE se utiliza para eliminar una tarea.

Por ejemplo:

`DELETE /tasks/1`

elimina la tarea con ID `1`.

Después de eliminarla, si se realiza:

`GET /tasks/1`

el servidor responde:

`404 Not Found`

porque la tarea ya no existe.

## Manejo de datos

Las solicitudes y respuestas utilizan formato JSON.

Se utiliza:

* `json.loads()` para leer y convertir los datos JSON recibidos.
* `json.dumps()` para convertir los datos y generar las respuestas.

Las respuestas del servidor incluyen:

`Content-Type: application/json`

## Archivo

Todo el servidor se encuentra en un único archivo:

`server.py`

## Pruebas

Las pruebas se realizaron utilizando `curl`.

Se comprobó:

1. Obtener todas las tareas.
2. Crear una tarea.
3. Consultar una tarea por su ID.
4. Modificar parcialmente una tarea con PATCH.
5. Eliminar una tarea con DELETE.
6. Consultar nuevamente la tarea eliminada y comprobar que devuelve `404 Not Found`.

La evidencia de las pruebas se encuentra en:

`tp_ingenieria.txt`
