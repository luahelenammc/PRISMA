import unittest
from dataclasses import replace
from reference.gate import Request, evaluate

class ContractTests(unittest.TestCase):
    def test_p01_documentary_vs_simulation(self):
        a=evaluate(Request('lens','public',sources=('synthetic:A',)))
        b=evaluate(Request('mask','public',explicit_mask=True))
        self.assertEqual((a.label,b.label),('supported_interpretation','labeled_fiction'))
    def test_p02_missing_source(self):
        self.assertEqual(evaluate(Request('lens','public')).route,'functional_fallback')
    def test_p03_mask_label(self):
        self.assertEqual(evaluate(Request('mask','public',explicit_mask=True)).label,'labeled_fiction')
        self.assertEqual(evaluate(Request('mask','public')).route,'blocked')
    def test_p04_distinct_modes(self):
        self.assertNotEqual(evaluate(Request('mask',explicit_mask=True)).route,evaluate(Request('table')).route)
    def test_p05_canon_conflict(self):
        d=evaluate(Request('world','fictional',sources=('C1',),canon_conflict=True,write_authorized=True))
        self.assertEqual((d.route,d.persistence),('candidate_only','READ_ONLY'))
    def test_p06_creative_candidate(self):
        self.assertTrue(evaluate(Request('world','fictional',sources=('C1',))).candidate)
    def test_p07_local_governance(self):
        self.assertEqual(evaluate(Request('table',domain='institution',local_authority_allows=False)).route,'blocked')
    def test_p08_high_risk(self):
        self.assertEqual(evaluate(Request('table','private',high_risk=True,identifiable=True)).route,'blocked')
        self.assertEqual(evaluate(Request('table',high_risk=True,educational=True)).route,'synthetic_educational')
    def test_p09_simple(self):
        self.assertEqual(evaluate(Request('table',simple=True)).route,'direct')
    def test_p10_domain_invariant(self):
        r=Request('counterproof'); self.assertEqual(evaluate(r),evaluate(replace(r,domain='new_domain')))
    def test_p11_disagreement(self):
        self.assertEqual(evaluate(Request('table',disagreements=('A != B',))).disagreements,('A != B',))
        self.assertEqual(evaluate(Request('table')).disagreements,())
    def test_p12_no_independence_claim(self):
        self.assertEqual(evaluate(Request('table')).independence,'not_verified')
    def test_p13_consent(self):
        self.assertEqual(evaluate(Request('mirror','mirror',sources=('C',))).route,'blocked')
        self.assertEqual(evaluate(Request('mirror','mirror',sources=('C',),consent=True)).route,'mirror')
    def test_p14_offline(self):
        self.assertEqual(evaluate(Request('lens','public',sources=('local',),internet=False,moon_source=False)).route,'lens')
    def test_p15_no_write(self):
        self.assertEqual(evaluate(Request('table',readback_verified=True)).persistence,'READ_ONLY')
    def test_p16_readback(self):
        self.assertEqual(evaluate(Request('table',write_authorized=True)).persistence,'pending_unverified')
        self.assertEqual(evaluate(Request('table',write_authorized=True,readback_verified=True)).persistence,'readback_declared')
