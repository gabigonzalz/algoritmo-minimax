import numpy as numpy # Utilizamos numpy para facilitar la creacion de la matriz tablero
import pygame # Utilizamos pygame para la parte visual del juego
import sys # Para acompanar a pygame y manejar la ventana del juego
import random # Para generar valores random

#--------------------------------------------LOGICAS NECESARIAS-----------------------------------------------------------#
# Crear el tablero (tamano ajustable)
tamano = 5
tablero = numpy.zeros((tamano, tamano), dtype=int)

# Función para calcular la distancia entre las dos posiciones iniciales
def distancia_inicial(posicion_inicial1, posicion_inicial2):
    return abs(posicion_inicial1[0] - posicion_inicial2[0]) + abs(posicion_inicial1[1] - posicion_inicial2[1])

# Generar 4 coordenadas iniciales
while True:
    posicion_random1 = random.randint(0, tamano-1)
    posicion_random2 = random.randint(0, tamano-1)
    posicion_random3 = random.randint(0, tamano-1)
    posicion_random4 = random.randint(0, tamano-1)
    
    # Deifinimos posiciones iniciales
    posicion_raton = (posicion_random1, posicion_random2)
    posicion_gato = (posicion_random3, posicion_random4)
    
    # Verificamos la distancia inicial mínima de 3 cuadros para mejor funcion del programa
    if distancia_inicial(posicion_raton, posicion_gato) >= 3:
        break

# Representacion de personajes en el tablero
tablero[posicion_gato] = 1  # 1 representa el gato
tablero[posicion_raton] = 2  # 2 representa el raton

def imprimir_tablero(tablero):
    print(tablero)
    print()

