import socket
import pickle
import threading

# Configuración del servidor
HOST = "0.0.0.0"  # Escucha en todas las interfaces de red
PORT = 5555

# Lista de jugadores conectados
clients = []

# Estado inicial del juego
game_state = {
    "players": {}
}

# Función para manejar clientes
def handle_client(conn, addr):
    global game_state
    print(f"Conexión establecida con {addr}")
    
    player_id = addr[1]  # Use port number as player ID
    game_state["players"][player_id] = {"x": 50, "y": 50, "dir": "right"}
    
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            
            # Decodificar datos del cliente
            player_move = pickle.loads(data)
            game_state["players"][player_id]["x"] += player_move["dx"]
            game_state["players"][player_id]["y"] += player_move["dy"]

            # Enviar estado del juego actualizado a todos los clientes
            for client in clients:
                client.sendall(pickle.dumps(game_state))

        except:
            break
    
    print(f"Cliente {addr} desconectado")
    conn.close()
    clients.remove(conn)
    del game_state["players"][player_id]

# Iniciar el servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Servidor esperando conexiones...")

while True:
    conn, addr = server.accept()
    clients.append(conn)
    threading.Thread(target=handle_client, args=(conn, addr)).start()
