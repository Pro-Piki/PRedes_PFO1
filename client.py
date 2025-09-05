import socket

def cliente():
    """
    Cliente que se conecta al servidor y envía mensajes hasta escribir 'éxito' o 'exito' .
    """
    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect(("127.0.0.1", 5000))  # conectar al servidor
        print("Conectado al servidor en 127.0.0.1:5000")

        while True:
            mensaje = input("Escribe tu mensaje ('éxito' o 'exito' para salir): ")
            if mensaje.lower() == "éxito" or mensaje.lower() == "exito":
                print("Cerrando conexión...")
                break

            # enviar mensaje
            cliente_socket.send(mensaje.encode("utf-8"))

            # recibir respuesta
            respuesta = cliente_socket.recv(1024).decode("utf-8")
            print(f"Servidor: {respuesta}")

        cliente_socket.close()
    except Exception as e:
        print(f"Error en el cliente: {e}")

if __name__ == "__main__":
    cliente()