"""PARTIAL original-only notification behavior model, not a working ASIO driver."""
from dataclasses import dataclass,field
STARTED=0x10
SIMULATED=0x40
WORKER_EVENTS=('OnDeviceStateChanged','OnDeviceAdded','OnDeviceRemoved','OnDefaultDeviceChanged')
@dataclass
class Port:
 flags:int=0
 client:bool=True
 stop_hresult:int=0
 stop_count:int=0
@dataclass
class Worker:
 flags:int=1
 ports:list=field(default_factory=list)
@dataclass
class Trace:
 resets:int=0
 stops:list=field(default_factory=list)
def audio_client_start(port,hr=0):
 if (port.flags&SIMULATED) or (port.client and hr==0):port.flags|=STARTED
 return port.flags
def config_listener(event,host_callbacks_present,trace):
 if event=='OnDeviceStateChanged' and host_callbacks_present:
  trace.resets+=1 # Calls ASIOCallbacks::asioMessage(3,0,0,nullptr), return ignored
 return 0
def worker_listener(event,worker,trace):
 if event not in WORKER_EVENTS:return 0
 worker.flags &= ~1
 for i,port in enumerate(worker.ports):
  if port.flags&STARTED and port.client:
   port.stop_count+=1;trace.stops.append((i,port.stop_hresult))
  port.flags &= ~STARTED
 return 0
@dataclass
class CallbackLifetime:
 callbacks_present:bool=False
 def create_buffers(self,success,callback_present=True):
  if success:self.callbacks_present=callback_present;return 0
  self.dispose_buffers();return -994
 def dispose_buffers(self):
  self.callbacks_present=False;return 0
