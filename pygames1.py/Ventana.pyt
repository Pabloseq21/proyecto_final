import pygame
import firebase_admin
from firebase_admin import credentials, db
import firebase_admin.auth as auth
import constantes  # Importar constantes desde el otro archivo

# Inicializa Firebase
cred = credentials.Certificate("testpython-673c0-firebase-adminsdk-b93r7-bd9607d785.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://testpython-673c0-default-rtdb.firebaseio.com/'
})

# Inicializa Pygame
pygame.init()

# Configuración de la ventana
screen = pygame.display.set_mode((300, 400))
pygame.display.set_caption("Inicio de Sesión")

# Colores
ACTIVE_COLOR = (constantes.GRIS)  # Color cuando el campo está activo
INACTIVE_COLOR = (constantes.BLANCO)  # Color cuando el campo no está activo

# Fuentes
font = constantes.front_inicio

# Variables de estado
text_nombre = ""
text_contraseña = ""
active_input = None  # None, 'nombre', or 'contrañesa'

# Funciones para manejar el inicio de sesión y registro
def login(nombre, contraseña):
    ref = db.reference('users')
    usuarios = ref.get()

    for usuario_id, usuario_data in usuarios.items():
        if usuario_data['display_name'] == nombre and usuario_data['contraseña'] == contraseña:
            print(f"Inicio de sesión exitoso para: {nombre}")
            return True

    print("Error en el inicio de sesión: Credenciales incorrectas")
    return False

def register(email, nombre, contraseña):

    ref = db.reference('users')
    usuarios = ref.get()

    for usuario_id, usuario_data in usuarios.items():

        #Verificar si ya existe un usuario con ese nombre o correo

        if usuario_data['display_name'] == nombre or usuario_data['email'] == email:

            print("El usuario o correo ya existe")
            return False
        else:
            usuario_data = {
                "email": email,
                "password": contraseña,
                "display_name": nombre
            }

            db.reference('users').push(usuario_data)
            print(f"Usuario registrado con correo: {email}")

# Bucle principal
running = True
while running:
    screen.fill(constantes.NEGRO)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            # Verificar si se hace clic en los campos de entrada
            input_box_username = pygame.Rect(50, 80, 200, 40)
            input_box_password = pygame.Rect(50, 150, 200, 40)
            if input_box_username.collidepoint(mouse_pos):
                active_input = "nombre"
                print("seleccion label nombre")
            elif input_box_password.collidepoint(mouse_pos):
                active_input = "contraseña"
                print("seleccion label contraseña")
            else:
                active_input = None
                print("seleccion label nada")

    # Manejo de entrada de texto
        elif event.type == pygame.KEYDOWN:
            print("escribiendo")
            if event.key == pygame.K_RETURN:
                if login(text_nombre, text_contraseña) == True:

                    # Redirijir a pagina principal ESTO ES IMPORTANTE

                    print("redirijiendo")
            elif event.key == pygame.K_BACKSPACE:
                print("borrando")
                if active_input == "nombre":
                    text_nombre = text_nombre[:-1]
                    print("nombre")
                elif active_input == "contraseña":
                    text_contraseña = text_contraseña[:-1]
                    print("contraseña")
            else:
                print(event.unicode)
                if active_input == "nombre":
                    text_nombre += event.unicode
                    print("en el nombre")
                elif active_input == "contraseña":
                    text_contraseña += event.unicode
                    print("en la contraseña")

    # Mostrar etiquetas y campos de entrada
    username_label = font.render("Usuario", True, constantes.BLANCO)
    password_label = font.render("Contraseña", True, constantes.BLANCO)

    box_username = pygame.Rect(50,80, 200, 40)
    box_password = pygame.Rect(50,150, 200, 40)

    pygame.draw.rect(screen, ACTIVE_COLOR if active_input == "nombre" else INACTIVE_COLOR, box_username)
    pygame.draw.rect(screen, ACTIVE_COLOR if active_input == "contraseña" else INACTIVE_COLOR, box_password)

    input_surface = font.render(text_nombre, True, constantes.NEGRO)  # Renderizar el texto
    screen.blit(input_surface, (box_username.x + 5, box_username.y + 5))

    input_surface = font.render('*' * len(text_contraseña), True, constantes.NEGRO)  # Renderizar el texto
    screen.blit(input_surface, (box_password.x + 5, box_password.y + 5))

    screen.blit(username_label, (50, 50))
    screen.blit(password_label, (50, 120))

    pygame.display.flip()

pygame.quit()