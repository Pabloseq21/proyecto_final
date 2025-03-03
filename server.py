import socket
import threading
import pickle

# Configuración del servidor
HOST = '127.0.0.1'
PORT = 5555

# Lista para almacenar las conexiones de los clientes
clientes = []

# Estado inicial del juego
estado_juego = {
    'pacman': {'fila': 16, 'columna': 9, 'direccion': 'izquierda'},
    'fantasma': {'fila': 10, 'columna': 8, 'direccion': 'izquierda'}
}

def manejar_cliente(conn, addr):
    global estado_juego
    print(f"Conectado a {addr}")
    conn.send(pickle.dumps(estado_juego))
    
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            if not data:
                break
            estado_juego.update(data)
            enviar_a_todos(pickle.dumps(estado_juego))
        except:
            break
    
    print(f"Desconectado de {addr}")
    conn.close()
    clientes.remove(conn)

def enviar_a_todos(data):
    for cliente in clientes:
        try:
            cliente.send(data)
        except:
            cliente.close()
            clientes.remove(cliente)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print("Servidor iniciado, esperando conexiones...")

    while True:
        conn, addr = server.accept()
        clientes.append(conn)
        thread = threading.Thread(target=manejar_cliente, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()
