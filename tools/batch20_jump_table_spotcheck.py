#!/usr/bin/env python3
"""Standalone SHA-pinned recovery of 7 original table-branch destinations.
Standard-library-only; reads but never executes or modifies the original DLL.
Not a source-level decompiler or native ASIO runtime parity check.
"""
import bisect,hashlib,struct,sys
from pathlib import Path
SHA='e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd'
# Site RVA: target dword table RVA, entry count, optional selector remap byte RVA, selector count
SPECS={0xe564:(0xf148,8,None,8),0xe8a8:(0xf168,15,0xf1a4,56),
 0x10ade:(0x10cec,6,0x10d04,21),0x1b656:(0x1be90,12,None,12),
 0x1b716:(0x1bec0,4,0x1bed0,59),0x1b7cc:(0x1bf0c,3,0x1bf18,59),
 0x1b850:(0x1bf54,3,0x1bf60,59)}
def audit(path):
 b=Path(path).read_bytes()
 if len(b)!=173056 or hashlib.sha256(b).hexdigest()!=SHA:raise ValueError('Unexpected original DLL bytes')
 nt=struct.unpack_from('<I',b,0x3c)[0];coff=nt+4;opt=coff+20
 if b[:2]!=b'MZ' or b[nt:nt+4]!=b'PE\0\0' or struct.unpack_from('<H',b,coff)[0]!=0x8664 or struct.unpack_from('<H',b,opt)[0]!=0x20b:raise ValueError('Not Win64 PE32+')
 sh=opt+struct.unpack_from('<H',b,coff+16)[0];sections=[]
 for i in range(struct.unpack_from('<H',b,coff+2)[0]):
  p=sh+40*i;v,s,size,raw=struct.unpack_from('<IIII',b,p+8);sections.append((s,size,raw))
 def read(r,n):
  for base,size,off in sections:
   if base<=r and r+n<=base+size:return b[off+r-base:off+r-base+n]
  raise ValueError('Unmapped RVA '+hex(r))
 pdata,size=struct.unpack_from('<II',b,opt+112+3*8)
 if size!=590*12:raise ValueError('Unexpected unwind records')
 entries=[struct.unpack('<III',read(pdata+12*i,12)) for i in range(590)]
 lookup={triple:i for i,triple in enumerate(entries)};parents={}
 for i,(a,z,u) in enumerate(entries):
  flags,n=read(u,3)[0]>>3,read(u,3)[2]
  if flags==4:
   chain=struct.unpack('<III',read(u+4+4*((n+1)//2),12))
   if chain not in lookup:raise ValueError('Broken unwind chain')
   parents[i]=lookup[chain]
 def root(r):
  idx=bisect.bisect_right([x[0] for x in entries],r)-1
  if idx<0 or not(entries[idx][0]<=r<entries[idx][1]):raise ValueError('Target outside unwind body '+hex(r))
  visited=set()
  while idx in parents:
   if idx in visited:raise ValueError('Cyclic unwind chain')
   visited.add(idx);idx=parents[idx]
  return idx
 output=[]
 for site,(table,n,remap,length) in SPECS.items():
  if read(site,2) != (b'\xff\xe2' if site==0x10ade else b'\xff\xe1'):raise AssertionError('Indirect jump changed '+hex(site))
  target_table=[struct.unpack('<I',read(table+4*i,4))[0] for i in range(n)]
  indices=list(read(remap,length)) if remap is not None else list(range(length))
  if max(indices)>=n:raise AssertionError('Invalid remap selector '+hex(site))
  targets=[target_table[j] for j in indices]
  if any(root(t)!=root(site) for t in targets):raise AssertionError('Jump crosses original root '+hex(site))
  output.append((site,length,len(set(targets))))
 if sum(n for _,n,_ in output)!=274 or len({struct.unpack('<I',read(t+4*j,4))[0] for t,n,_,_ in SPECS.values() for j in range(n)})!=45:raise AssertionError('Unexpected original table totals')
 print('PASS: original SHA; 590 unwind records; 7 table-jumps, 274 selectors, 45 unique same-root targets')
 print('Original not loaded/executed/modified; not Ghidra or Windows parity.')
 return output
if __name__=='__main__':
 if len(sys.argv)!=2:raise SystemExit('Usage: python batch20_jump_table_spotcheck.py ORIGINAL.dll')
 audit(sys.argv[1])
