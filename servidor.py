import socket
import sqlite3
import datetime
import sys
import threading

# Configuración de base de datos
DB_NAME = "chat_mensajes.db"


def init_db():
    """
    Inicializa la base de datos y crea la tabla si no existe.
    """
    try:
        conn = sqlite3.connect(DB_NAME)
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
        print(f"Error al acceder a la base de datos: {e}")
        sys.exit(1)


def save_message(ip, message):
    """
    Guarda un mensaje en la base de datos.
    Se abre y cierra conexión por cada operación (más seguro en multihilo).
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            "INSERT INTO mensajes (contenido, fecha_envio, ip_cliente) VALUES (?, ?, ?)",
            (message, timestamp, ip)
        )

        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print(f"Error al guardar el mensaje en la base de datos: {e}")


def init_socket(host='127.0.0.1', port=5000):
    """
    Inicializa el socket del servidor.
    """
    # Configuración del socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Permite reutilizar el puerto rápidamente
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Servidor escuchando en {host}:{port}")
        return server_socket

    except OSError as e:
        print(f"Error al inicializar el socket (¿puerto ocupado?): {e}")
        sys.exit(1)


def handle_client(client_socket, address):
    """
    Maneja la comunicación con un cliente individual.
    """
    ip_cliente = address[0]
    print(f"\nConexión establecida con: {ip_cliente}")

    try:
        while True:
            data = client_socket.recv(1024)

            if not data:
                break

            mensaje = data.decode('utf-8')
            print(f"Mensaje de {ip_cliente}: {mensaje}")

            # Guardar en la base de datos
            save_message(ip_cliente, mensaje)

            # Respuesta al cliente con timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            respuesta = f"Mensaje recibido: {timestamp}"

            client_socket.sendall(respuesta.encode('utf-8'))

    except Exception as e:
        print(f"Error con cliente {ip_cliente}: {e}")

    finally:
        client_socket.close()
        print(f"Conexión finalizada con: {ip_cliente}")


def handle_connections(server_socket):
    """
    Acepta conexiones entrantes y crea un hilo por cliente.
    """
    while True:
        try:
            client_socket, address = server_socket.accept()

            # Crear hilo para manejar cliente
            thread = threading.Thread(
                target=handle_client,
                args=(client_socket, address)
            )
            thread.start()

        except Exception as e:
            print(f"Error al aceptar conexiones: {e}")


if __name__ == "__main__":
    print("Iniciando servidor...")

    init_db()
    server_socket = init_socket()

    try:
        handle_connections(server_socket)

    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario.")

    finally:
        server_socket.close()