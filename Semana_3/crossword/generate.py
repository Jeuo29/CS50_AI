import sys
import copy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        Number_letter = {i:len(i) for i in self.crossword.words}
        for variable in self.crossword.variables:
            for word in Number_letter:
                if Number_letter[word] != variable.length and word in self.domains[variable]:
                    self.domains[variable].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        letters_index = self.crossword.overlaps[x,y]
        couples = {var_x:{True for var_y in self.domains[y] 
                              if var_x[letters_index[0]] == var_y[letters_index[1]]} for var_x in self.domains[x]}
        for word in couples:
            if len(couples[word]) == 0:
                self.domains[x].remove(word)
                revised = True
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        #Definimos la cola
        if arcs == None:
            queue = [(var_x,var_y) for var_x, var_y in self.crossword.overlaps
                 if self.crossword.overlaps[var_x,var_y] != None]
            while len(queue) != 0:
                var_x, var_y = queue.pop(0)
                if self.revise(var_x, var_y):
                    if len(self.domains[var_x]) == 0:
                        return False
                    for neighbor in self.crossword.neighbors(var_x):
                        if neighbor != var_y:
                            queue.append((neighbor,var_x))
            return True
        else:
            queue = arcs
            while len(queue) != 0:
                var_x, var_y = queue.pop(0)
                if self.revise(var_x, var_y):
                    if len(self.domains[var_x]) == 0:
                        return False
                    for neighbor in (self.crossword.neighbors(var_x)):
                        if neighbor != var_y:
                            queue.append((neighbor,var_x))
            return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return all([variable in assignment for variable in self.domains])

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Las palabras del diccionario assigment no deben ser iguales
        values = [value for value in assignment.values()]
        if len(values) != len(set(values)):
            return False

        # Las palabras deben ser del tamaño correcto de la variable
        length = [False for key,value in assignment.items() if key.length != len(value)]
        if len(length) > 0:
          return False

        # Las palabras vecinas no deben causar conflictos cuando se sobrelapan o sea las letras deben ser las mismas
        for key in assignment:
            for neighbor in self.crossword.neighbors(key):

                if neighbor in assignment:
                    index_x, index_y = self.crossword.overlaps[key,neighbor]
                    if assignment[key][index_x] != assignment[neighbor][index_y]:
                        return False
                    
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        choices = dict()
        for word_var in self.domains[var]:
            for neighbor in self.crossword.neighbors(var):
                list_choices = []
                if neighbor not in assignment:
                    var_x, var_y = self.crossword.overlaps[var, neighbor]
                    list_choices = [True for word_neighbor in self.domains[neighbor] if word_neighbor[var_y] != word_var[var_x]]
            choices[word_var] = len(list_choices)
            sort_choices = sorted(choices.items(), key=lambda item: item[1])
            return [choice[0] for choice in sort_choices]
    
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        variables_choices = {variable: self.domains[variable] for variable in self.domains 
                            if variable not in assignment}
        sort_choices = sorted(variables_choices.items(), key=lambda item:len(item[1]))
        return [choice[0] for choice in sort_choices][0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if len(assignment) == len(self.domains):
            return assignment
        Var = self.select_unassigned_variable(assignment)
        for value in self.domains[Var]:
            new_assignment = assignment.copy()
            new_assignment[Var] = value
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
