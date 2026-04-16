import socket
import sys

def start_client(host='127.0.0.1', port=5000):
    # Configuración del socket TCP/IP para el cliente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        print(f"Intentando conectar a {host}:{port}...")
        client_socket.connect((host, port))
        print("Conectado exitosamente al servidor.")
    except Exception as e:
        print(f"Error al conectar con el servidor: {e}")
        sys.exit(1)
        
    try:
        while True:
            mensaje = input("\nIngresá tu mensaje (escribí 'éxito' para salir): ")
            
            if mensaje.strip().lower() == 'éxito':
                # Aviso opcional al servidor
                client_socket.sendall("exit".encode('utf-8'))
                print("Desconectando...")
                break
                
            if not mensaje.strip():
                continue
                
            client_socket.sendall(mensaje.encode('utf-8'))
            
            try:
                data = client_socket.recv(1024)
                if not data:
                    print("El servidor cerró la conexión.")
                    break
                    
                respuesta_servidor = data.decode('utf-8')
                print(f"Servidor: {respuesta_servidor}")
                
            except Exception as e:
                print(f"Error al recibir la respuesta: {e}")
                break
                
    except KeyboardInterrupt:
        print("\nInterrupción del teclado. Cerrando cliente...")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()