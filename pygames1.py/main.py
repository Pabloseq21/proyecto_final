import pygame 
import constantes          #Importar constantes desde el otro archivo 

pygame.init ()              #para iniciar 

#crear una ventana 
vent = pygame.display.set_mode((constantes.WIDTH,constantes.HEIGHT))     #crear una ventana con las medidas sobre el archivo de constantes
pygame.display.set_caption("Pac-man")           #Nombre de la ventana 

#Fuentes de pantalla de inicio
front_inicio = pygame.font.SysFont("Arial", 30)     #cambiar por font pac man
front_salir = pygame.font.SysFont("Arial", 30)
fornt_titulo = pygame.font.SysFont("Arial", 30)

#botones 
boton_jugar = pygame.Rect (constantes.WIDTH_VENTANA/ 2 + 200, constantes.HEIGHT_VENTANA / 2 + 50, 200, 50)
boton_opciones = pygame.Rect (constantes.WIDTH_VENTANA// 2 + 200, constantes.HEIGHT_VENTANA // 2 + 150, 200, 50)
boton_mapas = pygame.Rect (constantes.WIDTH_VENTANA/ 2 + 200, constantes.HEIGHT_VENTANA / 2 + 250, 200, 50)
boton_salir = pygame.Rect (constantes.WIDTH_VENTANA/ 2 + 200, constantes.HEIGHT_VENTANA / 2 + 350, 200, 50)


def color_bot(button_rect):                               #funcion para los botones cuando se pasa por ensima del mouse cambian de color 
    mouse_pos = pygame.mouse.get_pos()
    
    if button_rect.collidepoint(mouse_pos):  # Verifica si el mouse está sobre el botón
        return constantes.BLUE  # Cambia a azul si el mouse está sobre él
    else:
        return constantes.LIGHT_BLUE
    
# funcion para crear los botones
def dibujar_boton(texto, button_rect):  
    color = color_bot(button_rect)
    pygame.draw.rect(vent, color, button_rect)
    text_surface = front_inicio.render(texto, True, constantes.BLANCO)
    text_rect = text_surface.get_rect(center=button_rect.center)
    vent.blit(text_surface, text_rect)
    
#codigo para que el se mantenga avierto hasta que el usuario quiera salirse 
run = True 
while run == True :
    vent.fill((0,0,0))
    
    dibujar_boton("Jugar", boton_jugar)
    dibujar_boton("Opciones",boton_opciones)
    dibujar_boton("Mapas!",boton_mapas)
    dibujar_boton("Salir", boton_salir)

    
    for event in pygame.event.get ():
         if event.type == pygame.QUIT:
             run = False
         elif event.type == pygame.MOUSEBUTTONDOWN:
             if boton_jugar.collidepoint(event.pos):
                print ("¡Iniciar Juego!")
             if boton_opciones.collidepoint(event.pos):
                 print ("Menu de opcciones!")
             if boton_mapas.collidepoint(event.pos):
                 print ("Menu de mapas!")
             elif boton_salir.collidepoint(event.pos):
                pygame.quit()
    pygame.display.flip()           
pygame.QUIT