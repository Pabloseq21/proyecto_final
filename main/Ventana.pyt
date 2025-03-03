import pygame
import firebase_admin
from firebase_admin import credentials, db
from main import menu_principal 

try:
    firebase_admin.get_app()  # Verifica si Firebase ya está inicializado
except ValueError:
    cred = credentials.Certificate("testpython-673c0-firebase-adminsdk-fbsvc-44c59768dc.json")
    firebase_admin.initialize_app(cred, {"databaseURL": "https://testpython-673c0-default-rtdb.firebaseio.com/"})
# Inicializar pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Inicio de Sesión")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (50, 150, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)

# Fuentes
front_inicio = pygame.font.Font("Font/Minecraft.ttf", 30)
small_font = pygame.font.Font(None, 30)



def login():
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
                        return True  
                    else:
                        error_message = "❌ Incorrect password."
                        return False

        error_message = "❌ We don't found an email in our database."
        show_register_button = True
        return False

    def register_user(email, password, name):
        nonlocal error_message, show_register_button
        ref = db.reference("users")
        new_user_ref = ref.push()
        new_user_ref.set({
            "email": email,
            "password": password,
            "display_name": name,
            "score": 0
        })
        error_message = "✅ Sign up successful!"
        show_register_button = False
        pygame.time.delay(1000)
        return True  

    running = True
    while running:
        screen.fill(BLACK)

        title = front_inicio.render("Inicio de Sesión", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        email_label = front_inicio.render("Email:", True, WHITE)
        password_label = front_inicio.render("Password:", True, WHITE)
        screen.blit(email_label, (200, 150))
        screen.blit(password_label, (200, 250))

        email_rect = pygame.Rect(350, 145, 300, 40)
        password_rect = pygame.Rect(350, 245, 300, 40)
        pygame.draw.rect(screen, GRAY, email_rect)
        pygame.draw.rect(screen, GRAY, password_rect)

        email_text = front_inicio.render(email_input, True, BLACK)
        password_text = front_inicio.render("*" * len(password_input), True, BLACK)
        screen.blit(email_text, (email_rect.x + 10, email_rect.y + 5))
        screen.blit(password_text, (password_rect.x + 10, password_rect.y + 5))

        login_rect = pygame.Rect(350, 350, 120, 50)
        pygame.draw.rect(screen, BLUE, login_rect)
        login_text = front_inicio.render("Login", True, WHITE)
        screen.blit(login_text, (login_rect.x + 20, login_rect.y + 10))

        register_rect = pygame.Rect(500, 350, 120, 50)
        if show_register_button:
            pygame.draw.rect(screen, GREEN, register_rect)
            register_text = front_inicio.render("Sign Up", True, WHITE)
            screen.blit(register_text, (register_rect.x + 10, register_rect.y + 10))

        if requesting_name:
            name_label = front_inicio.render("Name:", True, WHITE)
            screen.blit(name_label, (200, 300))
            name_rect = pygame.Rect(350, 295, 300, 40)
            pygame.draw.rect(screen, GRAY, name_rect)
            name_text = front_inicio.render(name_input, True, BLACK)
            screen.blit(name_text, (name_rect.x + 10, name_rect.y + 5))

        if error_message:
            error_color = RED if "❌" in error_message else GREEN
            error_text = small_font.render(error_message, True, error_color)
            screen.blit(error_text, (350, 420))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if email_rect.collidepoint(event.pos):
                    active_input = "email"
                elif password_rect.collidepoint(event.pos):
                    active_input = "password"
                elif requesting_name and name_rect.collidepoint(event.pos):
                    active_input = "name"
                elif login_rect.collidepoint(event.pos):
                    if authenticate_user(email_input, password_input):
                        pygame.quit()
                        menu_principal()  # Llamar al menú principal tras inicio de sesión exitoso
                        return
                elif show_register_button and register_rect.collidepoint(event.pos):
                    requesting_name = True  

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
                    if event.key == pygame.K_RETURN and name_input:
                        if register_user(email_input, password_input, name_input):
                            pygame.quit()
                            menu_principal()  # Llamar al menú principal tras registro exitoso
                            return

        pygame.display.flip()

    pygame.quit()
