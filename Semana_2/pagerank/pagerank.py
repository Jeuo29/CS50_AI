import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages

def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    No_damping_factor = 1 - damping_factor

    # Creamos un diccionario donde guardaremos las probabilidades de transición
    probabilidades = {key:0 for key in corpus}

    # Creamos un diccionario que guarde el numero de links de cada pagina
    numero_links = {key:len(corpus[key]) for key in corpus}
    N = len(corpus)
    
    for key in corpus:
        Probabilidad_links=0
        Probabilidad_corpus = No_damping_factor/N

        if key in corpus[page]:
            Probabilidad_links = damping_factor/numero_links[page]

        probabilidades[key] = Probabilidad_corpus + Probabilidad_links
    return probabilidades

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    if n > 0:
        # Creamos un diccionario donde guardaremos todos las veces que aparezcan cada pagina durante las n repeticiones
        opciones = [key for key in corpus] 
        frecuencia = {key:0 for key in opciones}

        # Escogemos nuestra primera muestra de forma aleatoria que sera nuestro punto de partida
        muestra = random.choice(opciones)

        for i in range(n-1):
            if frecuencia[muestra] == 0:
                frecuencia[muestra] = 1/n
            else:
                frecuencia[muestra]= frecuencia[muestra] + 1/n
            
            probabilidades = transition_model(corpus, muestra, damping_factor)

            muestra = random.choices(opciones,probabilidades.values())[0]
        return frecuencia
    else:
        raise ValueError("Error el numero de la muestra n debe ser mayor que 0")


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    No_damping_factor = 1 - damping_factor

    # Creamos dos diccionario donde guardaremos las probabilidades
    probabilidades_iniciales = {key:1/len(corpus) for key in corpus}
    probabilidades_finales = {key:{} for key in corpus}

    # Creamos un diccionario que guarde el numero de links de cada pagina
    numero_links = {key:len(corpus[key]) for key in corpus}

    while True:
        
        Probabildad_corpus = No_damping_factor/len(corpus)

        for key in corpus:
            acumulador_probabilidad = 0
            for link in corpus:

                if key in corpus[link]:
                    acumulador_probabilidad += probabilidades_iniciales[link]/numero_links[link]

            probabilidades_finales[key] =  Probabildad_corpus + acumulador_probabilidad*damping_factor
        
        Diferencia = {}
        for key in probabilidades_iniciales:
            Diferencia[f"{key} final - {key} Inicial"] = abs(probabilidades_finales[key] - probabilidades_iniciales[key])
        valores = max(tuple(Diferencia.values()))
        if valores < 0.001:
            return probabilidades_finales
        else:
            probabilidades_iniciales = probabilidades_finales.copy()

if __name__ == "__main__":
    main()
