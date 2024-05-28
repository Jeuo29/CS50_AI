import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Prob of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Prob of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Prob of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation Prob
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint Prob
                p = joint_Prob(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")

def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_Prob(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint Prob.

    The Prob returned should be the Prob that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    dic={}
    Dist_Prob_PasarGen={}
    for Nombre in people.values():
        dic[Nombre['name']]={'NumeroGenes': 1 if Nombre['name'] in one_gene else 2 if Nombre['name'] in two_genes else 0,
                               'Razgo': True if Nombre['name'] in have_trait else False,
                               'Parents': (Nombre['mother'],Nombre['father'])
                            }

    Prob = 1
    for nombre in dic:

        if dic[nombre]['Parents'] == (None,None):
            Prob *= PROBS['gene'][dic[nombre]['NumeroGenes']]*PROBS["trait"][dic[nombre]['NumeroGenes']][dic[nombre]['Razgo']]
        else:
            Prob *= PROBS["trait"][dic[nombre]['NumeroGenes']][dic[nombre]['Razgo']]
            Padres = dic[nombre]['Parents']

            for parent in Padres:
                Dist_Prob_PasarGen[parent] = PROBS['mutation'] if dic[parent]['NumeroGenes'] == 0 else 0.5 if dic[parent]['NumeroGenes'] == 1 else 1 - PROBS['mutation']

            if dic[nombre]['NumeroGenes'] == 0:
                Prob *= (1-Dist_Prob_PasarGen[Padres[0]])*(1-Dist_Prob_PasarGen[Padres[1]])
            elif dic[nombre]['NumeroGenes'] == 1:
                Prob *= (1-Dist_Prob_PasarGen[Padres[0]])*(Dist_Prob_PasarGen[Padres[1]]) + Dist_Prob_PasarGen[Padres[0]]*(1-Dist_Prob_PasarGen[Padres[1]])
            else:
                Prob *= Dist_Prob_PasarGen[Padres[0]]*Dist_Prob_PasarGen[Padres[1]]
    return Prob

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint Prob `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    dic = {}
    for nombre in probabilities:
        dic[nombre]={'NumeroGenes': 1 if nombre in one_gene else 2 if nombre in two_genes else 0,
                           'Razgo': True if nombre in have_trait else False
                    } 
        
    for nombre in probabilities:
        probabilities[nombre]["gene"][dic[nombre]['NumeroGenes']] += p
        probabilities[nombre]["trait"][dic[nombre]['Razgo']] += p

    return  
        
def normalize(probabilities):
    """
    Update `probabilities` such that each Prob distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        
        total_gen = 0
        for prob in probabilities[person]['gene'].values():
            total_gen += prob
        for norm in probabilities[person]['gene']:
            probabilities[person]['gene'][norm] *= 1/total_gen

        total_razgo = 0
        for prob in probabilities[person]['trait'].values():
            total_razgo += prob
        for norm in probabilities[person]['trait']:
            probabilities[person]['trait'][norm] *= 1/total_razgo

    return probabilities

if __name__ == "__main__":
    main()
