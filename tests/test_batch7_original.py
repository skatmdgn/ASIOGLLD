import unittest
from tools.batch7_original_wasapi import initialize_args

class OriginalBranchModelTest(unittest.TestCase):
    def test_shared_original(self):
        for duration in (0,1,10,50,100):
            self.assertEqual(initialize_args(duration,False,False),
              {'shareMode':0,'flags':0,'buffer':duration*20000,'period':0})
    def test_exclusive_event(self):
        self.assertEqual(initialize_args(10,True,True),
          {'shareMode':1,'flags':0x40000,'buffer':100000,'period':100000})
    def test_exclusive_non_event(self):
        self.assertEqual(initialize_args(10,True,False),
          {'shareMode':1,'flags':0,'buffer':200000,'period':0})
if __name__=='__main__':unittest.main()
