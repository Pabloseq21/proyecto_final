import pygame
import os
import random
import math
import socket
import pickle
from moviepy import VideoFileClip 
from main import seleccionar_mapa
from pyparsing import col

pygame.init()

# Configuración de la cuadrícula y la ventana
MARGEN = 70
FILAS, COLUMNAS = 21, 19
TAM_CELDA = 35
ANCHO, ALTO = COLUMNAS * TAM_CELDA + 2 * MARGEN, FILAS * TAM_CELDA + 2 * MARGEN

ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Fantasmas")
clock = pygame.time.Clock()
fps = 30

# Velocidades
pasos_pacman = 5  # Pac-Man se mueve cada 4 fotogramas
pasos_fantasmas = pasos_pacman + 0.5  # Los fantasmas se mueven 0.5 fotogramas más lento que Pac-Man

# Contadores
contador_pacman = 0
contador_fantasmas = 0

# Colores
CYAN, NEGRO, ROJO, AMARILLO,BLANCO = (0, 255, 255), (0, 0, 0), (255, 0, 0), (255, 255, 0), (255, 255, 255)

mapa =  [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
    [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
    [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]

imagen_poder = pygame.image.load("assents/images/poder/poder.png")
imagen_poder = pygame.transform.scale(imagen_poder,(30,30))
imagen_punto = pygame.image.load("assents/images/puntos/puntos.png")
imagen_punto = pygame.transform.scale(imagen_punto,(10,10))
puntos =[]
puntaje = 0
fuente = pygame.font.Font("assents/Font/Minecraft.ttf", 36)  

excepciones_circulos = [
        (3,1),(3,17),(16,1),(16,17),
        (8,0),(8,1),(8,2),(8,6),(8,7),(8,8),(8,9),(8,10),(8,11),(8,12),(8,13),(8,16),(8,18),(8,17),    
        (9,6),(9,9),(9,12),
        (10,0),(10,1),(10,2),(10,3),(10,5),(10,6),(10,7),(10,8),(10,9),(10,10),(12,10),(10,11),(10,12),(10,13),(10,15),(10,16),(10,18),(10,17),
        (11,6),(11,12),
        (12,0),(12,1),(12,2),(12,6),(12,7),(12,8),(12,9),(12,10),(12,11),(12,12),(12,13),(12,16),(12,18),(12,17),
        (13,6),(13,12)
        ]
poderes_casilla = [(3,1),(3,17),(16,1),(16,17)]
puntos_casilla = []
def dibujar_mapa():
    global puntos_casilla
    for fila in range(len(mapa)):
        for col in range(len(mapa[0])):
            color = (0, 0, 255) if mapa[fila][col] == 1 else (0, 0, 0)
            pygame.draw.rect(ventana, color, (col * TAM_CELDA + MARGEN, fila * TAM_CELDA + MARGEN, TAM_CELDA, TAM_CELDA))
            
    for fila, col in puntos_casilla:
        ventana.blit(imagen_punto, (col * TAM_CELDA + MARGEN + TAM_CELDA // 2 - 5, fila * TAM_CELDA + MARGEN + TAM_CELDA // 2 - 5))
    for fila, col in poderes_casilla:
        ventana.blit(imagen_poder, (col * TAM_CELDA + MARGEN + TAM_CELDA // 2 - 15, fila * TAM_CELDA + MARGEN + TAM_CELDA // 2 - 15))

def verificar_puntos(pacman_x,pacman_y):
    global puntaje,puntos
    fila =(pacman_y- MARGEN) // TAM_CELDA
    col =(pacman_x-MARGEN) // TAM_CELDA
    if (fila,col)in puntos:
        puntos.remove((fila,col))
        puntaje += 100 
        
def mostrar_puntaje():
    texto_puntaje = fuente.render(f"puntaje: {puntaje}", True, BLANCO)
    texto_1up = fuente.render("1 UP", True, BLANCO)
    
    # Calcular las posiciones centradas
    puntaje_rect = texto_puntaje.get_rect(center=(ANCHO // 2, 30))
    up_rect = texto_1up.get_rect(center=(ANCHO // 2, 70))
    
    ventana.blit(texto_puntaje, puntaje_rect)
    ventana.blit(texto_1up, up_rect)

# Cargar imágenes de fantasmas
DIRECTORIO_FANTASMAS = "assents/images/fantasmas"
animaciones_fantasmas = {}

def cargar_imagenes():
    if not os.path.exists(DIRECTORIO_FANTASMAS):
        print(f"Error: El directorio {DIRECTORIO_FANTASMAS} no existe.")
        return

    # Cargar imágenes de fantasmas vulnerables (sin dirección)
    animaciones_fantasmas["vulnerables"] = []
    for i in range(2):
        imagen_path = os.path.join(DIRECTORIO_FANTASMAS, "vulnerables", f"vulnerable_{i+1}.png")
        if os.path.exists(imagen_path):
            try:
                imagen = pygame.image.load(imagen_path).convert_alpha()
                imagen = pygame.transform.scale(imagen, (TAM_CELDA, TAM_CELDA))
                animaciones_fantasmas["vulnerables"].append(imagen)
            except pygame.error as e:
                print(f"Error al cargar la imagen {imagen_path}: {e}")
        else:
            print(f"Advertencia: La imagen {imagen_path} no existe.")
    
    # Cargar imágenes del fantasma azul
    animaciones_fantasmas["fantasma_azul"] = {"izquierda": [], "derecha": [], "arriba": [], "abajo": []}
    for direccion in ["izquierda", "derecha", "arriba", "abajo"]:
        for i in range(2):
            imagen_path = os.path.join(DIRECTORIO_FANTASMAS, "fantasma_azul", f"fantasma_azul_{direccion}_{i+1}.png")
            if os.path.exists(imagen_path):
                try:
                    imagen = pygame.image.load(imagen_path).convert_alpha()
                    imagen = pygame.transform.scale(imagen, (TAM_CELDA, TAM_CELDA))
                    animaciones_fantasmas["fantasma_azul"][direccion].append(imagen)
                except pygame.error as e:
                    print(f"Error al cargar la imagen {imagen_path}: {e}")
            else:
                print(f"Advertencia: La imagen {imagen_path} no existe.")
    
    # Cargar imagen de fantasmas comidos (sin dirección)
    imagen_path = os.path.join(DIRECTORIO_FANTASMAS, "comido", "comido.png")
    if os.path.exists(imagen_path):
        try:
            imagen = pygame.image.load(imagen_path).convert_alpha()
            imagen = pygame.transform.scale(imagen, (TAM_CELDA, TAM_CELDA))
            animaciones_fantasmas["comido"] = imagen
        except pygame.error as e:
            print(f"Error al cargar la imagen {imagen_path}: {e}")
    else:
        print(f"Advertencia: La imagen {imagen_path} no existe.")

cargar_imagenes()
print(animaciones_fantasmas)

# Pac-Man
DIRECTORIO_PACMAN = "assents/images/pacman"
animaciones_pacman = {}

def cargar_imagenes_pacman():
    for direccion in ["izquierda", "derecha", "arriba", "abajo"]:
        animaciones_pacman[direccion] = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(DIRECTORIO_PACMAN, f"pacman_{direccion}_{i+1}.png")).convert_alpha(),
                (TAM_CELDA, TAM_CELDA)
            ) for i in range(3) if os.path.exists(os.path.join(DIRECTORIO_PACMAN, f"pacman_{direccion}_{i+1}.png"))
        ]

cargar_imagenes_pacman()

def dibujar_celdas():
    for fila in range(FILAS):
        for col in range(COLUMNAS):
            pygame.draw.rect(ventana, CYAN, (col * TAM_CELDA + MARGEN, fila * TAM_CELDA + MARGEN, TAM_CELDA, TAM_CELDA), 1)
            
class Fantasmas:
    def __init__(self, fila, columna, tipo, tiempo_salida):
        self.fila, self.columna, self.tipo = fila, columna, tipo
        self.direccion = random.choice(["izquierda", "derecha", "arriba", "abajo"])
        self.frame, self.last_update = 0, pygame.time.get_ticks()
        self.contador_movimiento = 0
        self.tiempo_salida = tiempo_salida
        self.inicio = pygame.time.get_ticks()
        self.vulnerable = False
        self.tiempo_vulnerable = 0
        self.poscicion_inicial = (fila, columna)
        self.volviendo = False
        self.comido = False
        self.target = (fila, columna)  # Inicializa self.target
        self.controlado_por_jugador = True  # Permitir el control del jugador

    def activar_vulnerabilidad(self):
        self.vulnerable = True
        self.tiempo_vulnerable = pygame.time.get_ticks()
        self.modo_vulnerable(True)  # Llama a modo_vulnerable cuando se activa la vulnerabilidad

    def modo_vulnerable(self, vulnerable):
        if vulnerable and not self.vulnerable:
            self.vulnerable = vulnerable

    def actualizar_estado(self):
        if self.vulnerable and pygame.time.get_ticks() - self.tiempo_vulnerable > 6000:  # tiempo de vulnerabilidad de los fantasmas
            self.vulnerable = False

    def reiniciar_poscicion(self):
        self.volviendo = True
        self.vulnerable = False
        self.comido = True
        self.controlado_por_jugador = False  # Desactivar el control del jugador
        self.target = self.poscicion_inicial  # Establecer la meta como la posición inicial

    def mover(self, keys, ocupadas):
        self.actualizar_estado()

        if pygame.time.get_ticks() - self.inicio < self.tiempo_salida:
            return
        self.contador_movimiento += 1
        if self.contador_movimiento < pasos_fantasmas:
            return
        self.contador_movimiento = 0

        if self.volviendo:
            # Movimiento automático hacia la posición inicial
            if self.fila < self.target[0]:
                self.fila += 1
                self.direccion = "abajo"
            elif self.fila > self.target[0]:
                self.fila -= 1
                self.direccion = "arriba"
            elif self.columna < self.target[1]:
                self.columna += 1
                self.direccion = "derecha"
            elif self.columna > self.target[1]:
                self.columna -= 1
                self.direccion = "izquierda"
            
            # Si el fantasma ha llegado a la posición inicial
            if (self.fila, self.columna) == self.poscicion_inicial:
                self.volviendo = False
                self.comido = False
                self.controlado_por_jugador = True  # Devolver el control al jugador
            return

        if self.controlado_por_jugador:
            nueva_fila, nueva_col = self.fila, self.columna
            if keys[pygame.K_UP]:
                nueva_fila -= 1
                self.direccion = "arriba"
            elif keys[pygame.K_DOWN]:
                nueva_fila += 1
                self.direccion = "abajo"
            elif keys[pygame.K_LEFT]:
                nueva_col -= 1
                self.direccion = "izquierda"
            elif keys[pygame.K_RIGHT]:
                nueva_col += 1
            # Verificar si la nueva posición es válida antes de moverse
            if (0 <= nueva_fila < FILAS and 0 <= nueva_col < COLUMNAS and 
                mapa[nueva_fila][nueva_col] != 1 and (nueva_fila, nueva_col) not in ocupadas):
                self.fila, self.columna = nueva_fila, nueva_col

        # en la fila 10 se tepea de la ultima columna a la primera y viceversa
        if self.fila == 10:
            if self.columna == 0 and self.direccion == "izquierda":
                self.columna = COLUMNAS - 1
            elif self.columna == COLUMNAS - 1 and self.direccion == "derecha":
                self.columna = 0

    def draw(self):
        x, y = self.columna * TAM_CELDA + MARGEN, self.fila * TAM_CELDA + MARGEN
        now = pygame.time.get_ticks()
        if now - self.last_update > 200:
            self.last_update = now
            self.frame = (self.frame + 1) % 2  # Cambia el frame entre 0 y 1

        if self.comido:
            ventana.blit(animaciones_fantasmas["comido"], (x, y))
        elif self.vulnerable:
            # Asegúrate de que la lista no esté vacía
            if animaciones_fantasmas["vulnerables"]:
                ventana.blit(animaciones_fantasmas["vulnerables"][self.frame], (x, y))
        else:
            ventana.blit(animaciones_fantasmas[self.tipo][self.direccion][self.frame], (x, y))
            
# Eliminar la lista de fantasmas y crear un solo fantasma controlado por el jugador
fantasma = Fantasmas(10, 8, "fantasma_azul", 0)

def mostrar_game_over():
    # Reproduce el video de Game Over usando pygame
    video_path = "assents/videos/game_over.mp4"
    clip = VideoFileClip(video_path)
    
    # Configuración de la ventana de pygame
    screen = pygame.display.set_mode(clip.size)
    pygame.display.set_caption("Game Over")

    # Reproduce el video
    for frame in clip.iter_frames(fps=30, dtype="uint8"):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(surface, (0, 0))
        pygame.display.update()
        pygame.time.wait(int(1000 / 30))  # Espera para mantener la tasa de fotogramas

    # Espera un poco después de que el video termine
    pygame.time.wait(500)
    
    seleccionar_mapa()

def mostrar_victoria():
    # Reproduce el video de Victoria 
    video_path = "assents/videos/victoria.mp4"
    clip = VideoFileClip(video_path)
    
    # Configuración de la ventana 
    screen = pygame.display.set_mode(clip.size)
    pygame.display.set_caption("Victoria")

    # Reproduce el video
    for frame in clip.iter_frames(fps=30, dtype="uint8"):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(surface, (0, 0))
        pygame.display.update()
        pygame.time.wait(int(1000 / 30))  # Espera para mantener la tasa de fotogramas

    # Espera un poco después de que el video termine
    pygame.time.wait(500)
    
    seleccionar_mapa()

#clase para pacman 
class Pacman:
    def __init__(self, fila, columna):
        self.fila, self.columna, self.direccion = fila, columna, "izquierda"
        self.frame, self.last_update = 0, pygame.time.get_ticks()
        self.last_update = pygame.time.get_ticks()
        self.modo_poder = False
        self.tiempo_poder = 0

    def comer(self, puntos_casilla, poderes_casilla):
        global puntaje
        for punto in puntos_casilla:
            if (self.fila, self.columna) == punto:
                puntos_casilla.remove(punto)
                puntaje += 10  # Incrementa el puntaje al comer un punto
                
        for poder in poderes_casilla:
            if (self.fila, self.columna) == poder:
                poderes_casilla.remove(poder)
                self.modo_poder = True
                self.tiempo_poder = pygame.time.get_ticks()
                for fantasma in fantasma:
                    fantasma.activar_vulnerabilidad()
                
    def actualizar_poder(self):
        if self.modo_poder and pygame.time.get_ticks() - self.tiempo_poder > 6000:
            self.modo_poder = False 
            
    def verificar_colicion(self, fantasmas):
        for fantasma in fantasmas:
            if (self.fila, self.columna) == (fantasma.fila, fantasma.columna):
                if self.modo_poder and fantasma.vulnerable:
                    fantasma.reiniciar_poscicion()
                    fantasma.comido = True  # Marca el fantasma como comido
                elif not fantasma.vulnerable and not fantasma.comido:
                    print("Game Over")
                    mostrar_game_over()  # Mostrar el video de Game Over
                    pygame.quit()
                    exit()
            
    def mover(self, keys, ocupadas):
        global contador_pacman
        contador_pacman += 1
        if contador_pacman < pasos_pacman:
            return
        contador_pacman = 0
        nueva_fila, nueva_col = self.fila, self.columna
        if keys[pygame.K_w]:
            self.direccion, nueva_fila = "arriba", self.fila - 1
        elif keys[pygame.K_s]:
            self.direccion, nueva_fila = "abajo", self.fila + 1
        elif keys[pygame.K_a]:
            self.direccion, nueva_col = "izquierda", self.columna - 1
        elif keys[pygame.K_d]:
            self.direccion, nueva_col = "derecha", self.columna + 1
        if (nueva_fila, nueva_col) not in ocupadas and 0 <= nueva_fila < FILAS and 0 <= nueva_col < COLUMNAS and mapa[nueva_fila][nueva_col] != 1:
            self.fila, self.columna = nueva_fila, nueva_col
            
        if self.fila == 10:
            if self.columna == 0 and self.direccion == "izquierda":
                self.columna = COLUMNAS - 1
            elif self.columna == COLUMNAS - 1 and  self.direccion == "derecha":
                self.columna = 0

    def draw(self):
        x, y = self.columna * TAM_CELDA + MARGEN, self.fila * TAM_CELDA + MARGEN
        now = pygame.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update, self.frame = now, (self.frame + 1) % len(animaciones_pacman[self.direccion])
        ventana.blit(animaciones_pacman[self.direccion][self.frame], (x, y))
        if animaciones_pacman[self.direccion]:  # Asegura que existan animaciones
            ventana.blit(animaciones_pacman[self.direccion][self.frame], (x, y))
            
pacman = Pacman(16, 9)  #poscicion inicial de pacman               

# Define una variable para almacenar el tiempo del último decremento del puntaje
ultimo_decremento = pygame.time.get_ticks()

# Cargar imagen de los márgenes
imagen_margen = pygame.image.load("assents/images/margen/margen.png")
imagen_margen = pygame.transform.scale(imagen_margen, (MARGEN, ALTO // 2))

def dibujar_margen():
    # Dibujar la imagen en los márgenes izquierdo y derecho
    ventana.blit(imagen_margen, (0, 0))
    ventana.blit(imagen_margen, (0, ALTO // 2))
    ventana.blit(imagen_margen, (ANCHO - MARGEN, 0))
    ventana.blit(imagen_margen, (ANCHO - MARGEN, ALTO // 2))

# Configuración del cliente
HOST = '127.0.0.1'
PORT = 5555

# Conectar al servidor
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

# Recibir el estado inicial del juego
estado_juego = pickle.loads(cliente.recv(2048))

# Actualizar las posiciones iniciales de Pac-Man y el fantasma
pacman = Pacman(estado_juego['pacman']['fila'], estado_juego['pacman']['columna'])
fantasma = Fantasmas(estado_juego['fantasma']['fila'], estado_juego['fantasma']['columna'], "fantasma_azul", 0)

def enviar_estado():
    estado = {
        'pacman': {'fila': pacman.fila, 'columna': pacman.columna, 'direccion': pacman.direccion},
        'fantasma': {'fila': fantasma.fila, 'columna': fantasma.columna, 'direccion': fantasma.direccion}
    }
    cliente.send(pickle.dumps(estado))

def recibir_estado():
    global estado_juego
    estado_juego = pickle.loads(cliente.recv(2048))
    pacman.fila = estado_juego['pacman']['fila']
    pacman.columna = estado_juego['pacman']['columna']
    pacman.direccion = estado_juego['pacman']['direccion']
    fantasma.fila = estado_juego['fantasma']['fila']
    fantasma.columna = estado_juego['fantasma']['columna']
    fantasma.direccion = estado_juego['fantasma']['direccion']

def main():
    global puntos_casilla, ultimo_decremento, puntaje
    puntos_casilla = [(fila, col) for fila in range(len(mapa)) for col in range(len(mapa[0])) if mapa[fila][col] == 0 and (fila, col) not in excepciones_circulos]
    
    run = True
    while run:
        ventana.fill(NEGRO)
        dibujar_margen()  # Dibujar los márgenes
        dibujar_celdas()
        dibujar_mapa()
        verificar_puntos(pacman.fila, pacman.columna)  # Verifica puntos y actualiza el puntaje
        mostrar_puntaje()
        
        ocupadas = {(fantasma.fila, fantasma.columna)}  # Solo el fantasma azul ocupa una casilla
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        pacman.mover(keys, ocupadas)
        pacman.draw()
        pacman.comer(puntos_casilla, poderes_casilla)  # Asegúrate de pasar los puntos y poderes correctos
        pacman.actualizar_poder()
        pacman.verificar_colicion([fantasma])  # Verifica colisiones con el único fantasma
        
        # Mover el fantasma con las flechas del teclado celda por celda
        fantasma.mover(keys, ocupadas)
        fantasma.draw()
        
        # Reducir el puntaje en una unidad cada 3 segundos
        if pygame.time.get_ticks() - ultimo_decremento >= 3000:
            puntaje -= 1
            ultimo_decremento = pygame.time.get_ticks()
            
        if not puntos_casilla:
            print("pasaste de nivel")
            mostrar_victoria()  # Mostrar el video de victoria
            run = False
        
        # Enviar y recibir el estado del juego
        enviar_estado()
        recibir_estado()
        
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()

if __name__ == "__main__":
    main()