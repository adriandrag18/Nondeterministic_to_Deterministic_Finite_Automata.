from typing import List, Tuple, Set, Dict
from NFA import NFA


def check_state(transition: List[Tuple], state: Set):
    for st, _, _ in transition:
        if st == state:
            return True
    return False


def get_key(d: dict, value):
    for key, val in d.items():
        if val == value:
            return key


class DFA:
    def __init__(self, state_number: int, initial_state: int, final_states: Set,
                 transitions: Dict[(Tuple, Set)]):
        self.states = state_number
        self.current_state = initial_state
        self.initial_state = initial_state
        self.final_states = final_states
        self.transitions = transitions

    def __str__(self):
        dfa_str = f"{self.states}\n"
        dfa_str += " ".join([str(s) for s in self.final_states]) + "\n"

        transitions_str = [f"{state} {character} {next_state}"
                           for (state, character), next_state in self.transitions.items()]

        return dfa_str + "\n".join(transitions_str)

    @staticmethod
    def parse(file):
        with open(file, "r") as fin:
            num = int(fin.readline())
            final = {int(x) for x in fin.readline().strip().split()}
            initial = 0
            s = fin.readline().strip()
            transitions = dict()
            while s:
                a, b, c = s.split()
                transitions[(int(a), b)] = int(c)
                s = fin.readline().strip()

            return DFA(num, initial, final, transitions)

    @staticmethod
    def search(state: int, current_state: int, closures: List[Set], nfa: NFA):
        next_states = nfa.transitions.get((current_state, 'eps'))
        if not next_states:
            return
        for next_state in next_states:
            if next_state not in closures[state]:
                closures[state].add(next_state)
                DFA.search(state, next_state, closures, nfa)

    @staticmethod
    def remove_transitions(nfa, alphabet):
        useful = [False] * nfa.states
        for (state, ch), new in nfa.transitions.items():
            if len(new.union({state})) > 1:
                useful[state] = True
        to_remove = {i for i in range(nfa.states) if not useful[i] and i not in nfa.final_states}
        for (state, ch), new in nfa.transitions.items():
            nfa.transitions[(state, ch)] = new.difference(to_remove)
        for ch in alphabet:
            for state in to_remove:
                try:
                    nfa.transitions.pop((state, ch))
                    nfa.states -= 1
                except:
                    pass

    @staticmethod
    def from_nfa(nfa: NFA):
        alphabet = {ch for _, ch in nfa.transitions.keys() if not ch == 'eps'}
        DFA.remove_transitions(nfa, alphabet)

        transitions = []
        closures = [set() for _ in range(nfa.states)]
        for state in range(nfa.states):
            closures[state].add(state)
            DFA.search(state, state, closures, nfa)

        transitions.append((0, 'ab', closures[0]))
        has_new_state = True
        n = 0
        while has_new_state:
            has_new_state = False
            old_len = len(transitions)
            for i in range(n, len(transitions)):
                state, ch, new_state = transitions[i]
                if not check_state(transitions, new_state):
                    for ch in alphabet:
                        new = set()
                        for st in new_state:
                            if nfa.transitions.get((st, ch)):
                                for s in nfa.transitions.get((st, ch)):
                                    new.update(closures[s])
                        if len(new):
                            transitions.append((new_state, ch, new))
                            has_new_state = True
            n = old_len
            print(*transitions, sep='\n', end='\n\n')

        finals = []
        for _, _, new_state in transitions:
            if new_state.intersection(nfa.final_states) and new_state not in finals:
                finals.append(new_state)
        transitions.remove((0, 'ab', closures[0]))
        encode = {0: closures[0]}
        number = 1
        for state, _, new_state in transitions:
            if state not in encode.values():
                encode[number] = state
                number += 1
            if new_state not in encode.values():
                encode[number] = new_state
                number += 1

        print(*encode.items(), sep='\n', end='\n\n')

        delta = dict()
        for state, ch, new_state in transitions:
            delta[(get_key(encode, state), ch)] = get_key(encode, new_state)

        print(*delta.items(), sep='\n')
        sink = False
        for state in range(number):
            for ch in alphabet:
                if delta.get((state, ch)) is None:
                    delta[(state, ch)] = number
                    sink = True
        if sink:
            for ch in alphabet:
                delta[(number, ch)] = number
            number += 1
        final = {get_key(encode, state) for state in finals}
        return DFA(len(encode), 0, final, delta)
