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

import unittest

from nfa import NFA, Epsilon, NFAException


class TestSimpleDFA(unittest.TestCase):
    def setUp(self):
        self.fa = NFA('01')

    def test_instantiation(self):
        self.assertFalse(self.fa.no_of_states, 'States not empty at start')

    def test_add_state(self):
        """Newly created state should not have any transitions"""
        sid = self.fa.new_state()
        for s, p in self.fa.get_edges(sid).items():
            self.assertFalse(p, 'Found edge ({}, {}) in newly added state {}'.format(s, p, sid))

    def test_edge(self):
        fa = self.fa
        sid = fa.new_state()
        fa.new_edge(sid, '0', sid)
        edges = fa.get_edges(sid)
        q = edges['0']
        self.assertTrue(sid in q, 'Expected edge not found in {} for state {}'.format(q, sid))
        self.assertTrue(q - {sid} == set(), 'Unexpected edges found in {} for state {}'.format(q, sid))

    def test_has_edge(self):
        fa = self.fa
        s0 = fa.new_state()
        s1 = fa.new_state()
        s2 = fa.new_state()
        self.assertFalse(fa.has_edge(s0, s0), 'Should not have an edge s0->s0')
        self.assertFalse(fa.has_edge(s0, s1), 'Should not have an edge s0->s1')
        self.assertFalse(fa.has_edge(s0, s2), 'Should not have an edge s0->s2')
        self.assertFalse(fa.has_edge(s1, s1), 'Should not have an edge s1->s1')
        self.assertFalse(fa.has_edge(s1, s2), 'Should not have an edge s1->s2')
        self.assertFalse(fa.has_edge(s1, s0), 'Should not have an edge s1->s0')
        self.assertFalse(fa.has_edge(s2, s2), 'Should not have an edge s2->s2')
        self.assertFalse(fa.has_edge(s2, s1), 'Should not have an edge s2->s1')
        self.assertFalse(fa.has_edge(s2, s0), 'Should not have an edge s2->s0')

        fa.new_edge(s0, '0', s1)
        self.assertFalse(fa.has_edge(s0, s0), 'Should not have an edge s0->s0')
        self.assertTrue(fa.has_edge(s0, s1), 'Should have an edge s0->s1')
        self.assertFalse(fa.has_edge(s0, s2), 'Should not have an edge s0->s2')
        self.assertFalse(fa.has_edge(s1, s1), 'Should not have an edge s1->s1')
        self.assertFalse(fa.has_edge(s1, s2), 'Should not have an edge s1->s2')
        self.assertFalse(fa.has_edge(s1, s0), 'Should not have an edge s1->s0')
        self.assertFalse(fa.has_edge(s2, s2), 'Should not have an edge s2->s2')
        self.assertFalse(fa.has_edge(s2, s1), 'Should not have an edge s2->s1')
        self.assertFalse(fa.has_edge(s2, s0), 'Should not have an edge s2->s0')
        fa.new_edge(s0, '1', s2)
        self.assertFalse(fa.has_edge(s0, s0), 'Should not have an edge s0->s0')
        self.assertTrue(fa.has_edge(s0, s1), 'Should have an edge s0->s1')
        self.assertTrue(fa.has_edge(s0, s2), 'Should have an edge s0->s2')
        self.assertFalse(fa.has_edge(s1, s1), 'Should not have an edge s1->s1')
        self.assertFalse(fa.has_edge(s1, s2), 'Should not have an edge s1->s2')
        self.assertFalse(fa.has_edge(s1, s0), 'Should not have an edge s1->s0')
        self.assertFalse(fa.has_edge(s2, s2), 'Should not have an edge s2->s2')
        self.assertFalse(fa.has_edge(s2, s1), 'Should not have an edge s2->s1')
        self.assertFalse(fa.has_edge(s2, s0), 'Should not have an edge s2->s0')
        fa.new_edge(s0, '1', s0)
        self.assertTrue(fa.has_edge(s0, s0), 'Should have an edge s0->s0')
        self.assertTrue(fa.has_edge(s0, s1), 'Should have an edge s0->s1')
        self.assertTrue(fa.has_edge(s0, s2), 'Should have an edge s0->s2')
        self.assertFalse(fa.has_edge(s1, s1), 'Should not have an edge s1->s1')
        self.assertFalse(fa.has_edge(s1, s2), 'Should not have an edge s1->s2')
        self.assertFalse(fa.has_edge(s1, s0), 'Should not have an edge s1->s0')
        self.assertFalse(fa.has_edge(s2, s2), 'Should not have an edge s2->s2')
        self.assertFalse(fa.has_edge(s2, s1), 'Should not have an edge s2->s1')
        self.assertFalse(fa.has_edge(s2, s0), 'Should not have an edge s2->s0')
        fa.new_edge(s1, '0', s1)
        fa.new_edge(s1, '1', s0)
        fa.new_edge(s1, '1', s2)
        fa.new_edge(s2, '0', s0)
        self.assertTrue(fa.has_edge(s0, s0), 'Should have an edge s0->s0')
        self.assertTrue(fa.has_edge(s0, s1), 'Should have an edge s0->s1')
        self.assertTrue(fa.has_edge(s0, s2), 'Should have an edge s0->s2')
        self.assertTrue(fa.has_edge(s1, s1), 'Should have an edge s1->s1')
        self.assertTrue(fa.has_edge(s1, s2), 'Should have an edge s1->s2')
        self.assertTrue(fa.has_edge(s1, s0), 'Should have an edge s1->s0')
        self.assertFalse(fa.has_edge(s2, s2), 'Should not have an edge s2->s2')
        self.assertFalse(fa.has_edge(s2, s1), 'Should not have an edge s2->s1')
        self.assertTrue(fa.has_edge(s2, s0), 'Should have an edge s2->s0')

    def test_del_state(self):
        """Deleting a state should remove all edges to that state"""
        fa = self.fa
        s0 = fa.new_state()
        s1 = fa.new_state()
        s2 = fa.new_state()
        fa.new_edge(s0, '0', s1)
        fa.new_edge(s0, '1', s0)
        fa.new_edge(s0, '1', s2)
        fa.new_edge(s1, '0', s1)
        fa.new_edge(s1, '1', s0)
        fa.new_edge(s1, '1', s2)
        fa.new_edge(s2, '0', s0)

        fa.del_state(s0)
        self.assertEqual(fa.no_of_states, 2, 'Wrong number of states after delete ({})'.format(fa.no_of_states))
        edges = fa.get_edges(s1)
        self.assertFalse(s0 in [q for q in edges.values()], 'State {} remains a destination after delete')
        self.assertTrue(fa.has_edge_on_symbol(s1, '1', s2), 'Transition s1->s2 over 1 was deleted')
        self.assertFalse(fa.has_edge_on_symbol(s2, '0', s0), 'Transition s2->s0 over 1 not removed by delete')

    def test_process(self):
        fa = self.fa
        s0 = fa.new_state(initial=True, final=True)
        s1 = fa.new_state()

        fa.new_edge(s0, '0', s0)
        fa.new_edge(s0, '1', s1)
        fa.new_edge(s1, '0', s1)
        fa.new_edge(s1, '1', s0)

        vectors = {
            'accepting': [
                '0',
                '00',
                '000',
                '0110',
                '01010',
                '001100',
                '0011',
                '11000000',
                '11',
                '1111',
                '111111'],
            'rejecting': [
                '1',
                '01',
                '001',
                '10',
                '100',
                '111',
                '11111',
                '1111111',
                'abc'
            ]
        }

        for v in vectors['accepting']:
            self.assertTrue(fa.test_input(v), 'String "{}" was not accepted as it should'.format(v))

        for v in vectors['rejecting']:
            self.assertFalse(fa.test_input(v), 'String "{}" was not rejected as it should'.format(v))


