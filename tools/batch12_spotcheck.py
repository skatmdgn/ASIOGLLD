#!/usr/bin/env python3
"""Read-only original binary SHA/ABI opcode spotcheck (full 206-site checks in ZIP)."""
import hashlib,struct,sys
from pathlib import Path
SHA="e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd"
VTABLE=[0x1050,0x1060,0x1070,0x16b0,0x1650,0x1690,0x16a0,0x1740,0x1770,
0x1910,0x1930,0x1c50,0x1ad0,0x1aa0,0x1960,0x1bd0,0x1c00,0x17e0,
0x1c10,0x1c90,0x1d40,0x1dc0,0x5fa0,0x5fa0]
OPCODES={0x1bd2:"c7420c01000000",0x1bf6:"41c70001000000",
0x1c00:"f7da",0x1c02:"1bc0",0x1c04:"251afcffff",
0x1c22:"e8a96a0000",0x1c27:"33d2",
0x1c70:"418901",0x1c73:"8902",0x1c75:"418900",0x1c78:"418902",
0x1ce7:"e8c4750000",0x1cec:"33c0",0x1d04:"ff90a0000000",
0x1a23:"ff5010",0x86b2:"44894f24",
0x876d:"c7470801000000",0x8774:"c7470c00000000",
0x879e:"c7471012000000",0x87b7:"c7471011000000",
0x87da:"c7471010000000"}
def audit(filename):
 b=Path(filename).read_bytes()
 if hashlib.sha256(b).hexdigest()!=SHA:raise ValueError('Not the exact original DLL')
 pe=struct.unpack_from('<I',b,0x3c)[0];coff=pe+4;opt=pe+24
 if b[:2]!=b'MZ' or b[pe:pe+4]!=b'PE\x00\x00' or struct.unpack_from('<H',b,coff)[0]!=0x8664:raise ValueError('Invalid Win64 PE')
 base=struct.unpack_from('<Q',b,opt+24)[0];sh=opt+struct.unpack_from('<H',b,coff+16)[0]
 sec=[]
 for i in range(struct.unpack_from('<H',b,coff+2)[0]):
  p=sh+i*40;_,r,s,o=struct.unpack_from('<IIII',b,p+8);sec.append((r,s,o))
 def read(r,n):
  for a,s,o in sec:
   if a<=r and r+n<=a+s:return b[o+r-a:o+r-a+n]
  raise ValueError('Unmapped RVA '+hex(r))
 for i,v in enumerate(VTABLE):
  if struct.unpack('<Q',read(0x202f8+8*i,8))[0]-base!=v:raise AssertionError('IASIO slot '+str(i))
 for r,x in OPCODES.items():
  if read(r,len(x)//2)!=bytes.fromhex(x):raise AssertionError('original opcode '+hex(r))
 if read(0x201e0,9)!=b'Internal\x00' or read(0x20888,10)!=b'%.28ws %d\x00':raise AssertionError('rdata')
 print('PASS SHA, 24 IASIO pointers,',len(OPCODES),'original opcode signatures, 2 original strings')
 print('STATIC ONLY: not Windows behavior or faithful rebuilt DLL')
if __name__=='__main__':
 if len(sys.argv)!=2:raise SystemExit('Usage: python batch12_spotcheck.py path/to/original.dll')
 audit(sys.argv[1])
