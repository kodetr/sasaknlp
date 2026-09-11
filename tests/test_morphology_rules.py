"""Tests for morphological rule implementations."""

import unittest
from sasaknlp.morphology.rules import (
    CombinationRule,
    InfixRule,
    PrefixRule,
    ReduplicationRule,
    SuffixRule,
    load_rules_from_config,
)


class TestMorphologicalRules(unittest.TestCase):
    def test_prefix_rule_direct(self):
        rule = PrefixRule(name="passive_te", prefix="te")
        matches = rule.apply("tepinaq")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].root_candidate, "pinaq")
        self.assertEqual(matches[0].prefix, "te")

    def test_prefix_rule_nasal_m(self):
        # m- restoring p/b
        rule = PrefixRule(
            name="nasal_m",
            prefix="m",
            phonological_rules=[{"pattern": "^m([aeiou].*)", "restores": ["p\\1", "b\\1"]}],
        )
        matches = rule.apply("minaq")
        roots = [m.root_candidate for m in matches]
        self.assertIn("pinaq", roots)

    def test_suffix_rule_ang(self):
        rule = SuffixRule(name="transitive_ang", suffix="ang")
        matches = rule.apply("tulungang")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].root_candidate, "tulung")
        self.assertEqual(matches[0].suffix, "ang")

    def test_suffix_rule_ne(self):
        rule = SuffixRule(name="possessive_ne", suffix="ne")
        matches = rule.apply("baturne")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].root_candidate, "batur")

    def test_infix_rule_in(self):
        rule = InfixRule(name="passive_in", infix="in")
        matches = rule.apply("tinulung")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].root_candidate, "tulung")

    def test_combination_rule_pe_an(self):
        rule = CombinationRule(name="pe_an", prefix="pe", suffix="an")
        matches = rule.apply("pemanganan")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].root_candidate, "mangan")

    def test_reduplication_rule_hyphen(self):
        rule = ReduplicationRule()
        matches = rule.apply("bareng-bareng")
        self.assertTrue(any(m.root_candidate == "bareng" for m in matches))

    def test_reduplication_rule_space(self):
        rule = ReduplicationRule()
        matches = rule.apply("bareng bareng")
        self.assertTrue(any(m.root_candidate == "bareng" for m in matches))

    def test_reduplication_rule_with_suffix(self):
        rule = ReduplicationRule()
        matches = rule.apply("bareng-barengan")
        self.assertTrue(any(m.root_candidate == "bareng" for m in matches))

    def test_load_rules_from_config(self):
        rules = load_rules_from_config()
        self.assertGreater(len(rules), 10)


if __name__ == "__main__":
    unittest.main()
