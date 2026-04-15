import collections


class SudokuSolver:
    def __init__(self, board_str):
        # board_str is a list of 9 strings, each 9 chars long
        self.variables = [(r, c) for r in range(9) for c in range(9)]
        self.domains = {}
        for r in range(9):
            for c in range(9):
                val = int(board_str[r][c])
                if val == 0:
                    self.domains[(r, c)] = list(range(1, 10))
                else:
                    self.domains[(r, c)] = [val]

        self.neighbors = {v: self.get_neighbors(v) for v in self.variables}
        self.backtrack_calls = 0
        self.backtrack_failures = 0

    def get_neighbors(self, var):
        r, c = var
        neighbors = set()
        for i in range(9):
            neighbors.add((r, i))  # Row
            neighbors.add((i, c))  # Column
        # 3x3 Box
        br, bc = (r // 3) * 3, (c // 3) * 3
        for i in range(br, br + 3):
            for j in range(bc, bc + 3):
                neighbors.add((i, j))
        neighbors.remove(var)
        return neighbors

    def ac3(self):
        """Pre-process domains to ensure arc consistency."""
        queue = collections.deque([(u, v) for u in self.variables for v in self.neighbors[u]])
        while queue:
            (xi, xj) = queue.popleft()
            if self.revise(xi, xj):
                if not self.domains[xi]: return False
                for xk in self.neighbors[xi]:
                    if xk != xj:
                        queue.append((xk, xi))
        return True

    def revise(self, xi, xj):
        revised = False
        # If xj is assigned a single value, xi cannot have that value
        if len(self.domains[xj]) == 1:
            val = self.domains[xj][0]
            if val in self.domains[xi]:
                self.domains[xi].remove(val)
                revised = True
        return revised

    def is_consistent(self, var, value, assignment):
        for neighbor in self.neighbors[var]:
            if neighbor in assignment and assignment[neighbor] == value:
                return False
        return True

    def solve(self):
        # Run AC-3 first to narrow down possibilities
        self.ac3()
        # Create initial assignment from fixed values
        assignment = {v: self.domains[v][0] for v in self.variables if len(self.domains[v]) == 1}
        return self.backtrack(assignment)

    def backtrack(self, assignment):
        self.backtrack_calls += 1
        if len(assignment) == 81:
            return assignment

        # Select unassigned variable (MRV heuristic: variable with smallest domain)
        unassigned = [v for v in self.variables if v not in assignment]
        var = min(unassigned, key=lambda v: len(self.domains[v]))

        for value in self.domains[var]:
            if self.is_consistent(var, value, assignment):
                assignment[var] = value

                # Forward Checking: Temporary domain reduction
                saved_domains = {n: list(self.domains[n]) for n in self.neighbors[var]}
                consistent = True
                for neighbor in self.neighbors[var]:
                    if neighbor not in assignment and value in self.domains[neighbor]:
                        self.domains[neighbor].remove(value)
                        if not self.domains[neighbor]:
                            consistent = False
                            break

                if consistent:
                    result = self.backtrack(assignment)
                    if result: return result

                # Backtrack
                del assignment[var]
                for n, dom in saved_domains.items():
                    self.domains[n] = dom

        self.backtrack_failures += 1
        return None


def print_board(assignment):
    for r in range(9):
        line = ""
        for c in range(9):
            line += str(assignment.get((r, c), 0))
        print(line)


# --- Execution ---
# Example string for 'easy.txt' provided in your image
easy_board = [
    "004030050", "609400000", "005100489",
    "000060930", "300807002", "026040000",
    "453009600", "000004705", "090050200"
]

solver = SudokuSolver(easy_board)
solution = solver.solve()

if solution:
    print("Solution found:")
    print_board(solution)
    print(f"\nBacktrack Calls: {solver.backtrack_calls}")
    print(f"Backtrack Failures: {solver.backtrack_failures}")
else:
    print("No solution exists.")