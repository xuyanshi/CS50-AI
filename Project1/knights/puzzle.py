from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

A_basis = Or(And(AKnight, Not(AKnave)), And(Not(AKnight), AKnave))
B_basis = Or(And(BKnight, Not(BKnave)), And(Not(BKnight), BKnave))
C_basis = Or(And(CKnight, Not(CKnave)), And(Not(CKnight), CKnave))

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    A_basis,
    Or(
        And(AKnight, AKnight, AKnave),
        And(AKnave, Not(And(AKnight, AKnave)))
    )
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    A_basis,
    B_basis,
    Or(
        And(AKnight, And(AKnave, BKnave)),
        And(AKnave, Not(And(AKnave, BKnave)))
    )
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."

ab_same = Or(
    And(AKnight, BKnight),
    And(AKnave, BKnave)
)

ab_diff = Or(
    And(AKnight, BKnave),
    And(AKnight, BKnave)
)

knowledge2 = And(
    A_basis,
    B_basis,
    Or(
        And(AKnight, ab_same),
        And(AKnave, Not(ab_same))
    ),
    Or(
        And(AKnight, ab_diff),
        And(AKnave, Not(ab_diff))
    ),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

a_said = Or(
    AKnight,
    AKnave
)

b_said = Or(

)

b_said2 = Or(
    And(BKnight, CKnave),
    And(BKnave, Not(CKnave))
)

c_said = Or(
    And(CKnight, AKnight),
    And(CKnave, Not(AKnight))
)

knowledge3 = And(
    b_said,
    b_said2,
    c_said
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
