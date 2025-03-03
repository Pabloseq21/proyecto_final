import pygame
import os

pygame.init()  # Inicializa Pygame
pygame.font.init()  # 🔹 Inicializa el módulo de fuentes

# Ahora ya puedes cargar fuentes sin problemas
front_inicio = pygame.font.Font("assents/Font/Minecraft.ttf", 25)
small_font = pygame.font.Font(None, 30)
ruta_fuente = os.path.join(os.path.dirname(__file__), "assents", "Font", "Minecraft.ttf")
front_inicio = pygame.font.Font(ruta_fuente, 25)
try:
    front_inicio = pygame.font.Font(ruta_fuente, 25)
    print("Fuente cargada correctamente.")
except Exception as e:
    print(f"Error al cargar la fuente: {e}")
    
WIDTH = 800   # Ancho de la ventana
HEIGHT = 600        # Alto de la ventana

# tamano ventana
WIDTH_VENTANA = 200
HEIGHT_VENTANA = 300

#colores 
BLANCO = (255,255,255)
NEGRO = (0,0,0)
CYAN = (0,255,255)
MORADO = (138,43,226)
TRANSPARENTE = (0,0,0,0)
LIGHT_BLUE = (100, 100, 255)
BLUE = (0, 0, 255)

