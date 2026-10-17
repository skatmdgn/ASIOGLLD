import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from batch12_model import *
class ASIOModelTests(unittest.TestCase):
 def setUp(self):
  self.a=Port(True,2,exclusive_bits=24,shared_rates=(48000,),exclusive_rates=(44100,))
  self.b=Port(False,2,exclusive_bits=32,shared_bits=24,shared_rates=(48000,),exclusive_rates=(44100,))
 def test_rates(self):
  c=Config(False,(self.a,),(self.b,))
  self.assertEqual(can_sample_rate(c,48000),0)
  self.assertEqual(can_sample_rate(c,44100),-997)
 def test_depth(self):
  c=Config(True,(self.a,),(self.b,))
  self.assertEqual(channel_info(c,0,True)[1]['type'],17)
  self.assertEqual(channel_info(c,0,False)[1]['type'],18)
 def test_empty_eligible(self):
  c=Config(True,(replace(self.a,flags=0),),())
  self.assertEqual(can_sample_rate(c,12345),0)
 def test_failure_partial_write(self):
  c=Config(True,(replace(self.a,exclusive_bits=20),),())
  status,info=channel_info(c,0,True)
  self.assertEqual(status,-1000);self.assertEqual(info['isActive'],1)
 def test_registry_failure_keeps_updated_config(self):
  c=Config(True,(self.a,),(self.b,))
  status,updated,attempt,reset=set_sample_rate_path(c,48000,44100,helper=False)
  self.assertEqual(status,-995);self.assertEqual(updated.rate,44100)
  self.assertFalse(attempt);self.assertFalse(reset)
 def test_buffer_size_granularity(self):
  self.assertEqual(buffer_size(512),(0,(512,512,512,512)))
if __name__=='__main__':unittest.main()
