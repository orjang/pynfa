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
        self.fa = NFA('012')

    def test_instantiation(self):
        self.assertFalse(self.fa.no_of_states, 'States not empty at start')

    def test_add_state(self):
        """Newly created state should not have any transitions"""
        sid = self.fa.new_state()
        for s, p in self.fa.get_edges_from_state(sid).items():
            self.assertFalse(p, 'Found edge ({}, {}) in newly added state {}'.format(s, p, sid))

    def test_edge(self):
        fa = self.fa
        sid = fa.new_state()
        fa.new_edge(sid, '0', sid)
        edges = fa.get_edges_from_state(sid)
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
        edges = fa.get_edges_from_state(s1)
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
            ]
        }

        for v in vectors['accepting']:
            self.assertTrue(fa.test_input(v), 'String "{}" was not accepted as it should'.format(v))

        for v in vectors['rejecting']:
            self.assertFalse(fa.test_input(v), 'String "{}" was not rejected as it should'.format(v))


class TestAlphanumericDFA(unittest.TestCase):
    def setUp(self):
        alphabet = [chr(i) for i in range(ord('0'), ord('9')+1)]
        alphabet += [chr(i) for i in range(ord('A'), ord('Z')+1)]
        alphabet += [chr(i) for i in range(ord('a'), ord('z')+1)]
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
        alphabet = [chr(i) for i in range(ord('0'), ord('9')+1)]
        alphabet += [chr(i) for i in range(ord('A'), ord('Z')+1)]
        alphabet += [chr(i) for i in range(ord('a'), ord('z')+1)]
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

    def test_partial_match(self):
        """Test that a string with a partial match is not accepted.
        Example:
           nfa accepting string "abc" should not accept any string "abc.+"
        """
        fa = self.fa
        start = fa.new_state(initial=True)
        sa = fa.new_state(name='a')
        sb = fa.new_state(name='b')
        sc = fa.new_state(name='c')
        final = fa.new_state(final=True)
        fa.new_edge(start, 'a', sa)
        fa.new_edge(sa, 'b', sb)
        fa.new_edge(sb, 'c', sc)
        fa.new_edge(sc, Epsilon, final)
        self.assertTrue(fa.test_input('abc'), 'String "abc" not accepted as it should')
        self.assertFalse(fa.test_input(''), 'String "" not rejected as it should')
        self.assertFalse(fa.test_input('abcd'), 'String "abcd" not rejected as it should')


class TestCombinations(unittest.TestCase):
    def setUp(self):
        """
        Define one NFA a that accept all strings in the regular language '00*1'
        Define a second NFA accepting all string in the regular language '11*0'
        """
        fa = NFA('01')
        sa0 = fa.new_state(initial=True, name='sa0')
        sa1 = fa.new_state(name='sa1')
        sa2 = fa.new_state(final=True, name='sa2')

        fa.new_edge(sa0, '0', sa1)
        fa.new_edge(sa1, '0', sa1)
        fa.new_edge(sa1, '1', sa2)

        self.assertTrue(fa.test_input('01'), 'String "01" not accepted')
        self.assertFalse(fa.test_input('00'), 'String "00" not rejected')

        fb = NFA('01')
        sb0 = fb.new_state(initial=True, name='sb0')
        sb1 = fb.new_state(name='sb1')
        sb2 = fb.new_state(final=True, name='sb2')

        fb.new_edge(sb0, '1', sb1)
        fb.new_edge(sb1, '1', sb1)
        fb.new_edge(sb1, '0', sb2)

        self.assertTrue(fb.test_input('10'), 'String "10" not accepted')
        self.assertFalse(fb.test_input('11'), 'String "11" not rejected')

        self.nfa1 = fa
        self.nfa2 = fb

    def testConcatenation(self):
        """
        Define one NFA a that accept all strings in the regular language '00*1'
        Define a second NFA accepting all string in the regular language '11*0'

        Concatenate the two NFAs and test that it accepts only string of the regular
        language '00*111*0'
        :return:
        """
        fa = self.nfa1
        fb = self.nfa2

        fc = fa | fb

        self.assertTrue(fc.test_input('0110'), 'String "0110" was not accepted')
        self.assertTrue(fc.test_input('01110'), 'String "01110" was not accepted')
        self.assertFalse(fc.test_input('0010'), 'String "0010" not rejected')
        self.assertFalse(fc.test_input('0100'), 'String "0100" not rejected')
        self.assertFalse(fc.test_input('0111'), 'String "0111" not rejected')
        self.assertFalse(fc.test_input('1111'), 'String "1111" not rejected')

    def testUnion(self):
        """
        Define one NFA a that accept all strings in the regular language '00*1'
        Define a second NFA accepting all string in the regular language '11*0'

        Combine the two NFAs with an or function and test that the new NFA
        accepts string of the regular language '00*1 or 11*0'

        :return:
        """
        fa = self.nfa1
        fb = self.nfa2

        fc = fa + fb

        self.assertTrue(fc.test_input('01'), 'String "01" not accepted')
        self.assertTrue(fc.test_input('10'), 'String "10" not accepted')
        self.assertFalse(fc.test_input('11'), 'String "11" not rejected')
        self.assertFalse(fc.test_input('00'), 'String "00" not rejected')
        self.assertFalse(fc.test_input(''), 'String "" not rejected')

    def testStar(self):
        """
        Define one NFA a that accept all strings in the regular language '00*1'

        Make new NFA from defined as the kleene star operator of the original NFA.
        Make sure that the new NFA accepts string of the regular language '(00*1)*'

        :return:
        """
        fa = self.nfa1

        fstar = fa.star()

        self.assertTrue(fstar.test_input(''), 'String "" not accepted')
        self.assertTrue(fstar.test_input('01'), 'String "01" not accepted')
        self.assertTrue(fstar.test_input('0101'), 'String "0101" not accepted')
        self.assertTrue(fstar.test_input('01000100001'), 'String "01000100001" not accepted')
        self.assertFalse(fstar.test_input('00'), 'String "00" not rejected')
        self.assertFalse(fstar.test_input('10'), 'String "10" not rejected')


