# *CS50's* Introducción a la Inteligencia Artificial con python 

En el siguiente curso nos vamos a introducir, explorar y comprender los conceptos y algoritmos que constituyen la base de lo que hoy en dia conocemos como inteligencia artificial. El curso se encuentra dividido en siete semanas, donde en cada una de ellas se introduce y explora lo básico de cada una de las grandes areas que comprende la inteligencia artificial. 

El objetivo principal sera la completa comprensión de los algoritmos y el problema que se presenta, esto acompañado del desafió de implementar todo correctamente en python.  

## Semana 0: Búsqueda 

En la  vida real para poder encontrar una solución de un problema, muchas veces se requiere de una previa búsqueda de posibles soluciones. En la primera semana se exploran algunos algoritmos que nos permiten en base a una estructura de grafos buscar posibles soluciones a problemas. 

A continuación se presenta una introducción a los proyectos:

### **Proyecto 1**: Degrees 

En este proyecto nos interesa implementar el juego Six Degrees of Kevin Bacon. Este es un juego divertido en el que conectas a dos actores cualquiera a través de sus papeles cinematográficos. El objetivo es completar este proceso en el menor número de pasos posible. Aquí nuestro trabajo sera completar la función shortest_path que es una implementación del algoritmo de búsqueda en anchura que se ve a continuación: 

![BFS](https://github.com/user-attachments/assets/9bb539d5-b511-4720-a3b7-8acd31aa65ba)


### **Proyecto 2**: TicTacToe

En este proyecto nos interesa implementar el juego Tic Tac toe. Este es un juego divertido en una cuadrícula de 3x3, donde los jugadores toman turnos marcando los espacios con X o O en un intento de obtener tres en una fila, ya sea horizontal, vertical o diagonalmente. El objetivo del juego es conseguir tres X u O seguidas antes que tu oponente. Aquí nuestro trabajo sera completar 7 funciones que representan diversas facetas del juego, donde la principal función es la implementación del algoritmo minimax que sera aquella que le permita al programa calcular el mejor posible movimiento. El algoritmo requerido para la implementación del código es el siguiente:

![MinMax](https://github.com/user-attachments/assets/f31a0293-8dc8-4c47-b933-7ecb0f80f434)

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

Para este proyecto el conocimiento sera representado en sentencias lógicas que están divididas dos partes:

1) Un conjunto de celdas que involucra a todas aquellas celdas alrededor de una celda en el tablero. Por ejemplo:
![Tablero](https://github.com/user-attachments/assets/3dedf190-174a-4e0d-a2cb-9efbfc2fdf81)

2) Un número que representa un conteo de minas totales.
Si tomamos el conjunto de las celdas alrededor de ( i , j ) seria:\
cells = { (i-1, j-1) ; (i-1, j) ; (i-1, j+1) ; (i, j-1) ; (i, j+1) ; (i+1, j-1) ; (i+1, j) ; (i+1, j+1) } = números de minas. 

Con esta forma de representar el conocimiento se hace muy sencillo poder inferir donde están ubicadas las minas, como por ejemplo:

1) Si no hay ninguna mina alrededor de ( i , j ) y por lo tanto todas las celdas son seguras. Su representación viene dada por:\
{ (i-1, j-1) ; (i-1, j) ; (i-1, j+1) ; (i, j-1) ; (i, j+1) ; (i+1, j-1) ; (i+1, j) ; (i+1, j+1) } = 0

![0](https://github.com/user-attachments/assets/46dd8d02-3a92-4844-b2ae-313b27d97b8f)


2) Si hay 8 minas alrededor de ( i , j ) y por lo tanto no hay ninguna celda segura. Su representación viene dada por:\
{ (i-1, j-1) ; (i-1, j) ; (i-1, j+1) ; (i, j-1) ; (i, j+1) ; (i+1, j-1) ; (i+1, j) ; (i+1, j+1) } = 8

![8](https://github.com/user-attachments/assets/a1f75e07-815d-4b10-b598-0e83c8689abf)


3) Hay una mina alrededor de ( i-1 , j-1 ), ( i-1 , j ) y ( i-1 , j+1 ) y dos minas alrededor de ( i+1 , j ).

