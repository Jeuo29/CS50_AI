from logic import *

AKnight = Symbol("A is a Knight")  # A is a knight
AKnave = Symbol("A is a Knave")    # A is a knave

BKnight = Symbol("B is a Knight")  # B is a knight
BKnave = Symbol("B is a Knave")    # B is a knave 

CKnight = Symbol("C is a Knight")  # C is a knight
CKnave = Symbol("C is a Knave")    # C is a knave

# Puzzle 0
# A says "I am both a knight and a knave."  ------------------------> Premisa = And(AKnight,AKnave) 

knowledge0 = And(
    Or( And(AKnight, Not(AKnave)) , And(AKnave,Not(AKnight)) ), # Ley de la disyuncion exclusiva, esto ya que A es un caballero o un villano, pero no puede ser ambos 
    Implication( AKnave , Not(And(AKnight,AKnave)) ),  # Si A es un villano entonces la premisa es falsa porque todo lo que dice un villano es falso, por lo tanto If Aknave=true --> Not(False)=True
    Implication( AKnight , And(AKnight,AKnave) )       # Pero si A es un caballero entonces la premisa es verdadera porque todo lo que dice un caballero es verdad, por lo tanto If Aknight=true --> True
)

# Puzzle 1
# A says "We are both knaves." ------------------------------------> Premisa= And(AKnave,BKnave)
# B says nothing.

knowledge1 = And(
    Or( And(AKnight, Not(AKnave)) , And(AKnave,Not(AKnight)) ), # Ley de la disyuncion exclusiva, esto ya que A es un caballero o un villano, pero no puede ser ambos 
    Implication( AKnave, Not(And(AKnave,BKnave)) ),   # Si A es un villano entonces la premisa es falsa, por lo tanto esta linea seria verdadera 
    Implication( AKnight, And(AKnight,AKnave) ),      # Pero si A es un caballero entonces la premisa es verdadera, por lo tanto esta linea seria verdadera

    Or( And(BKnight, Not(BKnave)) , And(BKnave,Not(BKnight)) ), # Ley de la disyuncion exclusiva, esto ya que B es un caballero o un villano, pero no puede ser ambos 
                                                                # Si B no dice nada y la premisa de A es falsa, entonces B es un caballero 
)

# Puzzle 2
# A says "We are the same kind."      ------------------------------> Premisa de A = Or( And(AKnight,BKnight), And(AKnave,BKnave))
# B says "We are of different kinds." ------------------------------> Premisa de B = Or( And(AKnight,BKnave), And(AKnave,BKnight))

knowledge2 = And(
    Or( And(AKnight, Not(AKnave)) , And(AKnave,Not(AKnight)) ), # Ley de la disyuncion exclusiva, esto ya que A es un caballero o un villano, pero no puede ser ambos 
    Implication( AKnave, Not(Or( And(AKnight,BKnight), And(AKnave,BKnave))) ),   # Si A es un villano entonces la premisa es falsa, por lo tanto esta linea seria verdadera 
    Implication( AKnight, Or( And(AKnight,BKnight), And(AKnave,BKnave)) ),      # Pero si A es un caballero entonces la premisa es verdadera, por lo tanto esta linea seria verdadera

    Or( And(BKnight, Not(BKnave)) , And(BKnave,Not(BKnight)) ), # Ley de la disyuncion exclusiva, esto ya que B es un caballero o un villano, pero no puede ser ambos 
    Implication( BKnave, Not(Or( And(AKnight,BKnave), And(AKnave,BKnight))) ),   # Si B es un villano entonces la premisa es falsa, por lo tanto esta linea seria verdadera 
    Implication( BKnight, Or( And(AKnight,BKnave), And(AKnave,BKnight)) ),      # Pero si B es un caballero entonces la premisa es verdadera, por lo tanto esta linea seria verdadera
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which. ---> Premisa A = Or(AKnight, AKnave)
# B says "A said 'I am a knave'." ---------------> 1er Premisa B = Or(Not(AKnight),AKnave)
# B says "C is a knave." --------------> 2da Premisa B = CKnave
# C says "A is a knight." -------------> Premisa C = AKnight

knowledge3 = And(
   Or( And(AKnight, Not(AKnave)) , And(AKnave,Not(AKnight)) ), # Ley de la disyuncion exclusiva, esto ya que A es un caballero o un villano, pero no puede ser ambos 
   Implication( AKnave, Not(Or(AKnight,AKnave)) ),   # Si A es un villano entonces la premisa siempre es falsa, por lo tanto esta linea seria verdadera 
   Implication( AKnight, Or(AKnight,AKnave) ),       # Si A es un caballero entonces la premisa siempre es verdadera, por lo tanto esta linea seria verdadera 

   Or( And(BKnight, Not(BKnave)) , And(BKnave,Not(BKnight)) ), # Ley de la disyuncion exclusiva, esto ya que B es un caballero o un villano, pero no puede ser ambos 
   Implication( BKnave, Not(Or(Not(AKnight),AKnave)) ),   # Si B es un villano entonces la premisa siempre es falsa, por lo tanto esta linea seria verdadera 
   Implication( BKnight, Or(Not(AKnight),AKnave) ),       # Si B es un caballero entonces la premisa siempre es verdadera, por lo tanto esta linea seria verdadera 
   Implication(BKnave, Not(CKnave)),   # Si B es un villano entonces las premisa siempre es falsa, por lo tanto esta linea seria verdadera
   Implication(BKnight, CKnave),   # Si B es un caballero entonces las premisa siempre es verdadera, por lo tanto esta linea seria verdadera

   Or( And(CKnight, Not(CKnave)) , And(CKnave,Not(CKnight)) ), # Ley de la disyuncion exclusiva, esto ya que C es un caballero o un villano, pero no puede ser ambos 
   Implication( CKnave, Not(AKnight) ),   # Si C es un villano entonces la premisa es falsa, por lo tanto esta linea seria verdadera 
   Implication( CKnight, AKnight )        # Si C es un caballero entonces la premisa es verdadera, por lo tanto esta linea seria verdadera
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
