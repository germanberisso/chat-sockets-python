# Chat Cliente-Servidor con Sockets (Python)

## Descripción
Aplicación de chat básica cliente-servidor utilizando sockets en Python.  
El servidor recibe mensajes de clientes, los almacena en una base de datos SQLite y responde con una confirmación con timestamp.

## Tecnologías
- Python 3
- Sockets (TCP/IP)
- SQLite

## Funcionalidades

### Servidor
- Escucha en 127.0.0.1:5000
- Maneja múltiples clientes con threading
- Guarda mensajes en SQLite con los campos:
  - id
  - contenido
  - fecha_envio
  - ip_cliente
- Manejo de errores (puerto ocupado, DB inaccesible)

### Cliente
- Se conecta al servidor
- Permite enviar múltiples mensajes
- Finaliza al escribir "éxito"
- Muestra la respuesta del servidor

## Ejecución

### 1. Ejecutar servidor
```bash
python servidor.py
