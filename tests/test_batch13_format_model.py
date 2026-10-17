import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from batch13_format_model import *
class TestOriginalCandidateModel(unittest.TestCase):
 def test_default_data(self):
  self.assertEqual(FREQUENCIES,(44100,48000,96000))
  self.assertEqual(CHANNELS,(2,))
  self.assertEqual(DEPTHS,(16,))
  self.assertEqual(CHANNEL_MASK,3)
 def test_only_sok(self):
  self.assertEqual([x.rate for x in probe(lambda m,r,c,b: 0 if r==48000 else 1,1).rates],[48000])
 def test_full_tree(self):
  t=probe(lambda *a:0,0)
  self.assertEqual([x.rate for x in t.rates],[44100,48000,96000])
  self.assertEqual(t.rates[0].channels,{2:{16}})
 def test_shared_vs_exclusive(self):
  seen=[]
  probe(lambda *a:(seen.append(a),0)[1],1)
  self.assertTrue(all(x[0]==1 for x in seen))
  self.assertEqual(len(seen),3)
 def test_special_bypass(self):
  self.assertEqual(probe(lambda *a:1/0,0,special=True).rates,[])
 def test_rate_lookup(self):
  t=probe(lambda m,r,c,b:0 if r==44100 else 1,0)
  self.assertTrue(has_rate(t,44100))
  self.assertFalse(has_rate(t,96000))
if __name__=='__main__':unittest.main()
