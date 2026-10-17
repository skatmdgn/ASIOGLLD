"""Partial original-instruction-based worker shutdown model, NOT native ASIO driver."""
from dataclasses import dataclass,field
STARTED=0x10
@dataclass
class Port:
 flags:int=0
 has_client:bool=True
 capture:bool=False
 render:bool=False
 clock:bool=False
 event:bool=False
@dataclass
class Worker:
 stop_byte:int=0
 active:int=1
 event:bool=True
 thread:bool=True
 ports:list=field(default_factory=list)
 callbacks:bool=True
@dataclass
class Trace:
 actions:list=field(default_factory=list)
 wait_result:int=0
 def emit(self,event):self.actions.append(event)
def notify(worker,trace):
 worker.active &= ~1
 for p in worker.ports:
  if p.flags&STARTED and p.has_client:trace.emit('IAudioClient.Stop')
  p.flags &= ~STARTED
def stop(worker,trace):
 if worker.stop_byte==0 and worker.event and worker.thread:
  worker.stop_byte=1
  trace.emit('SetEvent')
  trace.emit('WaitForSingleObject(3000)')
  # Wait status is not inspected by original code in this path.
  trace.emit('CloseHandle(thread)');worker.thread=False
  trace.emit('CloseHandle(event)');worker.event=False
 trace.emit('EnterCriticalSection')
 for p in worker.ports:
  if p.flags&0x08:
   for attr in ('capture','render','clock'):
    if getattr(p,attr):
     trace.emit('Release.'+attr);setattr(p,attr,False)
   if p.event:trace.emit('CloseHandle.portEvent');p.event=False
  if p.flags&0x04:
   if p.has_client:trace.emit('Release.IAudioClient');p.has_client=False
   p.flags &= ~0x04
  p.flags &= ~0x08
 worker.ports.clear()
 trace.emit('LeaveCriticalSection')
 worker.callbacks=False
