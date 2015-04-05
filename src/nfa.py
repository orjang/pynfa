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
        """Add new edge from state p to q on symbol s"""
        self._states[p][s].add(q)

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

    def get_edges(self, p):
        """
        Get a dict mapping all edges from state q
        of format {symbol: set(states), ...}
        """
        return {s: q for s, q in self._states[p].items()}

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
        for p in list(current_states):
            current_states |= self.delta(p, Epsilon)

        for sym in input_sequence:
            next_states = set()
            for p in current_states:
                next_states |= self.delta(p, Epsilon)
                next_states |= self.delta(p, sym)

            for p in list(next_states):
                next_states |= self.delta(p, Epsilon)
            current_states = next_states

            if not current_states:
                return False

        return True if current_states & self._finals else False