class TestClosure(unittest.TestCase):
    def testClosure(self):
        nfa = NFA('01')

        s0 = nfa.new_state(initial=True)
        s1 = nfa.new_state()
        s2 = nfa.new_state()
        s3 = nfa.new_state(final=True)
        s4 = nfa.new_state()

        nfa.new_edge(s0, '0', s1)
        nfa.new_edge(s0, Epsilon, s2)
        nfa.new_edge(s1, '0', s3)
        nfa.new_edge(s1, Epsilon, s4)
        nfa.new_edge(s2, '1', s2)
        nfa.new_edge(s2, Epsilon, s3)

        closure = nfa.closure(s0)
        self.assertIn(s0, closure, "Closure start state s0 should be in closure")
        self.assertNotIn(s1, closure, "State s1 should not be in closure")
        self.assertIn(s2, closure, "State s2 not in closure")
        self.assertIn(s3, closure, "State s3 not in closure")
        self.assertNotIn(s4, closure, "State s4 should not be in closure")

    def testEmptyClosure(self):
        nfa = NFA('01')

        s0 = nfa.new_state(initial=True)

        closure = nfa.closure(s0)
        self.assertIn(s0, closure, "Closure start state should be in closure")

class TestAlphaNumericDFA(unittest.TestCase):
    """Test NFA->DFA conversion"""

    def setUp(self):
        alphabet = [chr(i) for i in range(ord('0'), ord('9')+1)]
        alphabet += [chr(i) for i in range(ord('A'), ord('Z')+1)]
        alphabet += [chr(i) for i in range(ord('a'), ord('z')+1)]
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
        nfa = self.fa
        sInit = nfa.new_state(initial=True)
        sSign = nfa.new_state()
        sDigit = nfa.new_state(final=True)

        nfa.new_edge(sInit, '+', sSign)
        nfa.new_edge(sInit, '-', sSign)
        nfa.new_edge(sInit, Epsilon, sSign)
        for s in '0123456789':
            nfa.new_edge(sSign, s, sDigit)
            nfa.new_edge(sDigit, s, sDigit)

        dfa = nfa.subset_construct_dfa()

        # Check that no epsilon transition exists
        eps = dfa.get_edges_on_symbol(Epsilon)
        self.assertFalse(eps, "DFA has epsilon transitions: {}".format(eps))

        # Check that no state has more than one transition per symbol
        for p in dfa.get_states():
            edges = dfa.get_edges_from_state(p)
            for s, qs in edges.items():
                self.assertTrue(len(qs) < 2, "DFA state {} has more than one transition on symbol {}".format(p, s))

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
                '-12abc',
                'ABC-321'
            ]
        }

        for v in vectors['accepting']:
            self.assertTrue(nfa.test_input(v), 'String "{}" was not accepted by nfa as it should'.format(v))
            self.assertTrue(dfa.test_input(v), 'String "{}" was not accepted by dfa as it should'.format(v))

        for v in vectors['rejecting']:
            self.assertFalse(nfa.test_input(v), 'String "{}" was not rejected by nfa as it should'.format(v))
            self.assertFalse(dfa.test_input(v), 'String "{}" was not rejected by dfa as it should'.format(v))


class TestStringNFA(unittest.TestCase):
    """Test construction of NFA from a simple string of symbols"""

    def setUp(self):
        alphabet = [chr(i) for i in range(ord('0'), ord('9')+1)]
        alphabet += [chr(i) for i in range(ord('A'), ord('Z')+1)]
        alphabet += [chr(i) for i in range(ord('a'), ord('z')+1)]
        alphabet += '+-'
        self.nfa = NFA(alphabet)

    def testSimpleString(self):
        nfa = self.nfa
        nfa.build_from_string('abcde')
        self.assertTrue(nfa.test_input('abcde'), 'String "abcde"  was not accepted by the nfa as it should')
        self.assertFalse(nfa.test_input('abcd'), 'String "abcd" was not rejected as it should')
        self.assertFalse(nfa.test_input('abcdef'), 'String "abcdef" was not rejected as it should')
        self.assertFalse(nfa.test_input(''), 'String "" was not rejected as it should')

if __name__ == '__main__':
    unittest.main()
