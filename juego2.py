import pygame
import os
import random
import math
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
pasos_fantasmas = 18  # Los fantasmas se mueven cada 5 fotogramas

# Contadores
contador_pacman = 0
contador_fantasmas = 0

# Colores
CYAN, NEGRO, ROJO, AMARILLO,BLANCO = (0, 255, 255), (0, 0, 0), (255, 0, 0), (255, 255, 0), (255, 255, 255)

mapa = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
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
        (8,6),(8,7),(8,8),(8,9),(8,10),(8,11),(8,12),(8,13),   
        (9,6),(9,9),(9,12),
        (10,5),(10,6),(10,7),(10,8),(10,9),(10,10),(12,10),(10,11),(10,12),(10,13),(10,15),
        (11,6),(11,12),
        (12,6),(12,7),(12,8),(12,9),(12,10),(12,11),(12,12),(12,13),
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
    for nombre in os.listdir(DIRECTORIO_FANTASMAS):
        ruta = os.path.join(DIRECTORIO_FANTASMAS, nombre)
        if os.path.isdir(ruta):
            animaciones_fantasmas[nombre] = {}
            for direccion in ["izquierda", "derecha", "arriba", "abajo"]:
                animaciones_fantasmas[nombre][direccion] = []
                for i in range(2):
                    imagen_path = os.path.join(ruta, f"{nombre}_{direccion}_{i+1}.png")
                    if os.path.exists(imagen_path):
                        imagen = pygame.image.load(imagen_path).convert_alpha()
                        imagen = pygame.transform.scale(imagen, (TAM_CELDA, TAM_CELDA))
                        animaciones_fantasmas[nombre][direccion].append(imagen)
# Cargar imágenes de fantasmas vulnerables
    animaciones_fantasmas["vulnerables"] = []
    for i in range(2):
        imagen_path = os.path.join(DIRECTORIO_FANTASMAS, "vulnerables", f"vulnerable_{i+1}.png")
        if os.path.exists(imagen_path):
            imagen = pygame.image.load(imagen_path).convert_alpha()
            imagen = pygame.transform.scale(imagen, (TAM_CELDA, TAM_CELDA))
            animaciones_fantasmas["vulnerables"].append(imagen)
    # Cargar imagen de fantasmas muertos
    imagen_path = os.path.join(DIRECTORIO_FANTASMAS, "muerto", "muerto.png")
    if os.path.exists(imagen_path):
        imagen = pygame.image.load(imagen_path).convert_alpha()
        imagen = pygame.transform.scale(imagen, (TAM_CELDA, TAM_CELDA))
        animaciones_fantasmas["muerto"] = imagen
