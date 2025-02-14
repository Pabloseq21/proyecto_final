import pygame 
import constantes          #Importar constantes desde el otro archivo 

pygame.init ()              #para iniciar 


#crear una ventana 
vent = pygame.display.set_mode((constantes.WIDTH, constantes.HEIGHT))     #crear una ventana con las medidas que antes deniminamos
pygame.display.set_caption("Pac-man")           #Nombre de la ventana 

#Fuentes de pantalla de inicio
front_inicio = pygame.font.SysFont("Arial", 30)
front_salir = pygame.font.SysFont("Arial", 30)
fornt_titulo = pygame.font.SysFont("Arial", 30)

#Botones: crear los botones con las cordenadast y tamano
boton_jugar = pygame.Rect(constantes.WIDTH_VENTANA / 2 - 100, constantes.HEIGHT_VENTANA / 2 - 50, 200, 50)    
boton_salir = pygame.Rect(constantes.WIDTH_VENTANA / 2 - 100, constantes.HEIGHT_VENTANA / 2 + 50, 200, 50)

# texto en los botones 
text_boton_jugar = front_inicio.render ("Jugar.",True, constantes.BLANCO)
text_boton_salir = front_salir.render ("salir.", True, constantes.MORADO)

# pantalla de inicio 
def pantalla_inicio():
    vent.fill(constantes.BLANCO)
    pygame.draw.text("Pac-man",fornt_titulo, constantes.NEGRO, constantes.HEIGHT_VENTANA / 2 - 200, constantes.WIDTH_VENTANA / 2 - 200)
    pygame.draw.rect(vent,constantes.CYAN,boton_jugar)
#codigo para que el se mantenga avierto hasta que el usuario quiera salirse 
run = True 
while run == True :
     for event in pygame.event.get ():
         if event.type == pygame.QUIT:
             run = False 
pygame.QUIT