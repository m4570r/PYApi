import mysql.connector
import json
import http.server
import urllib.parse

# Crea una conexión a la base de datos MySQL
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='sistema'
)

# Crea una clase para manejar las solicitudes del servidor web
class RequestHandler(http.server.BaseHTTPRequestHandler):

    # Maneja la solicitud GET
    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        parsed_query = urllib.parse.parse_qs(parsed_url.query)
        
        # Si se proporcionó la versión en la URL, devuelve un JSON con la información de la versión
        if parsed_url.path == '/version':
            result = {'version': 'API escrita en Python'}
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        # Muestra todos los usuarios si no se proporcionó un parámetro de búsqueda
        elif not parsed_query:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM usuarios")
            result = cursor.fetchall()
            result = [{'id': user[0], 'nombre': user[1], 'edad': user[2]} for user in result]
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        else:
            # Filtra los usuarios según el parámetro de búsqueda proporcionado
            field = list(parsed_query.keys())[0]
            value = parsed_query[field][0]
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM usuarios WHERE {field}='{value}'")
            result = cursor.fetchall()
            result = [{'id': user[0], 'nombre': user[1], 'edad': user[2]} for user in result]
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
            
    def do_POST(self):
        # Lee el cuerpo de la solicitud
        body = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(body.decode())
    
        # Ejecuta una consulta INSERT a la base de datos
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO usuarios (nombre, edad) VALUES ('{data['nombre']}', {data['edad']})")
        connection.commit()
    
        # Devuelve el ID del registro insertado y los demás campos en la respuesta
        cursor.execute("SELECT LAST_INSERT_ID()")
        id = cursor.fetchone()[0]
        result = {'id': id, 'nombre': data['nombre'], 'edad': data['edad']}
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())

    def do_PUT(self):
        # Lee el cuerpo de la solicitud
        body = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(body.decode())
    
        # Obtiene el ID del usuario a modificar
        user_id = data['id']
    
        # Ejecuta una consulta UPDATE a la base de datos
        cursor = connection.cursor()
        cursor.execute(f"UPDATE usuarios SET nombre='{data['nombre']}', edad={data['edad']} WHERE id={user_id}")
        connection.commit()
    
        # Devuelve el ID del registro modificado y los demás campos en la respuesta
        result = {'id': user_id, 'nombre': data['nombre'], 'edad': data['edad']}
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())

    def do_DELETE(self):
        # Obtén el ID del registro a eliminar
        parsed_url = urllib.parse.urlparse(self.path)
        parsed_query = urllib.parse.parse_qs(parsed_url.query)
        id = parsed_query['id'][0]
    
        # Ejecuta una consulta DELETE en la base de datos
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM usuarios WHERE id={id}")
        connection.commit()
    
        # Envía una respuesta al cliente indicando que la operación se realizó correctamente
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'message': 'Record deleted successfully'}).encode())



if __name__ == '__main__':
    server = http.server.HTTPServer(('0.0.0.0', 80), RequestHandler)
    print('Serving on 0.0.0.0:80')
    server.serve_forever()