cargar_imagenes()
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
    def __init__(self, fila, columna, tipo, persigue, embosca, rodear, aleatorio, tiempo_salida):
        self.fila, self.columna, self.tipo = fila, columna, tipo
        self.direccion = random.choice(["izquierda", "derecha", "arriba", "abajo"])
        self.frame, self.last_update = 0, pygame.time.get_ticks()
        self.persigue = persigue
        self.embosca = embosca
        self.rodear = rodear
        self.aleatorio = aleatorio
        self.contador_movimiento = 0
        self.tiempo_salida = tiempo_salida
        self.inicio = pygame.time.get_ticks()
        self.vulnerable = False
        self.tiempo_vulnerable = 0
        self.poscicion_inicial = (fila, columna)
        self.muerto = False
        self.target = (fila, columna)  # Inicializa self.target
        self.velocidad_normal = pasos_fantasmas
        self.velocidad_vulnerable = pasos_fantasmas * 1.5
        if aleatorio:
            self.direccion = "derecha"
        elif rodear:
            self.direccion = "izquierda"
        elif embosca:
            self.direccion = "arriba"
        else:
            self.direccion = random.choice(["izquierda", "derecha", "arriba", "abajo"])

    def activar_vulnerabilidad(self):
        self.vulnerable = True
        self.tiempo_vulnerable = pygame.time.get_ticks()
        self.modo_vulnerable(True)  # Llama a modo_vulnerable cuando se activa la vulnerabilidad

    def modo_vulnerable(self, vulnerable):
        if vulnerable and not self.vulnerable:
            self.direccion_contraria()
            self.meta_random()
        self.vulnerable = vulnerable

    def direccion_contraria(self):
        direcciones_opuestas = {"arriba": "abajo", "abajo": "arriba", "izquierda": "derecha", "derecha": "izquierda"}
        self.direccion = direcciones_opuestas[self.direccion]

    def meta_random(self):
        self.target = (random.randint(0, FILAS - 1), random.randint(0, COLUMNAS - 1))

    def actualizar_estado(self):
        if self.vulnerable and pygame.time.get_ticks() - self.tiempo_vulnerable > 6000:  # tiempo de vulnerabilidad de los fantasmas
            self.vulnerable = False

    def meta_inicial(self):
        if self.muerto:
            self.target = self.poscicion_inicial

    def mover(self, ocupadas, pacman):
        self.actualizar_estado()
        if pygame.time.get_ticks() - self.inicio < self.tiempo_salida:
            return

        self.contador_movimiento += 1
        if self.muerto:
            velocidad = pasos_fantasmas // 2  # Aumenta la velocidad en un 50% cuando está comido
        elif self.vulnerable:
            velocidad = self.velocidad_vulnerable
        else:
            velocidad = self.velocidad_normal
            
        if self.contador_movimiento < velocidad:
            return
        self.contador_movimiento = 0

        if not hasattr(self, "llego_meta"):
            self.llego_meta = False

        if not self.llego_meta:
            objetivo_fila, objetivo_col = 8, 9
            if (self.fila, self.columna) == (8, 9):
                self.llego_meta = True
        else:
            if self.vulnerable:
                objetivo_fila, objetivo_col = self.target
            else:
                objetivo_fila, objetivo_col = pacman.fila, pacman.columna

        # Definir las opciones de movimiento
        opciones = [
            (self.fila - 1, self.columna, "arriba"),
            (self.fila + 1, self.columna, "abajo"),
            (self.fila, self.columna - 1, "izquierda"),
            (self.fila, self.columna + 1, "derecha")
        ]

        # Direcciones opuestas
        direcciones_opuestas = {"arriba": "abajo", "abajo": "arriba", "izquierda": "derecha", "derecha": "izquierda"}

        # Filtrar opciones válidas
        if self.muerto:
            opciones_validas = [
                (fila, col, dir)
                for fila, col, dir in opciones
                if 0 <= fila < FILAS and 0 <= col < COLUMNAS
                and mapa[fila][col] != 1
            ]
        else:
            opciones_validas = [
                (fila, col, dir)
                for fila, col, dir in opciones
                if 0 <= fila < FILAS and 0 <= col < COLUMNAS
                and (fila, col) not in ocupadas
                and mapa[fila][col] != 1
                and dir != direcciones_opuestas[self.direccion]  # Evitar retrocesos constantes
            ]

        if self.muerto:
            objetivo_fila, objetivo_col = self.poscicion_inicial
            if (self.fila,self.columna) == self.poscicion_inicial:
                self.muerto = False

        # para el fantasma naranja que su meta es dos casillas antes de la poscicion de pacman
        if self.rodear and not self.muerto:
            if pacman.direccion == "arriba":
                objetivo_fila += 4
            elif pacman.direccion == "abajo":
                objetivo_fila -= 4
            elif pacman.direccion == "izquierda":
                objetivo_col += 4
            elif pacman.direccion == "derecha":
                objetivo_col -= 4

        # para el fantasmas rosado que su meta esta dos casillas adelante de la poscicion de pacman
        if self.embosca and not self.muerto:
            if pacman.direccion == "arriba":
                objetivo_fila -= 4
            elif pacman.direccion == "abajo":
                objetivo_fila += 4
            elif pacman.direccion == "izquierda":
                objetivo_col += 4
            elif pacman.direccion == "derecha":
                objetivo_col += 4

        # para el fantasmas azul que su movimiento es aleatorio
        if self.aleatorio and not self.muerto:
            self.target = random.choice(opciones_validas)

        # en la fila 2 se tepea de la ultima columna a la primera y viceversa
        if self.fila == 2:
            if self.columna == 0 and self.direccion == "izquierda":
                self.columna = COLUMNAS - 1
            elif self.columna == COLUMNAS - 1 and self.direccion == "derecha":
                self.columna = 0

        # limitante para la casilla (9,9) solo se pueden mover hacia arriba no se puede ir hacia abajo
        if (self.fila, self.columna) in [(9, 9), (8, 9)]:
            opciones_validas = [opcion for opcion in opciones_validas if opcion[2] != "abajo"]

        if opciones_validas:
            mejor_opcion = min(
                opciones_validas,
                key=lambda pos: math.sqrt((pos[0] - objetivo_fila) ** 2 + (pos[1] - objetivo_col) ** 2)
            )
            self.fila, self.columna, self.direccion = mejor_opcion

    def draw(self):
        x, y = self.columna * TAM_CELDA + MARGEN, self.fila * TAM_CELDA + MARGEN
        now = pygame.time.get_ticks()
        if now - self.last_update > 200:
            self.last_update = now
            self.frame = (self.frame + 1) % 2  # Cambia el frame entre 0 y 1

        if self.muerto:
            ventana.blit(animaciones_fantasmas["muerto"], (x, y))
        elif self.vulnerable:
            # Asegúrate de que la lista no esté vacía
            if animaciones_fantasmas["vulnerables"]:
                ventana.blit(animaciones_fantasmas["vulnerables"][self.frame], (x, y))
        else:
            ventana.blit(animaciones_fantasmas[self.tipo][self.direccion][self.frame], (x, y))
            
