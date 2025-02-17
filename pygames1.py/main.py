import pygame
import firebase_admin
from firebase_admin import credentials, db
from moviepy import VideoFileClip  # Para reproducir el video
import constantes  # Importar constantes desde el otro archivo

pygame.init()  # Iniciar pygame

# Inicializar Firebase
cred = credentials.Certificate(r"testpython-673c0-firebase-adminsdk-b93r7-bd9607d785.json")  # Reemplaza con la ruta de tu archivo JSON
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://testpython-673c0-default-rtdb.firebaseio.com/'
})

def obtener_puntajes():
    try:
        # Obtiene los datos de la base de datos
        ref = db.reference('users')
        usuarios = ref.get()  # Obtener todos los usuarios de la base de datos

        # Depuración: Verifica que los datos sean correctos
        if usuarios:
            print("Usuarios obtenidos de Firebase:")
            for usuario_id, usuario_data in usuarios.items():
                print(f"ID: {usuario_id}, Nombre: {usuario_data.get('display_name')}, Puntuación: {usuario_data.get('score')}")
        else:
            print("No se encontraron usuarios en la base de datos.")

        puntajes = []
        for usuario_id, usuario_data in usuarios.items():
            display_name = usuario_data.get('display_name', 'Desconocido')
            score = usuario_data.get('score', 0)
            puntajes.append((display_name, score))  # Guardar los nombres y puntajes en una lista

        # Ordenar los puntajes de mayor a menor
        puntajes.sort(key=lambda x: x[1], reverse=True)
        return puntajes
    except Exception as e:
        print(f"Error al obtener puntajes de Firebase: {e}")
        return []

# Crear una ventana
vent = pygame.display.set_mode((constantes.WIDTH, constantes.HEIGHT))  # Crear una ventana con las medidas del archivo de constantes
pygame.display.set_caption("Pac-man")  # Nombre de la ventana

# Fuentes
front_inicio = pygame.font.SysFont("Minecraft", 30)

# Botones
boton_start = pygame.Rect(constantes.WIDTH / 2 - 100, constantes.HEIGHT / 2 - 50, 200, 50)
boton_exit = pygame.Rect(constantes.WIDTH / 2 - 100, constantes.HEIGHT / 2 + 50, 200, 50)

# Función para el color de los botones con transparencia
def color_bot(button_rect):  # Función para cambiar el color de los botones
    mouse_pos = pygame.mouse.get_pos()
    
    if button_rect.collidepoint(mouse_pos):  # Verifica si el mouse está sobre el botón
        return (255, 255, 255, 64)  # blanco con transparencia (alfa 128)
    else:
        return (0, 0, 0, 0)  # Transparente (alfa 0) cuando el mouse no está sobre el botón

# Función para obtener el tamaño del texto
def get_text_width_height(text, font):
    text_surface = font.render(text, True, (255, 255, 255))
    return text_surface.get_width(), text_surface.get_height()

# Función para crear los botones sin crear una superficie adicional
def dibujar_boton(texto, x, y, font):  
    # Obtener el tamaño del texto
    width, height = get_text_width_height(texto, font)
    
    # Crear un rectángulo que se ajuste al tamaño del texto
    button_rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
    
    # Color de los botones
    color = color_bot(button_rect)
    
    # Crear una superficie con transparencia (con un canal alfa)
    surface_boton = pygame.Surface(button_rect.size, pygame.SRCALPHA)
    surface_boton.fill(color)  # Rellenar la superficie con el color RGBA que incluye la transparencia
    
    # Dibujar la superficie sobre la ventana
    vent.blit(surface_boton, button_rect.topleft)

    # Dibujar el texto sobre el botón
    text_surface = font.render(texto, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=button_rect.center)
    vent.blit(text_surface, text_rect)

