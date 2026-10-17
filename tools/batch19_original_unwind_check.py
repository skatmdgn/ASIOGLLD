#!/usr/bin/env python3
"""Read-only original Win64 x64 unwind chain verification; Python standard library."""
import collections,hashlib,struct,sys
from pathlib import Path
EXPECTED="e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd"
def check(path):
 b=Path(path).read_bytes()
 if len(b)!=173056 or hashlib.sha256(b).hexdigest()!=EXPECTED:raise ValueError("Original SHA mismatch")
 nt=struct.unpack_from("<I",b,0x3c)[0];coff=nt+4;opt=coff+20
 if b[:2]!=b"MZ" or b[nt:nt+4]!=b"PE\x00\x00" or struct.unpack_from("<H",b,coff)[0]!=0x8664 or struct.unpack_from("<H",b,opt)[0]!=0x20b:raise ValueError("Expected x64 PE32+")
 section=[];sh=opt+struct.unpack_from("<H",b,coff+16)[0]
 for i in range(struct.unpack_from("<H",b,coff+2)[0]):
  p=sh+40*i;_,start,size,off=struct.unpack_from("<IIII",b,p+8);section.append((start,size,off))
 def read(rva,n):
  for a,size,off in section:
   if a<=rva and rva+n<=a+size:return b[off+rva-a:off+rva-a+n]
  raise ValueError("Unmapped RVA "+hex(rva))
 rva,size=struct.unpack_from("<II",b,opt+112+3*8)
 if size%12:raise ValueError("Invalid pdata size")
 records=[struct.unpack("<III",read(rva+12*i,12)) for i in range(size//12)]
 known=set(records);parents={};handlers=collections.Counter()
 for a,z,u in records:
  first,_,n,_=struct.unpack("<BBBB",read(u,4));flag=first>>3
  if first&7!=1 or flag not in (0,1,2,3,4) or a>=z:raise ValueError("Invalid unwind record")
  trailer=u+4+4*((n+1)//2)
  if flag==4:
   target=struct.unpack("<III",read(trailer,12))
   if target not in known:raise ValueError("Broken CHAININFO")
   parents[(a,z,u)]=target
  elif flag&3:handlers[struct.unpack("<I",read(trailer,4))[0]]+=1
 def root(r):
  seen=set()
  while r in parents:
   if r in seen:raise ValueError("Cyclic chain")
   seen.add(r);r=parents[r]
  return r
 counts=(len(records),len(parents),len({root(r) for r in records}))
 if counts!=(590,221,369) or dict(handlers)!={0x105c0:30,0x12510:42,0x16f80:12}:raise ValueError("Unexpected original unwind data")
 print("PASS original SHA: pdata=%d chained=%d roots=%d exception records=84"%counts)
 print("Static unwind roots are not exact source-level C++ function count.")
if __name__=="__main__":
 if len(sys.argv)!=2:raise SystemExit("Usage: python tools/batch19_original_unwind_check.py ORIGINAL.dll")
 check(sys.argv[1])
