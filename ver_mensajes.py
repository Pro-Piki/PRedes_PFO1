import sqlite3

def ver_mensajes():
    """
    Consulta todos los mensajes almacenados en la base de datos chat.db
    y los muestra en consola de forma ordenada.
    """
    try:
        conn = sqlite3.connect("chat.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, contenido, fecha_envio, ip_cliente FROM mensajes ORDER BY id ASC")
        mensajes = cursor.fetchall()
        conn.close()

        if not mensajes:
            print("No hay mensajes registrados en la base de datos.")
            return

        print("\n Historial de mensajes guardados:\n")
        print("{:<5} {:<30} {:<20} {:<15}".format("ID", "Contenido", "Fecha de envío", "IP Cliente"))
        print("-" * 80)
        for msg in mensajes:
            print("{:<5} {:<30} {:<20} {:<15}".format(msg[0], msg[1][:30], msg[2], msg[3]))
    except sqlite3.Error as e:
        print(f"Error al consultar la base de datos: {e}")

if __name__ == "__main__":
    ver_mensajes()