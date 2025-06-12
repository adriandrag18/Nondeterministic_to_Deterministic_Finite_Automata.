# NFA to DFA Converter

This project implements a Python program to convert a Nondeterministic Finite Automaton (NFA) with epsilon transitions to a Deterministic Finite Automaton (DFA) using the subset construction algorithm. The code includes classes for representing NFAs and DFAs, parsing input files, and performing the conversion.

## Purpose

The program takes an NFA described in a text file, processes its states and transitions (including epsilon transitions), and outputs an equivalent DFA. This is a fundamental concept in automata theory, used in applications like regular expression matching and compiler design.

## Features

- **NFA Representation**: Supports NFAs with epsilon transitions, multiple transitions per input symbol, and multiple final states.
- **DFA Representation**: Produces a DFA with a single transition per input symbol and state.
- **File Parsing**: Reads NFA and DFA specifications from text files.
- **Conversion Algorithm**: Implements the subset construction method to convert NFAs to DFAs, handling epsilon closures and sink states.

## File Structure

- `NFA.py`: Defines the `NFA` class for representing and parsing NFAs.
- `DFA.py`: Defines the `DFA` class, including methods for parsing DFAs and converting NFAs to DFAs.

## Input File Format

The input file for an NFA should follow this format:

```
<number_of_states>
<final_state_1> <final_state_2> ... <final_state_n>
<state> <symbol> <next_state_1> <next_state_2> ...
...
```

- First line: Number of states (integer).
- Second line: Space-separated list of final states (integers).
- Subsequent lines: Transitions in the format `state symbol next_state(s)`, where `symbol` can be an input character or `eps` for epsilon transitions.

Example:
```
4
3
0 a 1 2
1 b 3
2 eps 3
```

## Usage

1. **Prepare an input file** (e.g., `nfa.txt`) with the NFA specification.
2. **Run the conversion**:
   ```python
   from NFA import NFA
   from DFA import DFA

   # Parse NFA from file
   nfa = NFA.parse("nfa.txt")

   # Convert NFA to DFA
   dfa = DFA.from_nfa(nfa)

   # Print DFA
   print(dfa)
   ```

3. The program outputs the DFA in a similar format:
   ```
   <number_of_states>
   <final_state_1> <final_state_2> ...
   <state> <symbol> <next_state>
   ...
   ```

## Algorithm Overview

The conversion from NFA to DFA uses the **subset construction algorithm**:

1. **Epsilon Closures**: Compute the epsilon closure for each state (all states reachable via epsilon transitions).
2. **State Subsets**: Each DFA state corresponds to a set of NFA states.
3. **Transitions**: For each DFA state and input symbol, compute the set of reachable NFA states, including their epsilon closures.
4. **Final States**: DFA states containing any NFA final state are marked as final.
5. **Sink State**: Add a sink state for undefined transitions to ensure the DFA is complete.

The code also removes unreachable states and handles edge cases like empty transitions.

## Key Concepts

- **Finite Automata**: Models of computation used to recognize regular languages.
- **NFA**: Allows multiple transitions per symbol and epsilon transitions (no input required).
- **DFA**: Requires exactly one transition per symbol per state, making it deterministic.
- **Epsilon Closure**: Set of states reachable from a given state via zero or more epsilon transitions.
- **Subset Construction**: Algorithm to convert an NFA to a DFA by treating sets of NFA states as single DFA states.

## Limitations

- Assumes input files are correctly formatted.
- Initial state is hardcoded to 0.
- Does not validate if the input alphabet is consistent across transitions.

## Further Reading

- **Automata Theory**: 
  - Sipser, M. (2012). *Introduction to the Theory of Computation*. Cengage Learning. [Chapter 1: Regular Languages]
  - [Wikipedia: Finite-state machine](https://en.wikipedia.org/wiki/Finite-state_machine)
- **Subset Construction**:
  - [Wikipedia: Powerset construction](https://en.wikipedia.org/wiki/Powerset_construction)
  - Hopcroft, J. E., & Ullman, J. D. (1979). *Introduction to Automata Theory, Languages, and Computation*. Addison-Wesley.
- **Python Type Hints**:
  - [Python Documentation: Typing](https://docs.python.org/3/library/typing.html)

## License

This project is for educational purposes and is not licensed for commercial use.
