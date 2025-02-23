import pygame

pygame.init()  # Inicializa Pygame
pygame.font.init()  # 🔹 Inicializa el módulo de fuentes

# Ahora ya puedes cargar fuentes sin problemas
front_inicio = pygame.font.Font("Font/Minecraft.ttf", 25)
small_font = pygame.font.Font(None, 30)

WIDTH = 800   # Ancho de la ventana
HEIGHT = 600 # Alto de la ventana

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

