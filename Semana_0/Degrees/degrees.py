import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}

def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass

def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")

## La siguiente función toma dos ID numbers que pertenecen a dos celebridades las cuales 
## queremos encontrar su conexión mas corta a traves de sus papeles.

def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    ## Se crean o definen: 
    ## El nodo inicial: su estado es el ID number,no tiene padre ni una acción 
    ## puntual definida(cualquier película donde haya trabajado). 
    ## Una frontera: para este caso en la búsqueda de anchura necesitamos una frontera 
    ## cuya forma de remover estados siga una cola del tipo FIFO y se agrega el estado 
    ## inicial a la frontera.
    ## Un conjunto vació: aquí se guardaran los estados que exploremos.

    nodo_inicial = Node(state = source, parent = None, action = None)
    frontera = QueueFrontier()
    frontera.add(nodo_inicial)
    N_explorados = set()

    ## Luego, nos interesa recorrer todos los estados en busca de una solución(si la hay).
    ## En cada iteración nos interesa comprobar:
    ## 1) Si la frontera se encuentra vacía: si esto es asi significa que habremos recorrido 
    ## todos los estados y no existe solución posible. Si no esta vacía continuamos con el paso 2.
    ## 2) Siguiendo una cola tipo FIFO removeremos el primer valor para analizar si es una solución
    ## 3) Si el valor removido resulta ser la solución entonces se crea una lista donde se guardara la solución 
    ## y se procede a recorrer cada nodo de padre en padre hasta llegar al nodo inicial, donde en cada recorrido 
    ## se guarda una tupla dentro de la lista con información acerca de la película y el nombre del actor, para al 
    ## final retornar la lista final.
    ## 4) Si el valor removido no resulta ser la solución, entonces se añade al conjunto de nodos explorados y se guardan 
    ## todos los vecinos del estado removido en la frontera teniendo algunas consideraciones. Para que un nodo vecino pueda 
    ## entrar a la frontera debe cumplir que no este en el conjunto de estados explorados y ademas no pertenezca ya a la frontera, 
    ## si esto se cumple este nodo hijo puede añadirse a la frontera para su posterior análisis. Ademas si simplemente detectamos 
    ## que uno de los vecinos ya es una solución no necesitamos añadirlo a la frontera, simplemente se retorna la solución.

    while True:
        if frontera.empty():
            raise Exception("no solution")
        nodo = frontera.remove()
        if nodo.state == target:
            camino = []
            while nodo.parent is not None:
                camino.append((nodo.action,nodo.state))
                nodo = nodo.parent
            camino.reverse()
            return camino 
        N_explorados.add(nodo)
        vecinos = neighbors_for_person(nodo.state)
        for accion, estado in vecinos:
            if not frontera.contains_state(estado) and estado not in N_explorados:
                nodo_hijo = Node(state = estado, parent = nodo , action = accion)
                if nodo_hijo.state == target:
                    camino = []
                    while nodo_hijo.parent is not None:
                        camino.append((nodo_hijo.action,nodo_hijo.state))
                        nodo_hijo = nodo_hijo.parent
                    camino.reverse()
                    return camino
                frontera.add(nodo_hijo)

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]

def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors

if __name__ == "__main__":
    main()
