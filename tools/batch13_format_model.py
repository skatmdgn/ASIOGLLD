"""Original normal-case WASAPI candidate probing PARTIAL MODEL, not a DLL."""
from dataclasses import dataclass,field
FREQUENCIES=(44100,48000,96000)
CHANNELS=(2,)
DEPTHS=(16,)
CHANNEL_MASK=3
@dataclass
class Rate:
 rate:int
 channels:dict=field(default_factory=dict)
@dataclass
class Tree:
 rates:list=field(default_factory=list)
 accepted:int=0
 def add(self,rate,channels,depth):
  self.accepted+=1
  n=next((x for x in self.rates if x.rate==rate),None)
  if n is None:
   n=Rate(rate);self.rates.append(n)
  n.channels.setdefault(channels,set()).add(depth)
def probe(supports,mode,special=False):
 t=Tree()
 if special:return t
 for ch in CHANNELS:
  for rate in FREQUENCIES:
   for width in DEPTHS:
    if supports(mode,rate,ch,width)==0:t.add(rate,ch,width)
 return t
def has_rate(tree,rate):
 return any(n.rate==rate for n in tree.rates)
