"""Original IASIO channel/rate behavior PARTIAL MODEL, not original C++ or driver.
Normal, bounded synthetic inputs only. Source RVA evidence: 0x85D0,0x86D0,
0x1AD0,0x1960,0x1C10 and batch12 documents.
"""
from dataclasses import dataclass,replace
@dataclass(frozen=True)
class Port:
 input:bool
 flags:int
 shared_channels:int=2
 exclusive_channels:int=2
 shared_bits:int=16
 exclusive_bits:int=16
 shared_rates:tuple=()
 exclusive_rates:tuple=()
 name:str='Unknown'
@dataclass(frozen=True)
class Config:
 exclusive:bool
 inputs:tuple
 outputs:tuple
 rate:int=44100
def validate_rate(c,r):
 eligible=[p for p in c.inputs+c.outputs if p.flags&2]
 return all(bool(p.flags&0x40) or r in (p.exclusive_rates if c.exclusive else p.shared_rates) for p in eligible)
def can_sample_rate(c,requested):
 r=int(requested)
 if r < -(1<<31) or r >= (1<<31):raise OverflowError('SSE conversion edge not modeled')
 return 0 if validate_rate(c,r) else -997
def channel_info(c,index,is_input):
 if index<0:return -998,None
 ports=c.inputs if is_input else c.outputs
 count=0
 for p in ports:
  count+=p.exclusive_channels if c.exclusive else p.shared_channels
  if index<count:
   depth=p.exclusive_bits if c.exclusive else p.shared_bits
   result={'isActive':1,'channelGroup':0,'name':p.name[:28]+' '+str(index+1),'type':None}
   if depth not in (16,24,32):return -1000,result
   result['type']={16:16,24:17,32:18}[depth]
   return 0,result
 return -1000,None
def set_sample_rate_path(c,cached_rate,requested,helper=True,key=True,callback=True):
 r=int(requested)
 if r==cached_rate:return 0,c,False,False
 if not validate_rate(c,r):return -995,c,False,False
 changed=replace(c,rate=r)
 if not helper:return -995,changed,False,False
 return 0,changed,key,callback
def buffer_size(n):return (0,(n,n,n,n)) if n>0 else (-1000,None)