fantasmas = [
    Fantasmas(10, 8, "fantasma_azul", False,False, False,True,15000),
    Fantasmas(8, 9, "fantasma_rojo", True, False, False,False,0),
    Fantasmas(10, 10, "fantasma_naranja", False, False, True,False,5000),
    Fantasmas(10, 9, "fantasma_rosa", False, True, False,False,1000)]

def mostrar_game_over():
    # Reproduce el video de Game Over 
    video_path = "assents/videos/game_over.mp4"
    clip = VideoFileClip(video_path)
    
    # Configuración de la ventana 
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
                for fantasma in fantasmas:
                    fantasma.activar_vulnerabilidad()
                
    def actualizar_poder(self):
        if self.modo_poder and pygame.time.get_ticks() - self.tiempo_poder > 6000:
            self.modo_poder = False 
            
    def verificar_colicion(self, fantasmas):
        for fantasma in fantasmas:
            if (self.fila, self.columna) == (fantasma.fila, fantasma.columna):
                if self.modo_poder and fantasma.vulnerable:
                    fantasma.meta_inicial()
                    fantasma.muerto = True 
                elif not fantasma.vulnerable and not fantasma.muerto:
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
        
        ocupadas = {(f.fila, f.columna) for f in fantasmas if not f.muerto}  # Excluir fantasmas comidos
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        pacman.mover(keys, ocupadas)
        pacman.draw()
        pacman.comer(puntos_casilla, poderes_casilla)  # Asegúrate de pasar los puntos y poderes correctos
        pacman.actualizar_poder()
        pacman.verificar_colicion(fantasmas)  # Verifica colisiones con fantasmas
        
        for fantasma in fantasmas:
            fantasma.mover(ocupadas,pacman)
            fantasma.draw()
        
        # Reducir el puntaje en una unidad cada 3 segundos
        if pygame.time.get_ticks() - ultimo_decremento >= 3000:
            puntaje -= 1
            ultimo_decremento = pygame.time.get_ticks()
            
        if not puntos_casilla:
            print("pasaste de nivel")
            run = False
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()

if __name__ == "__main__":
    main()