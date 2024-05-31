import numpy as numpy # Utilizamos numpy para facilitar la creacion de la matriz tablero
import pygame

#--------------------------------------------LOGICAS NECESARIAS-----------------------------------------------------------#
# Crear el tablero (tamano ajustable)
tamano = 5
tablero = numpy.zeros((tamano, tamano), dtype=int)

# Posiciones iniciales
posicion_gato = (0, 0)  # Gato en la esquina superior izquierda
posicion_raton = (tamano-1, tamano-1)  # Raton en la esquina inferior derecha

# Representacion en el tablero
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
#--------------------------------------------CUERPO PRINCIPAL-----------------------------------------------------------#
# Función principal para ejecutar el juego
def ejecutar_juego(posicion_gato, posicion_raton, depth):
    print('''El juego del gato y del raton:
- El raton escapa y el gato persigue''') # Titulo

    turno_raton = True  # Empieza el raton

    while depth > 0 and posicion_gato != posicion_raton:

        imprimir_tablero(tablero)

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
        depth = depth - 1

        # Actualizamos el tablero
        tablero.fill(0)
        tablero[posicion_gato] = 1
        tablero[posicion_raton] = 2

    imprimir_tablero(tablero)

    # Determinamos los casos posibles de finalizacion
    if depth == 0:
        print("Se han acabado los turnos; El raton gana!")
    elif posicion_gato == posicion_raton:
        print("El gato atrapo al raton; El gato gana!")

# Ejecutamos el juego y definimos profundidad
ejecutar_juego(posicion_gato, posicion_raton, 10)  # Profundidad de búsqueda = 6
