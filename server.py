import socket
import sqlite3
import datetime

# ------------------ Configuración de la Base de Datos ------------------
def inicializar_db():
    """
    Crea (si no existe) la base de datos SQLite para guardar mensajes.
    """
    try:
        conn = sqlite3.connect("chat.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error inicializando la base de datos: {e}")

# ------------------ Guardar mensaje en la DB ------------------
def guardar_mensaje(contenido, ip_cliente):
    """
    Inserta un mensaje en la base de datos con timestamp e IP del cliente.
    """
    try:
        conn = sqlite3.connect("chat.db")
        cursor = conn.cursor()
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO mensajes (contenido, fecha_envio, ip_cliente) VALUES (?, ?, ?)",
                       (contenido, fecha, ip_cliente))
        conn.commit()
        conn.close()
        return fecha
    except sqlite3.Error as e:
        print(f"Error guardando mensaje en la base de datos: {e}")
        return None

# ------------------ Configuración del socket TCP/IP ------------------
def inicializar_socket():
    """
    Crea un socket TCP/IP en localhost:5000 y lo deja escuchando.
    """
    try:
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.bind(("127.0.0.1", 5000))  # localhost:5000
        servidor.listen(5)  # hasta 5 conexiones en cola
        print("Servidor escuchando en 127.0.0.1:5000...")
        return servidor
    except OSError as e:
        print(f"Error al inicializar el socket: {e}")
        return None

# ------------------ Manejar conexiones ------------------
def manejar_conexiones(servidor):
    """
    Acepta conexiones de clientes y procesa los mensajes recibidos.
    """
    while True:
        conn, addr = servidor.accept()  # addr = (ip, puerto)
        print(f"Conexión establecida con {addr}")
        try:
            while True:
                data = conn.recv(1024).decode("utf-8")
                if not data:
                    break  # Cliente cerró la conexión
                print(f"Mensaje recibido de {addr[0]}: {data}")

                # Guardar mensaje en DB
                timestamp = guardar_mensaje(data, addr[0])

                # Responder al cliente
                if timestamp:
                    respuesta = f"Mensaje recibido: {timestamp}"
                else:
                    respuesta = "Error guardando el mensaje."
                conn.send(respuesta.encode("utf-8"))
        except Exception as e:
            print(f"Error con el cliente {addr}: {e}")
        finally:
            conn.close()
            print(f"Conexión cerrada con {addr}")

# ------------------ Punto de entrada ------------------
if __name__ == "__main__":
    inicializar_db()
    servidor = inicializar_socket()
    if servidor:
        manejar_conexiones(servidor)