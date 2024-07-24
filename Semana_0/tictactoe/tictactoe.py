"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

## La siguiente función determina de quien es el turno dado un tablero, teniendo en cuenta que siempre juegan primero la X.

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    ## La función toma como parámetro un tablero. Se inicia un contador que determinará 
    ## el numero de espacios vacíos en el tablero. Si el contador es un numero impar la función 
    ## devolverá X sino devolverá O.
    contador = 0
    for fila in board:
        for casilla in fila:
            if casilla is None:
                contador += 1
    juega = X if contador % 2 != 0 else O
    return juega

## La siguiente función determinara todos los posibles movimientos que sean validos dado un tablero

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    ## La función toma como parámetro un tablero. Se crea un conjunto vació donde se guardaran los resultados y
    ## se recorre todo el tablero buscando casillas vacías y si se encuentran se agregan al conjunto.
    conjunto=set()
    row=0
    for fila in board:
        colum=0
        for casilla in fila:
            if casilla == None:
                conjunto.add((row,colum))
            colum += 1
        row += 1
    return conjunto

## La siguiente función determina un nuevo tablero luego de que se realiza una acción sobre el anterior

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    ## La función toma como parámetros un tablero y una acción (i,j)-esima, si no es posible realizar la acción
    ## por no pertenecer al conjunto de acciones posibles, entonces se toma como movimiento no valido. De no ser asi,
    ## se crea una copia para operar con ella, se determina de quien es el turno y por ultimo según de quien fuera el turno se 
    ## reemplaza una X o un O en el (i,j)-esimo espacio.
    if action not in actions(board):
         raise NameError('No puede realizar ese movimiento, casilla ocupada')
    else:
        new_board=copy.deepcopy(board)
        turno=player(new_board)
        row, colum = action
        new_board[row][colum]=turno
    return new_board

## La siguiente función determina si hay un ganador 

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    ## La función toma como parámetro un tablero, recorre todas las filas, columnas y diagonales. Si existe alguna que tenga 
    ## en todas los mismos elementos devuelve que el ganador es ese elemento. Si no hay ganador retorna None. 
    if actions(board) != set():
        for row in board:
            if row == [X,X,X] or row == [O,O,O]:
                return row[0]

        for i, row in enumerate(board):
            columna = []
            for j, col in enumerate(row):
                columna.append(board[j][i])
            if columna == [X,X,X] or columna == [O,O,O]:
                return columna[0]

        diagonal1=[]
        diagonal2=[]
        for i, row in enumerate(board):
            diagonal1.append(row[i])
            diagonal2.append(row[2-i])
        if diagonal1 == [X,X,X] or diagonal1 == [O,O,O]:
            return diagonal1[0]
        elif diagonal2 == [X,X,X] or diagonal2 == [O,O,O]:
            return diagonal2[0]
    else:
        return None

## Es una función que determina si el juego ha acabado

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    ## La función toma como parámetro un tablero, recorre todo el tablero contando las casillas vacías
    ## si no hay casillas vacías o Hay un ganador, entonces el juego ha acabado, si no ocurre ninguna de 
    ## estas entonces el juego no ha acabado.
    contador=0
    for row in board:
        for col in row:
            if col == None:
                contador +=1
    desicion = winner(board)
    if desicion == X or desicion == O:
        return True
    elif contador == 0:
        return True
    else:
        return False

## Esta función asigna un numero dependiendo de quien haya ganado el juego

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    ## Asigna el numero 1 si "X" gana el juego, asigna el numero -1 si "O" gana el juego y
    ## asigna el numero 0 si ninguno gana.
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

## Esta función es la implementación del algoritmo minimax que se muestra en el archivo README.md

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    def max_valor(board):
        mejor_movimiento = ()
        if terminal(board):
            return utility(board), mejor_movimiento
        else:
            v = -5
            for accion in actions(board):
                valor_minimo = min_valor(result(board, accion))[0]
                if valor_minimo > v:
                    v = valor_minimo
                    mejor_movimiento = accion
            return v, mejor_movimiento

    def min_valor(board):
        mejor_movimiento = ()
        if terminal(board):
            return utility(board), mejor_movimiento
        else:
            v = 5
            for accion in actions(board):
                valor_maximo = max_valor(result(board, accion))[0]
                if valor_maximo < v:
                    v = valor_maximo
                    mejor_movimiento = accion
            return v, mejor_movimiento

    jugador = player(board)

    if terminal(board):
        return None

    if jugador == X:
        return max_valor(board)[1]

    else:
        return min_valor(board)[1]

   