# Función para reproducir el video de introducción
def play_intro_video(video_path):
    video = VideoFileClip(video_path)
    
    # Calcular la escala para mantener la relación de aspecto
    video_width, video_height = video.size
    scale = min(constantes.WIDTH / video_width, constantes.HEIGHT / video_height)
    new_width = int(video_width * scale)
    new_height = int(video_height * scale)
    
    # Calcular la posición centrada del video
    x_offset = (constantes.WIDTH - new_width) // 2
    y_offset = (constantes.HEIGHT - new_height) // 2

    clock = pygame.time.Clock()
    
    # Reproducir el video frame por frame
    for frame in video.iter_frames(fps=60, with_times=False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        frame_surface = pygame.transform.scale(frame_surface, (new_width, new_height))  # Escalar el frame
        vent.fill((0, 0, 0))  # Llenar el fondo de negro
        vent.blit(frame_surface, (x_offset, y_offset))  # Dibujar el video centrado

        pygame.display.update()
        clock.tick(30)

    video.close()

# Función para obtener los puntajes desde Firebase
def obtener_top_scores():
    ref = db.reference('/users')  # Ruta al nodo de usuarios en Firebase
    users = ref.get()  # Obtener los datos desde Firebase

    if users:
        print("Puntajes:")  # Muestra los puntajes en la consola
        # Ordenar los usuarios por el puntaje
        sorted_users = sorted(users.values(), key=lambda x: x['score'], reverse=True)
        
        y_offset = 150  # Inicialización para la posición Y de los puntajes
        for user in sorted_users:
            score_text = f"{user['display_name']}: {user['Puntuación']}"  # Mostrar el nombre del jugador y su puntaje
            text_surface = front_inicio.render(score_text, True, (255, 255, 255))
            vent.blit(text_surface, (constantes.WIDTH // 2 - text_surface.get_width() // 2, y_offset))
            y_offset += 40  # Espaciado entre cada puntaje

        pygame.display.update()  # Actualizar la pantalla después de mostrar los puntajes
    else:
        print("No se encontraron puntajes.")
        
def ventana_top_scores():
    puntajes = obtener_puntajes()  # Obtener los puntajes desde Firebase

    # Crear una ventana para mostrar los puntajes
    ventana_scores = True
    while ventana_scores:
        vent.fill((0, 0, 0))  # Fondo negro

        # Título de la ventana
        mostrar_titulo = front_inicio.render("Top Scores", True, (255, 255, 255))
        vent.blit(mostrar_titulo, (constantes.WIDTH / 2 - mostrar_titulo.get_width() / 2, 50))

        # Mostrar los puntajes
        y_offset = 150  # Para comenzar a dibujar las puntuaciones desde una posición vertical
        for display_name, score in puntajes:
            texto = f"{display_name}: {score}"
            texto_score = front_inicio.render(texto, True, (255, 255, 255))
            vent.blit(texto_score, (constantes.WIDTH / 2 - texto_score.get_width() / 2, y_offset))
            y_offset += 40  # Separar cada línea de puntajes

        # Botón para salir de la ventana de puntajes y volver al menú principal
        boton_exit = pygame.Rect(constantes.WIDTH / 2 - 100, constantes.HEIGHT - 100, 200, 50)
        dibujar_boton("EXIT", boton_exit.centerx, boton_exit.centery, front_inicio)

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ventana_scores = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_exit.collidepoint(event.pos):
                    ventana_scores = False  # Cerrar la ventana de puntajes y volver al menú principal
                    menu_principal()  # Volver al menú principal

        pygame.display.flip()  # Actualizar la ventana
# Nueva ventana para mostrar el mensaje de "Estoy Online"
def ventana_online():
    run = True
    while run:
        vent.fill((0, 0, 0))  # Fondo negro

        # Mostrar el mensaje
        mensaje = front_inicio.render("REMEMBER, u have to be online to save your progress", True, (255, 255, 255))
        vent.blit(mensaje, (constantes.WIDTH / 2 - mensaje.get_width() / 2, constantes.HEIGHT / 3))

        # Botones para "I'm Online" y "Exit"
        boton_online = pygame.Rect(constantes.WIDTH / 2 - 100, constantes.HEIGHT / 2 - 50, 200, 50)
        boton_exit = pygame.Rect(constantes.WIDTH / 2 - 100, constantes.HEIGHT / 2 + 50, 200, 50)

        dibujar_boton("I'm Online", boton_online.centerx, boton_online.centery, front_inicio)
        dibujar_boton("Exit", boton_exit.centerx, boton_exit.centery, front_inicio)

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_online.collidepoint(event.pos):
                    print("El jugador está online.")
                    run = False  # Cerrar la ventana emergente y continuar con el juego
                elif boton_exit.collidepoint(event.pos):
                    print("Volviendo al menú principal...")
                    menu_principal()  # Regresar al menú principal
                    run = False

        pygame.display.flip()  # Actualizar la ventana

def menu_principal():
    fondo_imagen = pygame.image.load(r"C:\Users\user\Downloads\P U C K.jpg")  # Cambia esta ruta por la imagen que desees
    fondo_imagen = pygame.transform.scale(fondo_imagen, (constantes.WIDTH, constantes.HEIGHT))  # Escalar la imagen al tamaño de la ventana

    boton_play = pygame.Rect(constantes.WIDTH / 2 - 100, constantes.HEIGHT / 2 - 100, 200, 50)
    boton_top_scores = pygame.Rect(constantes.WIDTH / 2 - 100, constantes.HEIGHT / 2, 200, 50)
    boton_exit = pygame.Rect(constantes.WIDTH / 2 - 100, constantes.HEIGHT / 2 + 100, 200, 50)

    run = True
    while run:
        vent.blit(fondo_imagen, (0, 0))  # Dibujar la imagen de fondo sobre la ventana

        dibujar_boton("PLAY", boton_play.centerx, boton_play.centery, front_inicio)  # Botón PLAY
        dibujar_boton("TOP SCORES", boton_top_scores.centerx, boton_top_scores.centery, front_inicio)  # Botón TOP SCORES
        dibujar_boton("EXIT", boton_exit.centerx, boton_exit.centery, front_inicio)  # Botón EXIT

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_play.collidepoint(event.pos):
                    print("Iniciar ventana 'I'm online'...")
                    ventana_online()  # Mostrar la ventana emergente "I'm online"
                    run = False  # Cerrar el menú y continuar con el juego
                elif boton_top_scores.collidepoint(event.pos):
                    print("Mostrando puntajes más altos...")
                    ventana_top_scores()  # Mostrar la ventana de top scores
                elif boton_exit.collidepoint(event.pos):
                    print("Volviendo al menú de opciones...")
                    opciones()  # Llamar a la función opciones para regresar al menú de opciones
                    run = False  # Cerrar el menú principal

        pygame.display.flip()  # Actualizar la ventana

# Función para la ventana de opciones (START y EXIT)
def opciones():
    fondo_imagen = pygame.image.load(r"C:\Users\user\Downloads\P U C K (2).jpg")  # Cambia esta ruta por la imagen que desees
    fondo_imagen = pygame.transform.scale(fondo_imagen, (constantes.WIDTH, constantes.HEIGHT))  # Escalar la imagen al tamaño de la ventana

    run = True
    while run:
        vent.blit(fondo_imagen, (0, 0))  # Dibujar la imagen de fondo

        dibujar_boton("START", boton_start.centerx, boton_start.centery, front_inicio)  # Botón START
        dibujar_boton("EXIT", boton_exit.centerx, boton_exit.centery, front_inicio)    # Botón EXIT

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_start.collidepoint(event.pos):
                    print("Iniciar juego...")
                    run = False  # Cerrar la ventana de opciones y abrir el menú
                    menu_principal()  # Abrir el menú principal después de presionar "START"
                elif boton_exit.collidepoint(event.pos):
                    pygame.quit()  # Salir del juego
                    run = False

        pygame.display.flip()  # Actualizar la ventana

# Ventana con opciones (START y EXIT)
def opciones():
    # Cargar imagen de fondo
    fondo_imagen = pygame.image.load(r"C:\Users\user\Downloads\P U C K (2).jpg")  # Cambia esta ruta por la imagen que desees
    fondo_imagen = pygame.transform.scale(fondo_imagen, (constantes.WIDTH, constantes.HEIGHT))  # Escalar la imagen al tamaño de la ventana

    run = True
    while run:
        vent.blit(fondo_imagen, (0, 0))  # Dibujar la imagen de fondo

        dibujar_boton("START", boton_start.centerx, boton_start.centery, front_inicio)  # Botón START
        dibujar_boton("EXIT", boton_exit.centerx, boton_exit.centery, front_inicio)    # Botón EXIT

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_start.collidepoint(event.pos):
                    print("Iniciar juego...")
                    run = False  # Cerrar la ventana de opciones y abrir el menú
                    menu_principal()  # Abrir el menú principal después de presionar "START"
                elif boton_exit.collidepoint(event.pos):
                    pygame.quit()  # Salir del juego
                    run = False

        pygame.display.flip()  # Actualizar la ventana

# Código principal del juego
if __name__ == "__main__":
    # Reproducir el video de introducción antes de mostrar el menú
    play_intro_video(r"C:\Users\user\Videos\0216(1).mp4")  # Cambia esta ruta por la correcta de tu video
    
    # Mostrar la ventana de opciones después del video
    opciones()

    # Aquí iría el resto del código del juego si elige "PLAY"
    pygame.quit()
