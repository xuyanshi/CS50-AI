import sys

from crossword import *


class CrosswordCreator:

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
        for var in self.domains:
            words = self.domains[var].copy()
            for word in words:
                if len(word) != var.length:
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revision = False
        '''
        The revise function should make the variable x arc consistent with the variable y. x and y will both be 
        Variable objects representing variables in the puzzle. Recall that x is arc consistent with y when every 
        value in the domain of x has a possible value in the domain of y that does not cause a conflict. (A conflict 
        in the context of the crossword puzzle is a square for which two variables disagree on what character value 
        it should take on.) To make x arc consistent with y, you’ll want to remove any value from the domain of x 
        that does not have a corresponding possible value in the domain of y. Recall that you can access 
        self.crossword.overlaps to get the overlap, if any, between two variables. The domain of y should be left 
        unmodified. The function should return True if a revision was made to the domain of x; it should return False 
        if no revision was made.
        '''
        if self.crossword.overlaps[x, y] is not None:
            idx_x, idx_y = self.crossword.overlaps[x, y]
            x_words = self.domains[x].copy()
            for word_x in x_words:
                remove_flag = all(word_x[idx_x] != word_y[idx_y] for word_y in self.domains[y])
                if remove_flag:
                    revision = True
                    self.domains[x].remove(word_x)
        return revision

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.

        function AC-3(csp):
            queue = all arcs in csp
            while queue non-empty:
                (X, Y) = DEQUEUE(queue)
                if REVISE(csp, X, Y):
                    if size of X.domain == 0:
                        return false
                    for each Z in X.neighbors - {Y}:
                        ENQUEUE(queue, (Z, X))
            return true
        """
        qu = []
        if arcs is None:
            for x in self.domains:
                qu.extend((x, y) for y in self.domains if x != y)
        else:
            qu.extend(arcs)
        while qu:
            x, y = qu.pop(0)
            if self.revise(x, y):
                if self.domains[x] is None or len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x):
                    if z != y:
                        qu.append((z, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.domains:
            if var not in assignment:  # or len(assignment[var]) != 1:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # all values are distinct
        vals = assignment.values()
        if len(set(vals)) != len(vals):
            return False

        for var in assignment:
            # every value is the correct length
            if var.length != len(assignment[var]):
                return False
            # no conflicts between neighboring variables
            for nbr in self.crossword.neighbors(var):
                if nbr in assignment:
                    idx_x, idx_y = self.crossword.overlaps[var, nbr]
                    if assignment[var][idx_x] != assignment[nbr][idx_y]:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        vals = []  # (order, value)
        # It may be helpful to first implement this function by returning a list of values in any arbitrary order
        # (which should still generate correct crossword puzzles).
        # Once your algorithm is working, you can then go back and ensure that
        # the values are returned in the correct order.
        for val in self.domains[var]:
            vals.append((len(vals), val))

        vals.sort()  # sorting by order
        return [val[1] for val in vals]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        selected_variable = None
        # It may be helpful to first implement this function by returning any arbitrary unassigned variable
        # (which should still generate correct crossword puzzles).
        # Once your algorithm is working, you can then go back and ensure that
        # you are returning a variable according to the heuristics.
        for var in self.domains:
            if var not in assignment:
                selected_variable = var
                break
        return selected_variable

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        raise NotImplementedError


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
