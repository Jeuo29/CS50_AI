![BFS](https://github.com/user-attachments/assets/9bb539d5-b511-4720-a3b7-8acd31aa65ba)
# *CS50's* Introducción a la Inteligencia Artificial con python 

En el siguiente curso nos vamos a introducir, explorar y comprender los conceptos y algoritmos que constituyen la base de lo que hoy en dia conocemos como inteligencia artificial. El curso se encuentra dividido en siete semanas, donde en cada una de ellas se introduce y explora lo básico de cada una de las grandes areas que comprende la inteligencia artificial. 

El objetivo principal sera la completa comprensión de los algoritmos y el problema que se presenta, esto acompañado del desafió de implementar todo correctamente en python.  

## Semana 0: Búsqueda 

En la  vida real para poder encontrar una solución de un problema, muchas veces se requiere de una previa búsqueda de posibles soluciones. En la primera semana se exploran algunos algoritmos que nos permiten en base a una estructura de grafos buscar posibles soluciones a problemas. 

A continuación se presenta una introducción a los proyectos:

### **Proyecto 1**: Degrees 

En este proyecto nos interesa implementar el juego Six Degrees of Kevin Bacon. Este es un juego divertido en el que conectas a dos actores cualquiera a través de sus papeles cinematográficos. El objetivo es completar este proceso en el menor número de pasos posible. Aquí nuestro trabajo sera completar la función shortest_path que es una implementación del algoritmo de búsqueda en anchura que se ve a continuación: 

![hola mundo](BFS.png)


### **Proyecto 2**: TicTacToe

En este proyecto nos interesa implementar el juego Tic Tac toe. Este es un juego divertido en una cuadrícula de 3x3, donde los jugadores toman turnos marcando los espacios con X o O en un intento de obtener tres en una fila, ya sea horizontal, vertical o diagonalmente. El objetivo del juego es conseguir tres X u O seguidas antes que tu oponente. Aquí nuestro trabajo sera completar 7 funciones que representan diversas facetas del juego, donde la principal función es la implementación del algoritmo minimax que sera aquella que le permita al programa calcular el mejor posible movimiento. El algoritmo requerido para la implementación del código es el siguiente:

![hola mundo](MinMax.png)

## Semana 1: Conocimiento  

El concepto de inteligencia a menudo viene muy fuertemente correlacionado con el concepto de conocimiento, esto quiere decir, que mientras un individuo posea mas conocimiento entonces, el individuo debería ser más inteligente. Por lo tanto, el objetivo de esta semana es construir un agente inteligente capaz de razonar y sacar conclusiones sobre información que conoce para descubrir como realizar una tarea.

Para la construcción de estos agentes haremos uso de sistemas lógicos-matemáticos formales como los son: 

1) La lógica proposicional: Es un sistema formado por proposiciones que hace uso de conectores lógicos que representan operaciones son capaces de formar proposiciones de mayor complejidad. 
2) La lógica de primer orden: Diseñado para estudiar la inferencia en los lenguajes de primer orden. Los lenguajes de primer orden son más expresivos que los lenguajes proposicionales, ya que permiten cuantificar sobre objetos y relaciones. Todo esto permite hacer afirmaciones sobre individuos y sus relaciones, lo cual lo hace ideal para modelar el mundo real.

A continuación se presenta una introducción a los proyectos:

### **Proyecto 1**: Knights

En este proyecto nos interesa implementar el juego o acertijo lógico de Caballeros y Bribones. El juego consiste en que te encuentras en una isla poblada por dos tipos de personas: caballeros y bribones. Los caballeros siempre dicen la verdad, mientras que los bribones siempre mienten. No hay forma de distinguirlos por su apariencia o comportamiento y basado en la información que te dicen las personas se busca realizar inferencia lógica para averiguar a que tipo de persona pertenece cada jugador.

Para este proyecto haremos uso de un sistema lógico: La lógica proposicional. Ahora recordemos cuales son sus conectores lógicos:

| Conector    | Símbolo          |
|:-----------:|:----------------:|
|   And       |    $\wedge$      |
|   Or        |    $\vee$        |
|implication  | $\rightarrow$    |
|biconditional| $\leftrightarrow$|

Ademas de conocer las reglas de inferencia, algunas serán listadas a continuación:

1) Modus Ponens 
2) And Elimination
3) Double Negation Elimination 
4) Implication Elimination 
5) Biconditional Elimination 
6) De Morgan's Law
7) Distributive Property 

### **Proyecto 2**: Minesweeper

En este proyecto nos interesa implementar el juego Buscaminas. Buscaminas es un clásico juego de computadora que consiste en encontrar todas las minas ocultas en un tablero cuadriculado sin hacer explotar ninguna.

Al inicio se presenta un tablero con casillas ocultas. Algunas de estas casillas contienen minas. Si haces clic en una casilla, esta se revela. Si hay una mina, pierdes la partida. Si la casilla revelada no tiene una mina, aparecerá un número. Este número indica cuántas minas hay en las 8 casillas adyacentes. Al sospechar que una casilla tiene una mina, puedes marcarla con una bandera y ganas la partida cuando has descubierto todas las casillas que no tienen minas.