# Calculamos la distancia absoluta "abs()" (distancia directa entre las dos posiciones)
def distancia(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def movimientos_validos(posicion):
    y, x = posicion # Posicion del elemento
    movimientos = []
    if y > 0: # Si hay espacio arriba
        movimientos.append((y - 1, x))  # Mover arriba ^
    if y < tamano - 1: # Si hay espacio abajo
        movimientos.append((y + 1, x))  # Mover abajo v
    if x > 0: # Si hay espacio a la izquierda
        movimientos.append((y, x - 1))  # Mover izquierda <
    if x < tamano - 1: # Si hay espacio a la derecha
        movimientos.append((y, x + 1))  # Mover derecha >
    return movimientos # Retornamos los movimientos que el personaje PUEDE realizar

def minimax(posicion_gato, posicion_raton, depth, maximizando, alpha=float('-inf'), beta=float('inf')):
    # Si la profundidad del programa llega a cero o si el gato encuentra al raton
    if depth == 0:
        return distancia(posicion_gato, posicion_raton), None
    elif posicion_gato == posicion_raton:
        return distancia(posicion_gato, posicion_raton), None #DIstancia p/ especificar  a el programa el estado final del juego y None para especificar que no se realizara mas movimientos
    
    # Cuando el algoritmo este en MAX (raton)
    if maximizando:
        # Iniciamos con la menor evaluacion posible para buscar un valor mayor y maximizar
        max_eval = float('-inf') 
        mejor_movimiento = None # Declaramos la variable que adoptara el mejor movimiento
        
        # Evaluamos cada posibilidad con cada movimiento posible (raton)
        for mov in movimientos_validos(posicion_raton):
            # Ignoramos mejor_movimiento para priorizar eval
            # Valor de evaluacion de el posible movimiento actual (raton)
            # Comparamos con la posicion actual del gato y declaramos que el siguiente turno es del gato (False)
            eval, _ = minimax(posicion_gato, mov, depth - 1, False, alpha, beta)
            # Si la evaluacion actual es mayor a nuestra max evaluacion anterior la reemplazamos
            if eval > max_eval:
                max_eval = eval
                mejor_movimiento = mov
            # Guarda el mejor valor del raton
            # Guarda el mayor valor entre si y eval
            alpha = max(alpha, eval)
            # Si el raton ya tiene una mejor jugada garantiza anterior podamos las evaluaciones (Optimizaicon)
            if beta <= alpha:
                break
        return max_eval, mejor_movimiento # Retornamos mejor jugada para el raton
    
    else:
        # Iniciamos con la mayor evaluacion posible para buscar un valor mayor y maximizar
        min_eval = float('inf')
        mejor_movimiento = None # Declaramos devuelta

        # Evaluamos cada posibilidad con cada movimiento posible (gato)
        for mov in movimientos_validos(posicion_gato):
            # Ignoramos mejor_movimiento para priorizar eval
            # Valor de evaluacion de el posible movimiento actual (gato)
            # Comparamos con la posicion actual del raton y declaramos que el siguiente turno es del raton (True)
            eval, _ = minimax(mov, posicion_raton, depth - 1, True, alpha, beta)
            if eval < min_eval:
                min_eval = eval
                mejor_movimiento = mov
            # Mejor valor para el gato
            # Guarda el menor valor entre si y eval
            beta = min(beta, eval)
            # " " " " Se podan la evaluaciones (Optimizacion)
            if beta <= alpha:
                break
        return min_eval, mejor_movimiento # Retornamos mejor jugada para el gato

# ------------------------------------------Parte grafica (pygame)------------------------------------------------------#
# Inicializamos Pygame
pygame.init()

# Declaramos colores para poder llamarlos
GREEN = (204, 255, 153)
D_GREEN = (51, 153, 51)
DR_GREEN = (0, 102, 0)

# Tamaño de los bloques y configuración de la ventana
BLOCK_SIZE = 100
WIDTH = HEIGHT = tamano * BLOCK_SIZE # Un cuadrado ajustable a la cantidad de casillas
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("El gato y el raton")

# Cargar imágenes y darles un tamano
gato_img = pygame.image.load('gato.png')
raton_img = pygame.image.load('raton.png')
fondo_img = pygame.image.load('fondo.png')
gato_img = pygame.transform.scale(gato_img, (BLOCK_SIZE, BLOCK_SIZE))
raton_img = pygame.transform.scale(raton_img, (BLOCK_SIZE, BLOCK_SIZE))
fondo_img = pygame.transform.scale(fondo_img, (WIDTH, HEIGHT))

# Inicializar la fuente de pygame
pygame.font.init()
font_size = 20  # Ajustamos el tamano del texto
font_path = 'Subway-Black.ttf'  # Fuente personalizada
font = pygame.font.Font(font_path, font_size)

def draw_board():
    screen.blit(fondo_img, (0, 0)) # Llamamos a la imagen de fondo
    for row in range(tamano):
        for col in range(tamano):
            # Definimos las casillas y las dibujamos
            rect = pygame.Rect(col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, D_GREEN, rect, 1)

def draw_pieces(): # Busca las posiciones de cada animal y las dibuja
    for row in range(tamano):
        for col in range(tamano):
            if tablero[row][col] == 1:  # Gato
                screen.blit(gato_img, (col * BLOCK_SIZE, row * BLOCK_SIZE))
            elif tablero[row][col] == 2:  # Raton
                screen.blit(raton_img, (col * BLOCK_SIZE, row * BLOCK_SIZE))

def draw_text(text): # Renderizamos el texto
    text_surface = font.render(text, True, DR_GREEN)
    text_rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip() # Actualizamos la pantalla

#--------------------------------------------CUERPO PRINCIPAL-----------------------------------------------------------#
# Función principal para ejecutar el juego hasta que la profundidad llegue a 0
def ejecutar_juego(posicion_gato, posicion_raton, depth):
    print('''El juego del gato y del raton:
- El raton escapa y el gato persigue''')

    turno_raton = True  # Empieza el raton
    juego_terminado = False # Estado del juego
    mensaje = "" # Mensaje al final del juego

    while not juego_terminado: # Mientras juego_terminado != True
        for event in pygame.event.get(): # Revisa los eventos del juego
            if event.type == pygame.QUIT: # Si este es Quit entonces salir
                pygame.quit()
                sys.exit()

        # Mientras la profundidad del programa no sea 0 y el gato no atrapo al raton
        if depth > 0 and posicion_gato != posicion_raton:

            # Dependiendo del turno llamamos a la funcion minimax con True or False para especificar el gato o el raton
            if turno_raton:
                _, mejor_mov = minimax(posicion_gato, posicion_raton, depth, True)
                if mejor_mov:
                    posicion_raton = mejor_mov
            else:
                _, mejor_mov = minimax(posicion_gato, posicion_raton, depth, False)
                if mejor_mov:
                    posicion_gato = mejor_mov

            # Alternamos el turno
            turno_raton = not turno_raton
            depth =  depth - 1

            # Actualizamos el tablero
            tablero.fill(0)
            tablero[posicion_gato] = 1
            tablero[posicion_raton] = 2
            # LLamamos a las funciones visuales de pygame y refrescamos la pantalla
            draw_board()
            draw_pieces()
            pygame.display.flip()
            pygame.time.wait(500)

        # Si es que depth == 0 o el gato atrapo al raton
        else:
            juego_terminado = True # Avisamos que el juego se termino
            # Determinamos la causa de la finalizacion
            if depth == 0:
                print("Se han acabado los turnos; ¡El ratón gana!")
                mensaje = "Se han acabado los turnos; ¡El ratón gana!"
            elif posicion_gato == posicion_raton:
                print("El gato atrapo al raton; ¡El gato gana!")
                mensaje = "El gato atrapo al raton; ¡El gato gana!"
    
    draw_text(mensaje) # Mostramos el mensaje final
    pygame.time.wait(3000)  # 3 segundos antes de cerrar


# Ejecutamos el juego y definimos su profundidad
ejecutar_juego(posicion_gato, posicion_raton, 15)