class TestAlphanumericDFA(unittest.TestCase):
    def setUp(self):
        alphabet = [chr(i) for i in xrange(ord('0'), ord('9')+1)]
        alphabet += [chr(i) for i in xrange(ord('A'), ord('Z')+1)]
        alphabet += [chr(i) for i in xrange(ord('a'), ord('z')+1)]
        self.fa = NFA(alphabet)

    def test_vectors(self):
        fa = self.fa
        s0 = fa.new_state(initial=True)
        sA = fa.new_state()
        sB = fa.new_state()
        sC = fa.new_state()
        sD = fa.new_state(final=True)

        fa.new_edge(s0, 'A', sA)
        fa.add_multiple_edges(sA, {'A': sA, 'B': sB, 'C': sC, 'D': sD})
        fa.add_multiple_edges(sB, {'B': sB, 'C': sC, 'D': sD})
        fa.add_multiple_edges(sC, {'C': sC, 'D': sD})
        fa.new_edge(sD, 'D', sD)

        vectors = {
            'accepting': [
                'ABCD',
                'AABCD',
                'ABBCCD',
                'ABCDDDDD',
                'AD',
                'AAD',
                'ADDD'],
            'rejecting': [
                'BCD'
            ]
        }

        for v in vectors['accepting']:
            self.assertTrue(fa.test_input(v), 'String "{}" was not accepted as it should'.format(v))

        for v in vectors['rejecting']:
            self.assertFalse(fa.test_input(v), 'String "{}" was not rejected as it should'.format(v))

    def testInvalidSymbol(self):
        fa = self.fa
        s0 = fa.new_state(initial=True)

        self.assertRaises(NFAException, fa.test_input, '*#*')


class TestAlphaNumericNFA(unittest.TestCase):
    def setUp(self):
        alphabet = [chr(i) for i in xrange(ord('0'), ord('9')+1)]
        alphabet += [chr(i) for i in xrange(ord('A'), ord('Z')+1)]
        alphabet += [chr(i) for i in xrange(ord('a'), ord('z')+1)]
        alphabet += '+-'
        self.fa = NFA(alphabet)

    def test_vectors(self):
        '''
        Test an NFA that accepts digits with an optional sign.

          sInit -(+)-> sSign
          sInit -(-)-> sSign
          sInit -(Epsilon)->  sSign

          sSign -([0-9])-> sDigit
          sDigit -([0-9])-> sDigit

          sDigit is the accepting state
        '''
        fa = self.fa
        sInit = fa.new_state(initial=True)
        sSign = fa.new_state()
        sDigit = fa.new_state(final=True)

        fa.new_edge(sInit, '+', sSign)
        fa.new_edge(sInit, '-', sSign)
        fa.new_edge(sInit, Epsilon, sSign)
        for s in '0123456789':
            fa.new_edge(sSign, s, sDigit)
            fa.new_edge(sDigit, s, sDigit)

        vectors = {
            'accepting': [
                '123',
                '0',
                '+1',
                '-1',
                '+321',
                '-321'],
            'rejecting': [
                'ABC',
                '+-0',
                '12+21',
                '-12abc'
            ]
        }

        for v in vectors['accepting']:
            self.assertTrue(fa.test_input(v), 'String "{}" was not accepted as it should'.format(v))

        for v in vectors['rejecting']:
            self.assertFalse(fa.test_input(v), 'String "{}" was not rejected as it should'.format(v))



if __name__ == '__main__':
    unittest.main()
