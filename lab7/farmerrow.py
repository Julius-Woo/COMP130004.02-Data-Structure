class State:
    '''
    This class represents a state in the Farmer, Wolf, Goat, and Cabbage.
    '''
    def __init__(self, farmer, wolf, goat, cabbage):
        # Use 1 to represent the start side and 0 to represent the end side.
        self.farmer = farmer
        self.wolf = wolf
        self.goat = goat
        self.cabbage = cabbage
        
    def is_valid(self):
        # Check if the state is valid.
        if (self.wolf == self.goat and self.farmer != self.wolf) or \
            (self.goat == self.cabbage and self.farmer != self.goat):
            return False
        else:
            return True
        
    def is_goal(self):
        # Check if the state is the goal state.
        if (self.farmer == 0 and self.wolf == 0 and self.goat == 0 and self.cabbage == 0):
            return True
        else:
            return False
    
    def __str__(self):
        # String representation of the state.
        return "Farmer: " + str(self.farmer) + " Wolf: " + str(self.wolf) + \
            " Goat: " + str(self.goat) + " Cabbage: " + str(self.cabbage)
        
    def next_state(self):
        # Generate all possibel next states from the current state.
        next_states = []
        items = [self.wolf, self.goat, self.cabbage]
        
        for i, item in enumerate(items):
            if item == self.farmer:  # The item is on the same side as the farmer, so it can be moved.
                next_state = State(1 - self.farmer, *[(1 - self.farmer) if j == i else x for j, x in enumerate(items)])
                if next_state.is_valid():
                    next_states.append(next_state)
        
        # The farmer can also move alone.
        farmer_alone = State(1 - self.farmer, self.wolf, self.goat, self.cabbage)
        if farmer_alone.is_valid():
            next_states.append(farmer_alone)
        
        return next_states
    
def cross_river():
    start = State(1, 1, 1, 1)  # Start from the state where all items are on the start side.
    stack = [(start, [str(start)])]  # Use a stack to store the states and the path to the state.
    solutions = []  # Store all solutions.
    
    while stack:
        state_cur, path_cur = stack.pop()
        if state_cur.is_goal():  # Check if the current state is the goal state.
            solutions.append(path_cur)
            continue
        
        for state_next in state_cur.next_state():
            # Check if the next state is already in the path
            if str(state_next) not in path_cur:
                stack.append((state_next, path_cur + [str(state_next)]))
        
    return solutions

solutions = cross_river()
if solutions:
    print(f"Number of solutions found: {len(solutions)}")
    for i, solution in enumerate(solutions, start=1):
        print(f"\nSolution {i}:")
        for j in solution:
            print(j)
else:
    print("No solution found.")