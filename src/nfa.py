# coding=utf-8

# pynfa
# Copyright (C) 2015  Örjan Gustavsson
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#


class Epsilon:
    """Null symbol used for epsilon transitions"""
    pass


class NFAException(Exception):
    pass


class NFAInvalidInput(NFAException):
    pass


class NFA(object):

    def __init__(self, alphabet):
        """
        :param alphabet: Sequence of symbols making up the input alphabet
        :return: None
        """
        self._alphabet = set(alphabet)
        self._states = {}  # {state:{symol:set(states)}}
        self._state_names = {}
        self._finals = set()
        self._initial = None
        self._next_state = 0
        self._alphabet.add(Epsilon)

    def new_state(self, initial=False, final=False, name=None):
        """

        :param initial: True if new state is an initial state
        :param final: True if new state is an accepting state
        :param name: Optional name for the new state
        :return: State id
        """
        sid = self._next_state
        self._next_state += 1
        self._states[sid] = {s: set() for s in self._alphabet}
        self._state_names[sid] = name or str(sid)
        if final:
            self._finals.add(sid)

        if initial:
            self._initial = sid

        return sid

    def set_initial_state(self, sid):
        """
        Set start state of the NFA. If an initial state already is assigned
        it will be replaced by the state id used in this call.

        :param sid: New initial state id
        :return: Previous initial state id, or None
        """
        prev = self._initial
        self._initial = sid

        return prev

    def set_as_final_state(self, sid):
        """
        Add state sid as an accepting final state

        :param sid: State id to be added to final state set
        :return: None
        """
        self._finals.add(sid)

    def remove_final_state(self, sid):
        """
        Remove state sid from final state set

        :param sid: State id to be removed from finals
        :return: None
        """
        self._finals.remove(sid)

    def del_state(self, sid):
        """
        Delete a state from the NFA.
        Any transitions to the deleted state from other states
        are removed as well
        """
        for p in self._states:
            for sym, states in self._states[p].items():
                if sid in states:
                    self._states[p][sym].remove(sid)

        if self._initial == sid:
            self._initial = None

        if sid in self._finals:
            self._finals.remove(sid)

        del self._states[sid]
        del self._state_names[sid]

    @property
    def no_of_states(self):
        return len(self._states)

    def delta(self, state, symbol):
        """
        Determine next set of states given current state
        and input symbol.

        Passing a symbol that is not part of the defined alphabet
        throws NFAInvalidInput.
        """
        try:
            return self._states[state][symbol]
        except KeyError:
            if symbol not in self._alphabet:
                raise NFAInvalidInput("symbol {} not in the defined alphabet".format(symbol))
            else:
                raise

    def new_edge(self, p, s, q):
        """
        Add edge from state p to state q on symbol s

        :param p: Edge source state id
        :param s: Input symbol for this edge
        :param q: Edge destination state id
        :return: None
        """
        self._states[p][s].add(q)

    def new_edge_set(self, p, s, states):
        """
        Add edges from state p over symbol s to a set of states

        :param p: Edge source state id
        :param s: Input symbol for this edge
        :param states: Set of edge destination state ids
        :return: None
        """
        self._states[p][s] |= states

    def add_multiple_edges(self, p, state_map):
        """Add multiple state transitions from state p

        state_map is a dict like:
           { sym: state, ...}

           Add one edge for each input symbol sym to its mapped state
        """
        for sym, state in state_map.items():
            self._states[p][sym].add(state)

    def has_edge_on_symbol(self, p, s, q):
        """
        Check if there is an edge from state p
        over symbol s to state q
        """
        return q in self._states[p][s]

    def has_edge(self, p, q):
        """
        Check if there is an edge from state p
        to state q on any symbol
        """
        for sym, states in self._states[p].items():
            if q in states:
                return True
        return False

    def get_states(self):
        """
        Get a dict of state ids and names in this NFA
        """
        return {p: self._state_names[p] for p in self._states}

    def get_initial(self):
        """
        Get initial state id

        :return: State id of the initial state or None if no initial state exists
        """
        return self._initial

    def get_finals(self):
        """
        Get a list of all final states

        :return: List all accepting state ids
        """
        return [p for p in self._finals]

    def get_edges_from_state(self, p):
        """
        Get a dict mapping all edges from state q
        of format {symbol: set(states), ...}
        """
        return {s: q for s, q in self._states[p].items()}

    def get_edges_on_symbol(self, s):
        """
        Get a dict mapping all edges from state over symbol s
        of format {from_state: to_state, ...}
        """
        edges = {}
        for p, states in self._states.items():
            try:
                edges[p] = set([q for q in states[s]])
            except KeyError:
                if s not in self._alphabet:
                    raise NFAInvalidInput("symbol {} not in the defined alphabet".format(s))
                else:
                    raise

        return edges

    def test_input(self, input_sequence):
        """
        Run NFA on an input sequence of symbols and return
        True if the whole sequence is consumed and the NFA is in
        at least one final state

        :param input_sequence: Iterable of input symbols from the defined alphabet
        :returns: True if the NFA accepts input, False if not
        """
        if self._initial is None:
            raise NFAException("NFA has no initial state")

        current_states = {self._initial}

        processed = set()
        while processed ^ current_states:
            for p in list(processed ^ current_states):
                current_states |= self.delta(p, Epsilon)
                processed.add(p)

        for sym in input_sequence:
            next_states = set()
            for p in current_states:
                next_states |= self.delta(p, Epsilon)
                next_states |= self.delta(p, sym)

            processed = set()
            while processed ^ next_states:
                for p in list(processed ^ next_states):
                    next_states |= self.delta(p, Epsilon)
                    processed.add(p)
            current_states = next_states

            if not current_states:
                return False

        return True if current_states & self._finals else False

    def concatenate(self, other):
        """
        Concatenate two NFAs
        A new NFA is returned with the concatenated NFAs, leaving both input NFAs unchanged

        :param other: Other NFA to be concatenated after this one
        :return: Concatenated new NFA
        """
        concat = NFA(self._alphabet)

        sid_first_to_new = {}
        sid_new_to_first = {}
        sid_second_to_new = {}
        sid_new_to_second = {}

        # Add all states from first NFA to new NFA
        for p, name in self.get_states().items():
            sid = concat.new_state(name=name)
            sid_first_to_new[p] = sid
            sid_new_to_first[sid] = p

        # Add all states from second NFA
        for p, name in other.get_states().items():
            sid = concat.new_state(name=name)
            sid_second_to_new[p] = sid
            sid_new_to_second[sid] = p

        # Add all transitions from first NFA
        for p in self.get_states():
            for s, states in self.get_edges_from_state(p).items():
                concat.new_edge_set(sid_first_to_new[p], s, set([sid_first_to_new[q] for q in states]))

        # Add all transitions from second NFA
        for p in other.get_states():
            for s, states in other.get_edges_from_state(p).items():
                concat.new_edge_set(sid_second_to_new[p], s, set([sid_second_to_new[q] for q in states]))

        # Set first NFA start state as new start state
        concat.set_initial_state(sid_first_to_new[self._initial])

        # Connect all final states in first NFA to start state of second NFA
        for p in self.get_finals():
            concat.new_edge(sid_first_to_new[p], Epsilon, sid_second_to_new[other.get_initial()])

        # Set all final states from second NFA as finals in new NFA
        for p in other.get_finals():
            concat.set_as_final_state(sid_second_to_new[p])

        return concat

    def closure(self, p):
        """
        Epsilon closure for a state

        Return the set of states reachable from state p without
        consuming any input symbols, ie, using only epsilon transitions

        :param p: State id to get closure of
        :return: Set of states that is the closure of p
        """
        closure_states = {p}
        processed = set()
        while closure_states ^ processed:
            for p in list(closure_states ^ processed):
                closure_states |= self.get_edges_from_state(p)[Epsilon]
                processed.add(p)
        return closure_states
