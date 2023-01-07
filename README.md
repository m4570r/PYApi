# PYApi
## Resumen
  > Esta aplicación es un servidor web que se conecta a una base de datos MySQL y permite realizar operaciones CRUD en una tabla de usuarios a través de solicitudes HTTP.

La aplicación que se presenta es un servidor web escrito en Python que utiliza el módulo http.server de la biblioteca estándar de Python para gestionar las solicitudes HTTP. El servidor web se conecta a una base de datos MySQL y permite realizar operaciones CRUD (crear, leer, actualizar y eliminar) en una tabla de usuarios.

## Manejo de solicitudes

Cuando se envía una solicitud GET al servidor, se pueden realizar dos acciones distintas. Si se envía la solicitud a la ruta '/version', el servidor devuelve un objeto JSON con la información de la versión de la API. Si no se proporcionan parámetros de búsqueda, el servidor devuelve una lista de todos los usuarios de la tabla. Si se proporcionan parámetros de búsqueda, el servidor devuelve una lista filtrada de usuarios según esos parámetros.

Cuando se envía una solicitud POST al servidor, se interpreta el cuerpo de la solicitud como un objeto JSON con los datos de un nuevo usuario. El servidor inserta este usuario en la tabla y devuelve el ID del registro insertado junto con los demás campos del usuario en la respuesta.

Cuando se envía una solicitud PUT al servidor, se interpreta el cuerpo de la solicitud como un objeto JSON con los datos actualizados de un usuario. El servidor actualiza el usuario correspondiente en la tabla y devuelve el ID del registro actualizado junto con los demás campos del usuario en la respuesta.

Cuando se envía una solicitud DELETE al servidor, se interpreta el cuerpo de la solicitud como un objeto JSON con el ID del usuario que se debe eliminar. El servidor elimina el usuario correspondiente de la tabla y devuelve el ID del registro eliminado en la respuesta.

## Uso de la clase RequestHandler
La aplicación también incluye una clase llamada RequestHandler, que hereda de http.server.BaseHTTPRequestHandler y se encarga de manejar las solicitudes HTTP. Esta clase sobrescribe varios métodos para manejar las distintas operaciones CRUD.

Por ejemplo, el método do_GET se ejecuta cuando se envía una solicitud GET al servidor. Este método interpreta la URL de la solicitud y los parámetros de búsqueda, y llama a la base de datos para obtener la información necesaria. Luego, el método devuelve la respuesta al cliente a través de un objeto JSON.

Los métodos do_POST, do_PUT y do_DELETE funcionan de manera similar, pero se ejecutan cuando se envían solicitudes POST, PUT y DELETE, respectivamente. Estos métodos interpretan el cuerpo de la solicitud y realizan las operaciones adecuadas en la base de datos.

## Requisitos
Python 3.x
El módulo mysql.connector para Python
## Instalación
Instala Python 3.x en tu sistema.
Instala el módulo mysql.connector ejecutando
```
pip install mysql-connector-python.
```
## Configuración
Crea una base de datos MySQL y una tabla de usuarios con las siguientes columnas:
```
id (INT, AUTO_INCREMENT)
nombre (VARCHAR)
edad (INT)
```
Abre el archivo app.py y modifica las siguientes líneas con los datos de tu base de datos:
```
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='sistema'
)
```
Reemplaza 'localhost' por la dirección del servidor MySQL, 'root' por el nombre de usuario y '' por la contraseña. Reemplaza 'sistema' por el nombre de la base de datos que creaste.
## Ejecución
Abre una consola en la carpeta donde se encuentra el archivo app.py.
Ejecuta el servidor con python app.py.
El servidor estará escuchando en el puerto 8000. Puedes enviarle solicitudes HTTP desde tu navegador o cualquier otra herramienta de cliente HTTP.
## Solicitudes HTTP
El servidor soporta las siguientes operaciones CRUD:

### Crear usuario (POST)
```
POST http://localhost:8000
Content-Type: application/json

{
  "nombre": "Juan",
  "edad": 30
}
```
### Leer usuarios (GET)
```
GET http://localhost:8000
```
### Leer usuario por ID (GET)
```
GET http://localhost:8000?id=1
```
### Leer usuarios por nombre (GET)
```
GET http://localhost:8000?nombre=Juan
Actualizar usuario (PUT)
```
PUT http://localhost:8000
Content-Type: application/json

{
  "id": 1,
  "nombre": "Juan",
  "edad": 31
}
```
### Eliminar usuario (DELETE)
```
DELETE http://localhost:8000
Content-Type: application/json

{
  "id": 1
}
```
## Respuestas del servidor
El servidor devuelve las siguientes respuestas a las solicitudes HTTP:

### Crear usuario (POST)
```
HTTP/1.0 200 OK
Content-Type: application/json

{
  "id": 1,
  "nombre": "Juan",
  "edad": 30
}
```
### Leer usuarios (GET)
```
HTTP/1.0 200 OK
Content-Type: application/json

[
  {
    "id": 1,
    "nombre": "Juan",
    "edad": 30
  },
  {
    "id": 2,
    "nombre": "Ana",
    "edad": 25
  }
]
```
### Leer usuario por ID (GET)
```
HTTP/1.0 200 OK
Content-Type: application/json

[
  {
    "id": 1,
    "nombre": "Juan",
    "edad": 30
  }
]
```
### Leer usuarios por nombre (GET)
```
HTTP/1.0 200 OK
Content-Type: application/json

[
  {
    "id": 1,
    "nombre": "Juan",
    "edad": 30
  }
]
```
### Actualizar usuario (PUT)
```
HTTP/1.0 200 OK
Content-Type: application/json

{
  "id": 1,
  "nombre": "Juan",
  "edad": 31
}
```
### Eliminar usuario (DELETE)
```
HTTP/1.0 200 OK
Content-Type: application/json

{
  "id": 1
}
```
### Errores
En caso de que ocurra algún error, el servidor devuelve una respuesta con el código de error HTTP adecuado y un mensaje de error en el cuerpo de la respuesta. Por ejemplo:
```
HTTP/1.0 400 Bad Request
Content-Type: application/json

{
  "error": "No se proporcionó el campo 'nombre' en el cuerpo de la solicitud"
}
```
## Ejemplos
A continuación se muestran algunos ejemplos de cómo se pueden realizar las operaciones CRUD en la aplicación utilizando cURL:

### Crear usuario (POST)
```
curl -X POST -H "Content-Type: application/json" -d '{"nombre": "Juan", "edad": 30}' http://localhost:8000
```
### Leer usuarios (GET)
```
curl http://localhost:8000
```
### Leer usuario por ID (GET)
```
curl http://localhost:8000?id=1
```
### Leer usuarios por nombre (GET)
```
curl http://localhost:8000?nombre=Juan
```
### Actualizar usuario (PUT)
```
curl -X PUT -H "Content-Type: application/json" -d '{"id": 1, "nombre": "Juan", "edad": 31}' http://localhost:8000
```
### Eliminar usuario (DELETE)
```
curl -X DELETE -H "Content-Type: application/json" -d '{"id": 1}' http://localhost:8000
```
