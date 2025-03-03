import pygame
import firebase_admin
from firebase_admin import credentials, db
import firebase_admin.auth as auth
from moviepy import VideoFileClip  # Para reproducir el video
import constantes  # Importar constantes desde el otro archivo
import subprocess

pygame.init()  # Iniciar pygame

# Inicializar Firebase
cred = credentials.Certificate(r"testpython-673c0-firebase-adminsdk-fbsvc-cfdb9b6a07.json")  #tienen que descargar la llave en firebase, cada que se hace un commit dejarla en el gitignore
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://testpython-673c0-default-rtdb.firebaseio.com/'
})

vent = pygame.display.set_mode((constantes.WIDTH, constantes.HEIGHT))
pygame.display.set_caption("Pac-man")

# Botones
boton_start = pygame.Rect(constantes.WIDTH / 2 - 100, constantes.HEIGHT / 2 - 50, 200, 50)
boton_exit = pygame.Rect(constantes.WIDTH / 2 - 100, constantes.HEIGHT / 2 + 50, 200, 50)

# Funciones auxiliares
def color_bot(button_rect):
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        return (255, 255, 255, 64)  # blanco con transparencia (alfa 128)
    else:
        return (0, 0, 0, 0)  # Transparente (alfa 0) cuando el mouse no está sobre el botón

def get_text_width_height(text, font):
    text_surface = font.render(text, True, (255, 255, 255))
    return text_surface.get_width(), text_surface.get_height()

def dibujar_boton(texto, x, y, font):
    width, height = get_text_width_height(texto, font)
    button_rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
    color = color_bot(button_rect)
    surface_boton = pygame.Surface(button_rect.size, pygame.SRCALPHA)
    surface_boton.fill(color)
    vent.blit(surface_boton, button_rect.topleft)
    text_surface = font.render(texto, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=button_rect.center)
    vent.blit(text_surface, text_rect)

