"""Synthetic-only COM listener state tracking; not original C++ source."""
from dataclasses import dataclass,field
@dataclass
class Listener:
 refs_native:int=0
 os_refs:int|None=None
 registration_hresult:int|None=None
@dataclass
class Registration:
 enumerator:bool
 listener:Listener|None=None
 events:list=field(default_factory=list)
 def setup(self,alloc_ok=True,hr=0):
  if not self.enumerator or not alloc_ok:return
  self.listener=Listener(refs_native=1,registration_hresult=hr)
  self.events+=['listener.AddRef','enumerator.RegisterEndpointNotificationCallback']
 def teardown(self):
  if self.listener is not None:
   if self.enumerator:self.events.append('enumerator.UnregisterEndpointNotificationCallback')
   self.events.append('listener.Release')
   self.listener.refs_native-=1;self.listener=None
  if self.enumerator:self.events.append('enumerator.Release');self.enumerator=False
def config_com_init(hr,enumerator_present):
 return {'CoInitializeEx_hresult_ignored':True,
  'CoInitializeEx_hresult':hr,'CoCreateInstance_attempted':True,
  'enumerator_pointer_nonnull':bool(enumerator_present)}
