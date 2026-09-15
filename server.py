from wsgiref.simple_server import make_server
import json


tasks = []
next_id = 1


def application(environ, start_response):
    method = environ["REQUEST_METHOD"]
    path = environ["PATH_INFO"]

    # GET /tasks
    if method == "GET" and path == "/tasks":
        status = "200 OK"
        response = json.dumps(tasks).encode()

        headers = [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(response))),
        ]

        start_response(status, headers)
        return [response]

    # GET /tasks/{id}
    if method == "GET" and path.startswith("/tasks/"):
        partes = path.split("/")

        try:
            task_id = int(partes[2])
        except ValueError:
            status = "404 Not Found"
            response = json.dumps({"error": "Tarea no encontrada"}).encode()

            headers = [
                ("Content-Type", "application/json"),
                ("Content-Length", str(len(response))),
            ]

            start_response(status, headers)
            return [response]

        tarea_encontrada = None

        for t in tasks:
            if t["id"] == task_id:
                tarea_encontrada = t
                break

        if tarea_encontrada is None:
            status = "404 Not Found"
            response = json.dumps({"error": "Tarea no encontrada"}).encode()
        else:
            status = "200 OK"
            response = json.dumps(tarea_encontrada).encode()

        headers = [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(response))),
        ]

        start_response(status, headers)
        return [response]

    # POST /tasks
    if method == "POST" and path == "/tasks":
        global next_id

        content_length = int(environ.get("CONTENT_LENGTH", 0) or 0)
        body = environ["wsgi.input"].read(content_length)

        try:
            task_data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            status = "400 Bad Request"
            response = json.dumps({"error": "JSON invalido"}).encode()

            headers = [
                ("Content-Type", "application/json"),
                ("Content-Length", str(len(response))),
            ]

            start_response(status, headers)
            return [response]

        task = {
            "id": next_id
        }

        for clave in task_data:
            if clave != "id":
                task[clave] = task_data[clave]

        tasks.append(task)
        next_id += 1

        status = "201 Created"
        response = json.dumps(task).encode()

        headers = [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(response))),
        ]

        start_response(status, headers)
        return [response]

    # PATCH /tasks/{id}
    if method == "PATCH" and path.startswith("/tasks/"):
        partes = path.split("/")

        try:
            task_id = int(partes[2])
        except ValueError:
            status = "404 Not Found"
            response = json.dumps({"error": "Tarea no encontrada"}).encode()

            headers = [
                ("Content-Type", "application/json"),
                ("Content-Length", str(len(response))),
            ]

            start_response(status, headers)
            return [response]

        tarea_encontrada = None

        for t in tasks:
            if t["id"] == task_id:
                tarea_encontrada = t
                break

        if tarea_encontrada is None:
            status = "404 Not Found"
            response = json.dumps({"error": "Tarea no encontrada"}).encode()
        else:
            content_length = int(environ.get("CONTENT_LENGTH", 0) or 0)
            body = environ["wsgi.input"].read(content_length)

            try:
                cambios = json.loads(body) if body else {}
            except json.JSONDecodeError:
                status = "400 Bad Request"
                response = json.dumps({"error": "JSON invalido"}).encode()

                headers = [
                    ("Content-Type", "application/json"),
                    ("Content-Length", str(len(response))),
                ]

                start_response(status, headers)
                return [response]

            # PATCH modifica solamente los campos enviados
            for clave in cambios:
                if clave != "id":
                    tarea_encontrada[clave] = cambios[clave]

            status = "200 OK"
            response = json.dumps(tarea_encontrada).encode()

        headers = [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(response))),
        ]

        start_response(status, headers)
        return [response]

    # DELETE /tasks/{id}
    if method == "DELETE" and path.startswith("/tasks/"):
        partes = path.split("/")

        try:
            task_id = int(partes[2])
        except ValueError:
            status = "404 Not Found"
            response = json.dumps({"error": "Tarea no encontrada"}).encode()

            headers = [
                ("Content-Type", "application/json"),
                ("Content-Length", str(len(response))),
            ]

            start_response(status, headers)
            return [response]

        tarea_encontrada = None

        for t in tasks:
            if t["id"] == task_id:
                tarea_encontrada = t
                break

        if tarea_encontrada is None:
            status = "404 Not Found"
            response = json.dumps({"error": "Tarea no encontrada"}).encode()
        else:
            tasks.remove(tarea_encontrada)

            status = "200 OK"
            response = json.dumps({"mensaje": "Tarea eliminada"}).encode()

        headers = [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(response))),
        ]

        start_response(status, headers)
        return [response]

    # Ruta inexistente
    status = "404 Not Found"
    response = json.dumps({"error": "Not Found"}).encode()

    headers = [
        ("Content-Type", "application/json"),
        ("Content-Length", str(len(response))),
    ]

    start_response(status, headers)
    return [response]


# Iniciar servidor
server = make_server("localhost", 9292, application)

print("Servidor escuchando en http://localhost:9292")

server.serve_forever()