![3](https://github.com/user-attachments/assets/cce3d112-6f6c-4c27-a5c9-5e97bbe9d555)


En esta ultima se puede realizar inferencia usando el hecho que:

 1) {( i , j-1 ) , ( i , j ) , ( i-1 , j ) } = 1
 2) {( i , j+1 ) , ( i , j ) , ( i-1 , j ) } = 1
 3) {( i-1 , j-1 ) , ( i , j-1 ) , ( i , j ) , ( i , j+1 ), ( i-1, j+1 )} = 1

 Con esto es claro que en realidad {( i , j )} = 1 y sumado que:

 4) { ( i+1  , j-1 ) , ( i , j-1 ) , ( i , j ) , ( i , j+1 ) , ( i+1 , j+1 ) } = 2 

 Por lo tanto es claro que {( i+1  , j-1 ) , ( i+1 , j+1 )} = 1.

## Semana 2: Incertidumbre 

A veces podemos toparnos en ocasiones no favorables, donde los dos temas anteriores no son suficientes para llevar a cabo con éxito las tareas asignadas. Un ejemplo claro es cuando un agente no posea la completa información acerca de un suceso o evento y este deba aun asi resolver una tarea, entonces ¿Como un agente podría realizar esto? El objetivo es cuantificar de la mejor forma la incertidumbre para que realize la opción mas plausible posible. En la vida real un hombre quizá no conozca sobre meteorología, pero es capaz de poder predecir que lloverá por observar su entorno y notar que esta nublado.

El objetivo en esta sección es construir agentes que bajo condiciones de observación parcial, eventos aleatorios o adversidades, sea capaz de manejar la incertidumbre y llevar a cabo sus tareas de la mejor forma posible. Para todo esto vamos a usar la probabilidad, pero ¿Que es la probabilidad? Bueno, para esto debemos saber que en la vida cotidiana generalmente existen dos tipos de fenómenos:

1) Los fenómenos deterministas: Son aquellos que no importa cuantas veces repitas un experimento sobre ellos siempre arrojan los mismos resultados. Ejemplo: El punto de ebullición del agua 
2) Los fenómenos aleatorios: Son aquellos que no importa cuantas veces repitas un experimento sobre ellos siempre arrojan un resultado distinto. Ejemplo: Lanzamiento de un dado.

Es claro que la probabilidad es la medida que cuantifica la incertidumbre asociada a la ocurrencia de algún evento o fenómeno de interés.
Estas deben cumplir algunos axiomas:

1) La probabilidad del suceso seguro es 1:

$$P(\Omega)= 1$$

2) La probabilidad de cualquier suceso *A* es no negativa

$$P(A)>0\ \ \ \forall A\ \epsilon\ \sigma-algebra\ sucesos $$

3) Si $\{S_n \}_{n\epsilon N}$ son eventos mutuamente excluyentes entonces:

$$P(U_{n=1}^\infty S_n) = \sum_{n=1}^{\infty}P(S_n)$$

Ademas otros conceptos de vital importancia son:

1) Variable aleatoria: Una variable aleatoria es una función que asigna un valor numérico a cada posible resultado de un experimento aleatorio:

$$(\Omega,F, P) \rightarrow (ℝ,B(ℝ), P_x)$$

2) Probabilidad Condicional: es la probabilidad de que ocurra un evento, dado que otro evento ya ha ocurrido, o sea es la probabilidad de que algo suceda, considerando que algo más ya ha sucedido. La formula viene dada por:

$$P(Y|X=x) = \frac{P(Y=y , X=x)}{P(X=x)}$$

$$P(Y=y, X=x)=P(X=x)P(Y|X=x)\ \ \ product\ rule$$ 

3) Probabilidad conjunta: es la probabilidad que nos permite calcular la probabilidad de que dos o más eventos ocurran al mismo tiempo. Es decir, mide la posibilidad de que se intercepten o coincidan múltiples eventos. Si los eventos son independientes su calculo viene dado por:

$$P(Y=y, X=x)= P(Y)P(X)$$

4) Probabilidad marginal: es la probabilidad de que ocurra un evento sin considerar la ocurrencia de otros eventos relacionados. En otras palabras, es la probabilidad "individual" de un evento, sin tomar en cuenta su relación con otros.

$$P(Y) = \sum_{x \epsilon X}P(Y=y, X=x)$$

5) Regla de bayes: es una fórmula que nos permite actualizar nuestras creencias o probabilidades sobre un evento, a medida que obtenemos nueva información. Para ello nsotros sabemos por los anteriores puntos que:

$$P(Y=y, X=x)=P(X=x)P(Y|X=x)$$ 
$$P(Y=y, X=x)=P(Y=y)P(X|Y=y)$$ 

Igualando:

$$P(X=x)P(Y|X=x)=P(Y=y)P(X|Y=y)$$

$$P(X|Y=y)=\frac{P(X=x)P(Y|X=x)}{P(Y=y)}$$

### **Proyecto 1**: PageRank















