import itertools
import random

class Minesweeper():
    """
    Minesweeper game representation
    """
    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines

class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """
    # Esta clase deberia crear objetos que son definidos por sus celdas adyacentes y el conteo de minas que estos tienen, por ejemplo:
    # Para definir el siguiente objeto 3x3:
    #
    #     | (1,1) | (1,2) | (1,3) |
    #     |-----------------------|   Sentence(cells, count) donde cells sera un input de un conjunto de tuplas(como veremos mas adelante)
    #     | (2,1) | (2,2) | (2,3) |   y count el contador de minas alrededor de la celda seleccionada. Por ejemplo: Supongamos que la celda 
    #     |-----------------------|   celda seleccionada fue (2,2) entonces cells sera un conjunto {(1,1),(1,2),(1,3),(2,1),(2,3),(3,1),(3,2),(3,3)}
    #     | (3,1) | (3,2) | (3,3) |   y count seria el numero de minas alrededor de (2,2)

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        ## La única forma de saber con certeza donde están todas las minas es si recibimos la información previa de que el
        ## el conteo de minas alrededor de una celda es igual a ocho.
        return self.cells if self.count == 8 else None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        ## La única forma de saber con certeza que todas las celdas aledañas son seguras es si recibimos la información previa
        ## de que el conteo de minas alrededor de una celda es igual a cero.
        return self.cells if self.count == 0 else None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        ## Se debe comprobar que la celda introducida que sabemos que es una mina pertenezca al conjunto de todas las celdas aledañas.
        ## Si pertenece entonces debemos actualizar el conjunto de todas las celdas aledañas removiendo esa celda conocida como mina y
        ## reduciendo el conteo de minas totales en el tablero. Si no pertenece entonces devuelve None.
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        return None

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        ## Se debe comprobar que la celda introducida que sabemos que es segura pertenezca al conjunto de todas las celdas aledañas.
        ## Si pertenece entonces debemos actualizar el conjunto de todas las celdas aledañas removiendo esa celda conocida como segura.
        ## Si no pertenece entonces devuelve None.
        return self.cells.remove(cell) if cell in self.cells else None

class MinesweeperAI():
    """
    Minesweeper game player
    """
    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        ## Si el movimiento no ha sido hecho, o sea que la celda no se encuentra en el conjunto de movimientos hechos 
        ## vamos a agregar la celda que sabemos que es segura al conjunto de movimientos hechos, si la celda se encuentra en
        ## el conjunto de movimientos hechos entonces devolveremos None.
        
        self.moves_made.add(cell) if cell not in self.moves_made else None
        
        ## Si el movimiento no ha sido marcado como seguro, o sea que la celda no se encuentra en el conjunto de movimientos seguros 
        ## vamos a agregar la celda que sabemos que es segura al conjunto de movimientos seguros, si la celda se encuentra en
        ## el conjunto de movimientos seguros entonces devolveremos None.
        
        self.mark_safe(cell) if cell not in self.safes else None

        ## Para este paso vamos a crear un conjunto vació donde guardaremos todas las posibles celdas jugables, para ello
        ## se va a recorrer todas las celdas aledañas a la celda (i,j)-esima introducida y estas celdas se agregaran al
        ## conjunto de acuerdo a algunos requerimientos como:
        ## 1) Que las celdas estén dentro del tablero de juego.
        ## 2) Que las celdas no se encuentren en el conjunto de movimientos hechos ni en el conjunto de minas.
        ## Si se cumplen ambos requerimientos entonces la celda (i,j)-esima se agregara al conjunto, pero ademas
        ## de hallar alguna celda que pertenece al conjunto de las minas se reducirá el contador de minas conocidas.
        ## Luego con toda esta informacion previa podemos crear "Sentence" que añadiremos al conocimiento 

        cells = set()
        
        for i in range( cell[0] - 1, cell[0] + 2 ):
            for j in range( cell[1] - 1, cell[1] + 2 ):

                if (i,j) == cell:
                    continue
                
                if 0 <= i < self.height and 0 <= j < self.width:
                    if (i,j) not in self.moves_made and (i,j) not in self.mines:
                        cells.add((i,j))
                    elif (i,j) in self.mines:
                        count -= 1
        nueva_sentencia = Sentence(cells,count)
        self.knowledge.append(nueva_sentencia)

        ## Marcar cualquier celda adicional como segura o como mina si se puede concluir ello a traves de la lista de 
        ## conocimiento y las funciones antes creadas para ello.
        
        for i in self.knowledge:

            # Casillas seguras
            seguras = i.known_safes()
            if seguras is not None:
                segura = list(seguras)
                for j in segura:
                    self.mark_safe(j)

            # Casillas con minas
            minas = i.known_mines()
            if minas is not None:
                mina = list(minas)
                for j in mina:
                    self.mark_mine(j)

        # Añadir una nueva "sentence" al conocimiento base de la IA si ella puede ser inferida del conocimineto existente

        for sentence in self.knowledge:
            for item in self.knowledge:

                if item == sentence:
                    continue

                if item.cells.issubset(sentence.cells):
                    new_set = sentence.cells.difference(item.cells)
                    new_count = sentence.count - item.count
                    new_sentence = Sentence(new_set, new_count)
                    if new_sentence not in self.knowledge:
                        self.knowledge.append(new_sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        ## Para retornar una celda segura primero debemos crear un conjunto que contenga todas estas celdas.
        ## Usando la diferencia de conjuntos podemos hallar este conjunto muy fácilmente y luego solo queda 
        ## comprobar que dicho conjunto no sea vació para devolver algún valor(celda) de este, sino solo se devuelve None
        movimientos = self.safes - self.moves_made
        if len(movimientos) != 0:
            for i in movimientos:
                return i
        return None
       
    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        ## Si ninguna celda es segura, o sea make_safe_move() devuelve None, entonces se elegirá alguna celda aleatoria.
        ## Esta celda aleatoria debe cumplir:
        ## 1) La celda resultante debe estar dentro de las dimensiones del tableros 
        ## 2) La celda no debe estar dentro del conjunto de movimientos ya hechos, ni dentro del conjunto de las minas 
        while True:
            (i, j) = (random.randrange(self.height) , random.randrange(self.width))
            if (i, j) not in self.moves_made and (i, j) not in self.mines:
                return (i, j)
