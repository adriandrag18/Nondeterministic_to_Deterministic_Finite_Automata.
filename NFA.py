from typing import Dict, Tuple, Set


class NFA:
    def __init__(self, state_number, initial_state, final_states: Set, transitions: Dict[(Tuple,
                                                                                          Set)]):
        self.states = state_number
        self.current_state = initial_state
        self.initial_state = initial_state
        self.final_states = final_states
        self.transitions = transitions

    def __str__(self):
        nfa_str = f"{self.states}\n"
        nfa_str += " ".join([str(s) for s in self.final_states]) + "\n"

        transitions_str = []
        for (state, character), next_states in self.transitions.items():
            transitions_str.append(f"{state} {character} " + " ".join(map(str, next_states)))

        return nfa_str + "\n".join(transitions_str)

    @staticmethod
    def parse(file):
        with open(file, "r") as fin:
            num = int(fin.readline().strip())
            final = [int(x) for x in fin.readline().strip().split()]
            initial = 0
            s = fin.readline().strip()
            transitions = dict()
            while s:
                state, character, *next_states = s.split()
                transitions[(int(state), character)] = set([int(x) for x in next_states])
                s = fin.readline().strip()

            return NFA(num, initial, set(final), transitions)
