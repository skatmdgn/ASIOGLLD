import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import unittest
from batch10_worker_model import expected_mask,per_poll,advance_buffer,wait_gate
class WorkerModelTests(unittest.TestCase):
    def test_expected_mask(self):
        self.assertEqual([expected_mask(n) for n in range(4)],[0,1,3,7])
    def test_persistent_mask_across_iterations(self):
        a=per_poll([(True,True),(False,True)])
        self.assertFalse(a.callback)
        b=per_poll([(False,False),(True,True)],a.next_mask)
        self.assertTrue(b.callback)
        self.assertEqual(b.next_mask,0)
    def test_shortcut_not_a_full_reset(self):
        self.assertEqual(per_poll([(True,True),(False,True)]).next_mask,1)
    def test_double_buffer(self):
        self.assertEqual(advance_buffer(0,0),(1,1,1))
        self.assertEqual(advance_buffer(1,1),(0,2,1))
    def test_wait_failed_and_timeout(self):
        self.assertEqual(wait_gate(False,0xffffffff,False,True),'EXIT')
        self.assertEqual(wait_gate(False,0x102,False,True),'PROCESS')
    def test_mask_aliasing_above_32_is_synthetic(self):
        self.assertEqual(expected_mask(32),expected_mask(33))
if __name__=='__main__':unittest.main()
