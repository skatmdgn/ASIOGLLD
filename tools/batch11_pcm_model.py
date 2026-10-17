"""Partial PCM-domain original algorithm model: not a driver or complete source."""
from dataclasses import dataclass
WIDTHS=(1,2,4)
def channel_to_interleaved(dst,src,width,channels,channel,frames):
 if width not in WIDTHS or frames<=0:return
 if not (0<=channel<channels) or len(src)<frames*width or len(dst)<frames*channels*width:raise ValueError("invalid prevalidated buffers")
 for n in range(frames):
  dst[(n*channels+channel)*width:(n*channels+channel+1)*width]=src[n*width:(n+1)*width]
def interleaved_to_channel(dst,src,width,channels,channel,frames,offset=0):
 if width not in WIDTHS or frames<=0:return
 if not (0<=channel<channels) or offset<0 or len(src)<frames*channels*width or len(dst)<(offset+frames)*width:raise ValueError("invalid prevalidated buffers")
 for n in range(frames):
  dst[(offset+n)*width:(offset+n+1)*width]=src[(n*channels+channel)*width:(n*channels+channel+1)*width]
@dataclass(frozen=True)
class Ring:
 offset:int
 index:int
 blocks:int
def ring_advance(pos,consumed,frames,ring_count):
 if min(consumed,frames,ring_count)<0 or frames==0 or ring_count==0:raise ValueError("bad ring")
 q,rem=divmod(consumed,frames)
 off=pos.offset+rem
 if off>=frames:off-=frames;q+=1
 idx=pos.index+q
 if idx>=ring_count:idx-=ring_count
 return Ring(off,idx,pos.blocks+q)
