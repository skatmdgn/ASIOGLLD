import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from batch18_listener_model import Registration,config_com_init
class Batch18Synthetic(unittest.TestCase):
 def test_hresult_ignored(self):self.assertTrue(config_com_init(0x80010106,True)['CoCreateInstance_attempted'])
 def test_enum_can_be_absent(self):self.assertFalse(config_com_init(0,False)['enumerator_pointer_nonnull'])
 def test_listener_attempted_on_failure(self):
  x=Registration(True);x.setup(hr=0x80004005)
  self.assertIsNotNone(x.listener)
  self.assertEqual(x.listener.registration_hresult,0x80004005)
 def test_refcount_of_os_stays_unknown(self):
  x=Registration(True);x.setup();self.assertIsNone(x.listener.os_refs)
 def test_failed_register_can_still_attempt_unreg(self):
  x=Registration(True);x.setup(hr=0x80004005);x.teardown()
  self.assertIn('enumerator.UnregisterEndpointNotificationCallback',x.events)
 def test_success_register_unreg(self):
  x=Registration(True);x.setup();x.teardown()
  self.assertEqual(x.events.count('enumerator.UnregisterEndpointNotificationCallback'),1)
 def test_alloc_fail_no_unreg(self):
  x=Registration(True);x.setup(alloc_ok=False);x.teardown()
  self.assertNotIn('enumerator.UnregisterEndpointNotificationCallback',x.events)
 def test_enum_fail_no_registration(self):
  x=Registration(False);x.setup();self.assertIsNone(x.listener)
if __name__=='__main__':unittest.main()
