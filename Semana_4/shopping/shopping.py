import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")

def month(mes):
  return {'Jan':0, 'Feb':1, 'Mar':2, 'Apr':3, 'May':4, 'June':5, 'Jul':6, 'Aug':7, 'Sep':8, 'Oct':9, 'Nov':10, 'Dec':11}.get(mes)

def visitor(tipo):
  return {'Returning_Visitor':1, 'New_Visitor':0, 'Other':0}.get(tipo)

def weekend(yesornot):
  return {'TRUE':1, 'FALSE':0}.get(yesornot)

def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    labels = []

    with open(filename,"r") as archivo:
        datos = csv.reader(archivo)
        for fila in datos:
           evidence.append(fila[0:17])
           labels.append(fila[17])

    evidence.pop(0)
    for i in evidence:
       i[0] = int(i[0]) # Administrative como int
       i[1] = float(i[1]) # Administrative_Duration como float
       i[2] = int(i[2]) # Informational como int
       i[3] = float(i[3]) # Informational_Duration como float
       i[4] = int(i[4]) # ProductRelated como int
       i[5] = float(i[5]) # ProductRelated_Duration como float
       i[6] = float(i[6]) # BounceRates como float
       i[7] = float(i[7]) # ExitRates como float
       i[8] = float(i[8]) # PageValues como float
       i[9] = float(i[9]) # SpecialDay como float
       i[10] = month(i[10]) # Month como int
       i[11] = int(i[11]) # OperatingSystems como int
       i[12] = int(i[12]) # Browser como int
       i[13] = int(i[13]) # Region como int
       i[14] = int(i[14]) # TrafficType como int
       i[15] = visitor(i[15]) # VisitorType como int
       i[16] = weekend(i[16]) # Weekend como int

    labels.pop(0)
    for i,j in enumerate(labels):
       labels[i] = weekend(j) # Usamos la misma funcion que se uso para weekend

    return evidence, labels

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    clasificador = KNeighborsClassifier(n_neighbors=1)
    return clasificador.fit(evidence,labels)

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    counter_true_positives = 0
    counter_true_negatives = 0
    counter_false_positives = 0
    counter_false_negatives = 0

    for tupla in [(j,l) for i,j in enumerate(labels) for k,l in enumerate(predictions) if i == k]:

        if tupla[0] == 1 and tupla[1] == 1:
            counter_true_positives += 1
        elif tupla[0] == 0 and tupla[1] == 1:
            counter_false_positives += 1
        elif tupla[0] == 0 and tupla[0] == 0:
            counter_true_negatives += 1
        else:
            counter_false_negatives += 1

    # Sensitivity and specificity calculation
    sensitivity = counter_true_positives / (counter_true_positives + counter_false_positives)
    specificity = counter_true_negatives / (counter_true_negatives + counter_false_negatives)

    return sensitivity, specificity

if __name__ == "__main__":
    main()
