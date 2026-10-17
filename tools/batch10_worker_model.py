"""Batch10 original static *model*, NOT a working ASIO implementation."""
from dataclasses import dataclass
U32=0xffffffff
def rol32(x,n=1):
    n &= 31
    x &= U32
    return ((x << n) | (x >> (32-n))) & U32 if n else x
def expected_mask(n):
    if n<0:raise ValueError('negative port count')
    bit=1;out=0
    for _ in range(n):
        out |= bit
        bit=rol32(bit)
    return out
@dataclass(frozen=True)
class PortPass:
    expected:int
    complete:int
    next_mask:int
    callback:bool
def per_poll(results,previous_mask=0):
    complete=previous_mask & U32
    for index,(capture_ok,render_ok) in enumerate(results):
        if capture_ok and render_ok:
            complete |= rol32(1,index)
    expected=expected_mask(len(results))
    ready=(expected==complete)
    return PortPass(expected,complete,0 if ready else complete,ready)
def advance_buffer(index,blocks):
    if index not in (0,1):raise ValueError('invalid ASIO double buffer index')
    return (index^1,(blocks+1)&0xffffffffffffffff,1)  # index, blocks, directProcess
def wait_gate(stop_before,wait_result,stop_after,active):
    if stop_before or (wait_result&U32)==U32 or stop_after:return 'EXIT'
    if not active:return 'RETRY'
    return 'PROCESS'  # WAIT_TIMEOUT also traverses this code path