def play_intro_video(video_path):
    video = VideoFileClip(video_path)
    video_width, video_height = video.size
    scale = min(constantes.WIDTH / video_width, constantes.HEIGHT / video_height)
    new_width = int(video_width * scale)
    new_height = int(video_height * scale)
    x_offset = (constantes.WIDTH - new_width) // 2
    y_offset = (constantes.HEIGHT - new_height) // 2
    clock = pygame.time.Clock()
    for frame in video.iter_frames(fps=60, with_times=False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        frame_surface = pygame.transform.scale(frame_surface, (new_width, new_height))
        vent.fill((0, 0, 0))
        vent.blit(frame_surface, (x_offset, y_offset))
        pygame.display.update()
        clock.tick(30)
    video.close()

def obtener_puntajes():
    try:
        ref = db.reference('users')
        usuarios = ref.get()
        if usuarios:
            print("Usuarios obtenidos de Firebase:")
            for usuario_id, usuario_data in usuarios.items():
                print(f"ID: {usuario_id}, Nombre: {usuario_data.get('display_name')}, Puntuación: {usuario_data.get('score')}")
        else:
            print("No se encontraron usuarios en la base de datos.")
        puntajes = [(usuario_data.get('display_name', 'Desconocido'), usuario_data.get('score', 0)) for usuario_data in usuarios.values()]
        puntajes.sort(key=lambda x: x[1], reverse=True)
        return puntajes
    except Exception as e:
        print(f"Error al obtener puntajes de Firebase: {e}")
        return []

def ventana_top_scores():
    puntajes = obtener_puntajes()
    ventana_scores = True
    while ventana_scores:
        vent.fill((0, 0, 0))
        mostrar_titulo = constantes.front_inicio.render("Top Scores", True, (255, 255, 255))
        vent.blit(mostrar_titulo, (constantes.WIDTH / 2 - mostrar_titulo.get_width() / 2, 50))
        y_offset = 150
        for display_name, score in puntajes:
            texto = f"{display_name}: {score}"
            texto_score = constantes.front_inicio.render(texto, True, (255, 255, 255))
            vent.blit(texto_score, (constantes.WIDTH / 2 - texto_score.get_width() / 2, y_offset))
            y_offset += 40
        boton_exit = pygame.Rect(constantes.WIDTH / 2 - 100, constantes.HEIGHT - 100, 200, 50)
        dibujar_boton("EXIT", boton_exit.centerx, boton_exit.centery, constantes.front_inicio)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ventana_scores = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_exit.collidepoint(event.pos):
                    ventana_scores = False
                    menu_principal()
        pygame.display.flip()

def ventana_multiplayer_opciones():
    run = True
    while run:
        vent.fill((0, 0, 0))
        mensaje = constantes.front_inicio.render("Multiplayer Options", True, (255, 255, 255))
        vent.blit(mensaje, (constantes.WIDTH / 2 - mensaje.get_width() / 2, 50))
        boton_online = pygame.Rect(constantes.WIDTH / 2 - 100, constantes.HEIGHT / 2 - 50, 200, 50)
        boton_local = pygame.Rect(constantes.WIDTH / 2 - 100, constantes.HEIGHT / 2 + 50, 200, 50)
        boton_exit = pygame.Rect(constantes.WIDTH / 2 - 100, constantes.HEIGHT / 2 + 150, 200, 50)
        dibujar_boton("Online", boton_online.centerx, boton_online.centery, constantes.front_inicio)
        dibujar_boton("Local", boton_local.centerx, boton_local.centery, constantes.front_inicio)
        dibujar_boton("EXIT", boton_exit.centerx, boton_exit.centery, constantes.front_inicio)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_online.collidepoint(event.pos):
                    subprocess.run(["python", "1v1online.py"])
                    pass
                elif boton_local.collidepoint(event.pos):
                    subprocess.run(["python", "1v1local.py"])
                    pass
                elif boton_exit.collidepoint(event.pos):
                    run = False
                    ventana_online_opciones()
        pygame.display.flip()

def ventana_online_opciones():
    run = True
    while run:
        vent.fill((0, 0, 0))
        mensaje = constantes.front_inicio.render("Choose an Option", True, (255, 255, 255))
        vent.blit(mensaje, (constantes.WIDTH / 2 - mensaje.get_width() / 2, 50))
        boton_multiplayer = pygame.Rect(constantes.WIDTH / 2 - 100, constantes.HEIGHT / 2 - 50, 200, 50)
        boton_single_player = pygame.Rect(constantes.WIDTH / 2 - 100, constantes.HEIGHT / 2 + 50, 200, 50)
        boton_exit = pygame.Rect(constantes.WIDTH / 2 - 100, constantes.HEIGHT / 2 + 150, 200, 50)
        dibujar_boton("Multiplayer", boton_multiplayer.centerx, boton_multiplayer.centery, constantes.front_inicio)
        dibujar_boton("Single player", boton_single_player.centerx, boton_single_player.centery, constantes.front_inicio)
        dibujar_boton("EXIT", boton_exit.centerx, boton_exit.centery, constantes.front_inicio)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_multiplayer.collidepoint(event.pos):
                    ventana_multiplayer_opciones()
                elif boton_single_player.collidepoint(event.pos):
                    seleccionar_mapa()
                elif boton_exit.collidepoint(event.pos):
                    run = False
                    menu_principal()
        pygame.display.flip()

def seleccionar_mapa():
    seleccionando_mapa = True
    while seleccionando_mapa:
        vent.fill((0, 0, 0))
        mensaje = constantes.front_inicio.render("Elije el mapa", True, (255, 255, 255))
        vent.blit(mensaje, (constantes.WIDTH / 2 - mensaje.get_width() / 2, 50))
        boton_mapa_1 = pygame.Rect(constantes.WIDTH / 2 - 100, constantes.HEIGHT / 2 - 50, 200, 50)
        boton_mapa_2 = pygame.Rect(constantes.WIDTH / 2 - 100, constantes.HEIGHT / 2 , 200, 50)
        boton_mapa_3 = pygame.Rect(constantes.WIDTH / 2 - 100, constantes.HEIGHT / 2 + 50, 200, 50)
        boton_exit = pygame.Rect(constantes.WIDTH / 2 - 100, constantes.HEIGHT / 2 + 150, 200, 50)
        dibujar_boton("Mapa 1", boton_mapa_1.centerx, boton_mapa_1.centery, constantes.front_inicio)
        dibujar_boton("Mapa 2", boton_mapa_2.centerx, boton_mapa_2.centery, constantes.front_inicio)
        dibujar_boton("Mapa 3", boton_mapa_3.centerx, boton_mapa_3.centery, constantes.front_inicio)
        dibujar_boton("EXIT", boton_exit.centerx, boton_exit.centery, constantes.front_inicio)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                seleccionando_mapa = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_mapa_1.collidepoint(event.pos):
                    subprocess.run(["python", "juego.py"])
                elif boton_mapa_2.collidepoint(event.pos):
                    subprocess.run(["python", "juego2.py"])
                elif boton_mapa_3.collidepoint(event.pos):
                    subprocess.run(["python", "juego3.py"])
                elif boton_exit.collidepoint(event.pos):
                    seleccionando_mapa = False
                    ventana_online_opciones()
                    
        pygame.display.flip()

def login():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Login")
    font = pygame.font.Font(None, 36)
    email_input = ""
    password_input = ""
    name_input = ""
    active_input = None
    error_message = ""
    show_register_button = False
    requesting_name = False

    def authenticate_user(email, password):
        nonlocal error_message, show_register_button
        ref = db.reference("users").get()
        if ref:
            for user_id, user_data in ref.items():
                if user_data.get("email") == email:
                    if user_data.get("password") == password:
                        error_message = "✅ Sign in successful!"
                        show_register_button = False
                        pygame.time.delay(1000)
                        menu_principal()
                        return True
                    else:
                        error_message = "❌ Incorrect password."
                        return False
        error_message = "❌ Email not found in database."
        show_register_button = True
        return False

    running = True
    while running:
        screen.fill((0, 0, 0))
        title = font.render("Inicio de Sesión", True, (255, 255, 255))
        screen.blit(title, (300, 50))
        email_label = font.render("Email:", True, (255, 255, 255))
        password_label = font.render("Password:", True, (255, 255, 255))
        screen.blit(email_label, (200, 150))
        screen.blit(password_label, (200, 250))
        email_rect = pygame.Rect(350, 145, 300, 40)
        password_rect = pygame.Rect(350, 245, 300, 40)
        pygame.draw.rect(screen, (150, 150, 150), email_rect)
        pygame.draw.rect(screen, (150, 150, 150), password_rect)
        email_text = font.render(email_input, True, (0, 0, 0))
        password_text = font.render("*" * len(password_input), True, (0, 0, 0))
        screen.blit(email_text, (email_rect.x + 10, email_rect.y + 5))
        screen.blit(password_text, (password_rect.x + 10, password_rect.y + 5))
        login_rect = pygame.Rect(350, 350, 120, 50)
        pygame.draw.rect(screen, (0, 0, 255), login_rect)
        login_text = font.render("Login", True, (255, 255, 255))
        screen.blit(login_text, (login_rect.x + 20, login_rect.y + 10))
        register_rect = pygame.Rect(500, 350, 120, 50)
        if show_register_button:
            pygame.draw.rect(screen, (0, 255, 0), register_rect)
            register_text = font.render("Sign Up", True, (255, 255, 255))
            screen.blit(register_text, (register_rect.x + 10, register_rect.y + 10))
        
        # Add Back button
        back_rect = pygame.Rect(50, 50, 100, 50)
        pygame.draw.rect(screen, (255, 0, 0), back_rect)
        back_text = font.render("Back", True, (255, 255, 255))
        screen.blit(back_text, (back_rect.x + 10, back_rect.y + 10))
        
        if error_message:
            error_color = (255, 0, 0) if "❌" in error_message else (0, 255, 0)
            error_text = font.render(error_message, True, error_color)
            screen.blit(error_text, (350, 420))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if email_rect.collidepoint(event.pos):
                    active_input = "email"
                elif password_rect.collidepoint(event.pos):
                    active_input = "password"
                elif login_rect.collidepoint(event.pos):
                    if authenticate_user(email_input, password_input):
                        return
                elif show_register_button and register_rect.collidepoint(event.pos):
                    requesting_name = True
                elif back_rect.collidepoint(event.pos):
                    opciones_login_register()
                    return
            if event.type == pygame.KEYDOWN:
                if active_input == "email":
                    if event.key == pygame.K_BACKSPACE:
                        email_input = email_input[:-1]
                    else:
                        email_input += event.unicode
                elif active_input == "password":
                    if event.key == pygame.K_BACKSPACE:
                        password_input = password_input[:-1]
                    else:
                        password_input += event.unicode
        pygame.display.flip()
    pygame.quit()

def register():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Register")
    font = pygame.font.Font(None, 36)
    email_input = ""
    password_input = ""
    name_input = ""
    active_input = None
    error_message = ""

    def register_user(email, password, name):
        nonlocal error_message
        try:
            ref = db.reference("users")
            new_user_ref = ref.push()
            new_user_ref.set({
                "email": email,
                "password": password,
                "display_name": name,
                "score": 0
            })
            error_message = "✅ Sign up successful!"
            pygame.time.delay(1000)
            menu_principal()
            return True
        except Exception as e:
            error_message = f"❌ Error: {e}"
            return False

    running = True
    while running:
        screen.fill((0, 0, 0))
        title = font.render("Registro", True, (255, 255, 255))
        screen.blit(title, (300, 50))
        email_label = font.render("Email:", True, (255, 255, 255))
        password_label = font.render("Password:", True, (255, 255, 255))
        name_label = font.render("Name:", True, (255, 255, 255))
        screen.blit(email_label, (200, 150))
        screen.blit(password_label, (200, 250))
        screen.blit(name_label, (200, 350))
        email_rect = pygame.Rect(350, 145, 300, 40)
        password_rect = pygame.Rect(350, 245, 300, 40)
        name_rect = pygame.Rect(350, 345, 300, 40)
        pygame.draw.rect(screen, (150, 150, 150), email_rect)
        pygame.draw.rect(screen, (150, 150, 150), password_rect)
        pygame.draw.rect(screen, (150, 150, 150), name_rect)
        email_text = font.render(email_input, True, (0, 0, 0))
        password_text = font.render("*" * len(password_input), True, (0, 0, 0))
        name_text = font.render(name_input, True, (0, 0, 0))
        screen.blit(email_text, (email_rect.x + 10, email_rect.y + 5))
        screen.blit(password_text, (password_rect.x + 10, password_rect.y + 5))
        screen.blit(name_text, (name_rect.x + 10, name_rect.y + 5))
        register_rect = pygame.Rect(350, 450, 120, 50)
        pygame.draw.rect(screen, (0, 255, 0), register_rect)
        register_text = font.render("Sign Up", True, (255, 255, 255))
        screen.blit(register_text, (register_rect.x + 10, register_rect.y + 10))
        
        # Add Back button
        back_rect = pygame.Rect(50, 50, 100, 50)
        pygame.draw.rect(screen, (255, 0, 0), back_rect)
        back_text = font.render("Back", True, (255, 255, 255))
        screen.blit(back_text, (back_rect.x + 10, back_rect.y + 10))
        
        if error_message:
            error_color = (255, 0, 0) if "❌" in error_message else (0, 255, 0)
            error_text = font.render(error_message, True, error_color)
            screen.blit(error_text, (350, 520))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if email_rect.collidepoint(event.pos):
                    active_input = "email"
                elif password_rect.collidepoint(event.pos):
                    active_input = "password"
                elif name_rect.collidepoint(event.pos):
                    active_input = "name"
                elif register_rect.collidepoint(event.pos):
                    if register_user(email_input, password_input, name_input):
                        return
                elif back_rect.collidepoint(event.pos):
                    opciones_login_register()
                    return
            if event.type == pygame.KEYDOWN:
                if active_input == "email":
                    if event.key == pygame.K_BACKSPACE:
                        email_input = email_input[:-1]
                    else:
                        email_input += event.unicode
                elif active_input == "password":
                    if event.key == pygame.K_BACKSPACE:
                        password_input = password_input[:-1]
                    else:
                        password_input += event.unicode
                elif active_input == "name":
                    if event.key == pygame.K_BACKSPACE:
                        name_input = name_input[:-1]
                    else:
                        name_input += event.unicode
        pygame.display.flip()
    pygame.quit()

def menu_principal():
    fondo_imagen = pygame.image.load(r"assents/images/puck/P U C K.jpg")
    fondo_imagen = pygame.transform.scale(fondo_imagen, (constantes.WIDTH, constantes.HEIGHT))
    boton_play = pygame.Rect(constantes.WIDTH / 2 - 100, constantes.HEIGHT / 2 - 100, 200, 50)
    boton_top_scores = pygame.Rect(constantes.WIDTH / 2 - 100, constantes.HEIGHT / 2, 200, 50)
    boton_exit = pygame.Rect(constantes.WIDTH / 2 - 100, constantes.HEIGHT / 2 + 100, 200, 50)
    run = True
    while run:
        vent.blit(fondo_imagen, (0, 0))
        dibujar_boton("PLAY", boton_play.centerx, boton_play.centery, constantes.front_inicio)
        dibujar_boton("TOP SCORES", boton_top_scores.centerx, boton_top_scores.centery, constantes.front_inicio)
        dibujar_boton("EXIT", boton_exit.centerx, boton_exit.centery, constantes.front_inicio)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_play.collidepoint(event.pos):
                    ventana_online_opciones()  # Llama directamente a ventana_online_opciones
                    run = False
                elif boton_top_scores.collidepoint(event.pos):
                    print("Mostrando puntajes más altos...")
                    ventana_top_scores()
                elif boton_exit.collidepoint(event.pos):
                    print("Volviendo al menú de opciones...")
                    opciones()
                    run = False
        pygame.display.flip()

def opciones_login_register():
    fondo_imagen = pygame.image.load(r"assents/images/puck/P U C K (2).jpg")
    fondo_imagen = pygame.transform.scale(fondo_imagen, (constantes.WIDTH, constantes.HEIGHT))
    run = True
    while run:
        vent.blit(fondo_imagen, (0, 0))
        boton_login = pygame.Rect(constantes.WIDTH / 2 - 100, constantes.HEIGHT / 2 - 50, 200, 50)
        boton_signup = pygame.Rect(constantes.WIDTH / 2 - 100, constantes.HEIGHT / 2 + 50, 200, 50)
        dibujar_boton("LOGIN", boton_login.centerx, boton_login.centery, constantes.front_inicio)
        dibujar_boton("SIGN UP", boton_signup.centerx, boton_signup.centery, constantes.front_inicio)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_login.collidepoint(event.pos):
                    run = False
                    login()
                elif boton_signup.collidepoint(event.pos):
                    run = False
                    register()
        pygame.display.flip()

def opciones():
    fondo_imagen = pygame.image.load(r"assents/images/puck/P U C K (2).jpg")
    fondo_imagen = pygame.transform.scale(fondo_imagen, (constantes.WIDTH, constantes.HEIGHT))
    run = True
    while run:
        vent.blit(fondo_imagen, (0, 0))
        dibujar_boton("START", boton_start.centerx, boton_start.centery, constantes.front_inicio)
        dibujar_boton("EXIT", boton_exit.centerx, boton_exit.centery, constantes.front_inicio)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_start.collidepoint(event.pos):
                    run = False
                    opciones_login_register()
                elif boton_exit.collidepoint(event.pos):
                    pygame.quit()
                    run = False
        pygame.display.flip()

if __name__ == "__main__":
    play_intro_video(r"assents/videos/0216(1).mp4")
    opciones()
    pygame.quit()


