## Construcción de un servidor HTTP en Python

Desarrollar un servidor HTTP utilizando únicamente `wsgiref.simple_server`, sin utilizar frameworks como Flask.

El servidor deberá manejar una lista de tareas almacenada en memoria y permitir realizar las operaciones básicas mediante los principales métodos HTTP.

### Endpoints requeridos

* **GET `/tasks`** → Obtener y mostrar todas las tareas. Debe responder con `200 OK`.
* **GET `/tasks/{id}`** → Consultar una tarea específica. Debe devolver `200 OK` si existe o `404 Not Found` si no se encuentra.
* **POST `/tasks`** → Agregar una nueva tarea utilizando los datos enviados en formato JSON. Debe responder con `201 Created`.
* **PATCH `/tasks/{id}`** → Actualizar únicamente los campos enviados de una tarea existente. Debe devolver `200 OK` o `404 Not Found` si la tarea no existe.
* **DELETE `/tasks/{id}`** → Eliminar una tarea determinada. Debe responder con `200 OK` o `204 No Content` si se elimina correctamente, y `404 Not Found` si no existe.

Todo el desarrollo deberá encontrarse en un único archivo llamado `server.py`.

El servidor deberá ejecutarse localmente en:

`http://localhost:9292`

### Manejo de datos

Las solicitudes y respuestas deberán utilizar exclusivamente formato JSON.

Para procesar los datos recibidos se deberá utilizar:

* `json.loads()` para convertir el JSON recibido.
* `json.dumps()` para generar las respuestas.

Todas las respuestas deberán incluir el siguiente encabezado:

`Content-Type: application/json`

También se deberán utilizar correctamente los códigos de estado HTTP correspondientes a cada operación.

Es importante que **PATCH funcione como una actualización parcial**. Es decir, solamente deberá modificar los atributos que se envíen en la solicitud y conservar sin cambios los demás datos de la tarea.

### Pruebas

Una vez terminado el servidor, se deberán realizar pruebas utilizando `curl` o el script `demo-verbos-http.sh`.

Las pruebas deberán guardarse como evidencia en un archivo llamado, por ejemplo:

`evidencia.txt`

Entre las pruebas realizadas deberá demostrarse que una tarea puede ser creada, consultada, modificada y finalmente eliminada.

Además, se deberá comprobar específicamente que, después de realizar un `DELETE`, al intentar consultar nuevamente esa misma tarea mediante `GET`, el servidor responda con:

`404 Not Found`

### Comportamiento de cada método HTTP

**GET – Consultar**

GET solamente permite obtener información. No debe realizar modificaciones en el servidor.

Si se ejecuta varias veces la misma consulta, el resultado deberá mantenerse igual mientras no se haya realizado otra operación que modifique los datos.

Ejemplo:

`GET /tasks/1`

→ Muestra la información correspondiente a la tarea con ID `1`.

---

**POST – Crear**

POST se utiliza para incorporar una nueva tarea.

Cada vez que se realiza una solicitud POST se debe generar un nuevo recurso, por lo que repetir la misma solicitud dará como resultado nuevas tareas con identificadores diferentes.

Ejemplo:

`POST /tasks`

```json
{"title": "Comprar pan"}
```

Si esta operación se realiza dos veces, deberán existir dos tareas independientes, cada una con su propio `id`.

---

**PATCH – Actualizar parcialmente**

PATCH permite modificar solamente determinados datos de una tarea existente.

Los campos que no sean enviados en la solicitud deberán conservar exactamente su valor anterior.

Ejemplo:

`PATCH /tasks/1`

```json
{"done": true}
```

En este caso, la tarea `1` queda marcada como completada, pero el resto de sus datos permanece sin modificaciones.

Si se vuelve a enviar exactamente el mismo PATCH, la tarea continuará marcada como completada y no se deberán producir cambios adicionales.

---

**DELETE – Eliminar**

DELETE se utiliza para quitar una tarea de la lista.

Ejemplo:

`DELETE /tasks/1`

Luego de ejecutarlo, la tarea `1` ya no deberá existir.

Si se intenta ejecutar nuevamente un DELETE sobre esa misma tarea, el recurso continuará sin existir y el servidor deberá responder indicando que no fue encontrado, por ejemplo con:

`404 Not Found`