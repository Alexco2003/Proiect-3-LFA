# Function to read the NFA-LAMBDA from the file and transform it to a DFA (the function will return the DFA)

def build_automata(file_name):
    # Read the NFA-LAMBDA from the file and extract the necessary information
    with open(file_name) as f:
        n = int(f.readline().strip())  # Total number of states
        sigma = f.readline().strip().split()  # The alphabet
        q0 = int(f.readline().strip())  # Start state
        final_states = set(int(state) for state in f.readline().strip().split())  # Set of final states
        delta = {}  # Transition function (it will be a dictionary of dictionaries)

        # Parsing the transition table
        for line in f:
            aux = line.strip().split()
            state = int(aux[0])  # Current state
            symbol = aux[1]  # Input symbol
            next_state = int(aux[2])  # Next state

            # Updating the transition function dictionary
            if state in delta:
                if symbol in delta[state]:
                    delta[state][symbol].add(next_state)
                else:
                    delta[state][symbol] = set([next_state])
            else:
                delta[state] = {symbol: set([next_state])}

    def lambda_closure(state, delta):
        closure = set([state])  # Initialize the closure with the current state

        # If there are lambda transitions from the current state, add the next states to the closure
        if state in delta and 'lambda' in delta[state]:
            for next_state in delta[state]['lambda']:
                closure.update(lambda_closure(next_state, delta))

        return closure

    def get_dfa_state(states):
        return tuple(sorted(states))  # Return a sorted tuple of states as a single DFA state

    # Find the lambda closure of the start state
    initial_state = lambda_closure(q0, delta)

    dfa_delta = {}  # DFA transition function
    visited = set()  # Set to keep track of visited DFA states

    dfa_initial_state = get_dfa_state(initial_state)  # Convert the initial state to a DFA state
    visited.add(dfa_initial_state)  # Add the initial state to the visited set

    queue = [initial_state]  # Initialize the queue with the initial state
    while queue:
        current_states = queue.pop(0)  # Get the current NFA states from the queue
        current_dfa_state = get_dfa_state(current_states)  # Convert the current NFA states to a DFA state

        for symbol in sigma:
            if symbol != 'lambda':
                next_states = set()

                # Find the next states for the given input symbol by exploring the NFA transitions
                for state in current_states:
                    if state in delta and symbol in delta[state]:
                        next_states.update(delta[state][symbol])

                lambda_states = set()

                # Find the lambda closure of the next states
                for state in next_states:
                    lambda_states.update(lambda_closure(state, delta))

                next_dfa_state = get_dfa_state(lambda_states)  # Convert the lambda closure to a DFA state

                # If the next DFA state has not been visited, add it to the visited set and the queue for further exploration
                if next_dfa_state not in visited:
                    queue.append(lambda_states)
                    visited.add(next_dfa_state)

                # Update the DFA transition function
                if current_dfa_state not in dfa_delta:
                    dfa_delta[current_dfa_state] = {}
                dfa_delta[current_dfa_state][symbol] = next_dfa_state

    dfa_final_states = set()

    # Check each visited DFA state if it contains any final NFA state, add it to the set of DFA final states
    for dfa_state in visited:
        if any(state in final_states for state in dfa_state):
            dfa_final_states.add(dfa_state)

    # Return the DFA information
    return len(visited), sigma, dfa_initial_state, dfa_final_states, dfa_delta

# The NFA-LAMBDA file name
file_name = input("Enter the NFA-LAMBDA file name: ").strip()

# Call the build_automata function to build the DFA
n, sigma, q0, final_states, delta = build_automata(file_name)

# For the output

# Convert states to strings
sigma_str = " ".join(sigma)  # Convert sigma (alphabet) to a string
q0_str = "".join(map(str, q0))  # Convert the initial state to a string
final_states_str = " ".join(["".join(map(str, state)) for state in final_states])  # Convert final states to a string
delta_str = []

# Convert the DFA transition function to a string representation
for state, transitions in delta.items():
    state_str = "".join(map(str, state))  # Convert the current state to a string
    for symbol, next_state in transitions.items():
        next_state_str = "".join(map(str, next_state))  # Convert the next state to a string
        delta_str.append(f"{state_str} {symbol} {next_state_str}")

# Write the DFA information to output.txt
with open("output.txt", "w") as f:
    f.write(str(n) + "\n")  # Write the number of states
    f.write(sigma_str + "\n")  # Write the alphabet
    f.write(q0_str + "\n")  # Write the initial state
    f.write(final_states_str + "\n")  # Write the final states
    f.write("\n".join(delta_str))  # Write the transition function
